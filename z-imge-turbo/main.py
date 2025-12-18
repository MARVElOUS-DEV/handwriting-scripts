# =============================================================================
# Z-Image-Turbo 推理服务 + Gradio Web UI
# =============================================================================
# 部署命令: uv run modal deploy main.py
# =============================================================================

import io
import base64
import secrets
from pathlib import Path

import modal

# =============================================================================
# S1: 环境准备 - 构建基础镜像
# =============================================================================
LOCAL_DIR = Path(__file__).parent

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install(
        "torch>=2.4.0",
        "diffusers>=0.33.0",
        "transformers>=4.47.0",
        "accelerate>=1.2.0",
        "safetensors>=0.4.0",
        "sentencepiece>=0.2.0",
        "huggingface_hub[hf_transfer]>=0.27.0",
        "fastapi[standard]>=0.115.0",
        "pillow>=10.0.0",
        "gradio>=6.0.0",
        "itsdangerous",
        "uvicorn",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .add_local_file(LOCAL_DIR / "gradio_app.py", "/app/gradio_app.py")
)

# HuggingFace Secret
try:
    hf_secret = modal.Secret.from_name("huggingface-secret")
except modal.exception.NotFoundError:
    hf_secret = None

# Gradio Auth Secret (create with: modal secret create gradio-auth GRADIO_USER=admin GRADIO_PASS=yourpassword)
try:
    gradio_auth_secret = modal.Secret.from_name("gradio-auth")
except modal.exception.NotFoundError:
    gradio_auth_secret = None

# =============================================================================
# S2: Modal App 配置
# =============================================================================
vol = modal.Volume.from_name("z-image-turbo-cache", create_if_missing=True)
app = modal.App(name="z-image-turbo", image=image)

MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"
CACHE_DIR = "/cache/models"

# =============================================================================
# S3: 推理服务类
# =============================================================================
# @app.cls(
#     gpu="L40S",
#     volumes={"/cache": vol},
#     secrets=[hf_secret] if hf_secret else [],
#     timeout=600,
#     container_idle_timeout=300,
# )
# @modal.concurrent(max_inputs=10)
class ZImageInference:
    """Z-Image-Turbo 推理服务"""

    # @modal.enter()
    def load_model(self):
        """容器启动时加载模型"""
        import os
        import torch
        from diffusers import ZImagePipeline, AutoencoderKL
        from diffusers.models.transformers.transformer_z_image import ZImageTransformer2DModel
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print("Loading Z-Image-Turbo model...")

        hf_token = os.getenv("HF_TOKEN")
        cache_dir = CACHE_DIR

        print("   Loading VAE...")
        vae = AutoencoderKL.from_pretrained(
            MODEL_ID,
            subfolder="vae",
            torch_dtype=torch.bfloat16,
            cache_dir=cache_dir,
            token=hf_token,
        )

        print("   Loading text encoder...")
        text_encoder = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            subfolder="text_encoder",
            torch_dtype=torch.bfloat16,
            cache_dir=cache_dir,
            token=hf_token,
        ).eval()

        print("   Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            subfolder="tokenizer",
            cache_dir=cache_dir,
            token=hf_token,
        )
        tokenizer.padding_side = "left"

        print("   Loading transformer...")
        transformer = ZImageTransformer2DModel.from_pretrained(
            MODEL_ID,
            subfolder="transformer",
            cache_dir=cache_dir,
            token=hf_token,
        ).to(torch.bfloat16)

        print("   Assembling pipeline...")
        self.pipe = ZImagePipeline(
            scheduler=None,
            vae=vae,
            text_encoder=text_encoder,
            tokenizer=tokenizer,
            transformer=transformer,
        )
        self.pipe.to("cuda", torch.bfloat16)
        self.pipe.transformer.set_attention_backend("native")

        print("Model loaded successfully!")

    # @modal.method()
    def generate(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 9,
        seed: int = -1,
        shift: float = 3.0,
    ) -> tuple:
        """生成图像，返回 PIL Image 和 seed"""
        import random
        import torch
        from diffusers import FlowMatchEulerDiscreteScheduler

        if seed == -1:
            seed = random.randint(1, 1000000)

        generator = torch.Generator("cuda").manual_seed(seed)

        scheduler = FlowMatchEulerDiscreteScheduler(
            num_train_timesteps=1000,
            shift=shift,
        )
        self.pipe.scheduler = scheduler

        image = self.pipe(
            prompt=prompt,
            height=height,
            width=width,
            guidance_scale=0.0,
            num_inference_steps=num_inference_steps + 1,
            generator=generator,
            max_sequence_length=512,
        ).images[0]

        return image, seed

    # @modal.web_endpoint(method="POST")
    def api(self, request: dict) -> dict:
        """REST API 端点"""
        image, seed = self.generate(
            prompt=request.get("prompt", "a beautiful landscape"),
            width=request.get("width", 1024),
            height=request.get("height", 1024),
            num_inference_steps=request.get("num_inference_steps", 9),
            seed=request.get("seed", -1),
            shift=request.get("shift", 3.0),
        )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"image": image_base64, "seed": seed}


# =============================================================================
# S4: Gradio Web UI
# =============================================================================
_ui_secrets = [s for s in [hf_secret, gradio_auth_secret] if s is not None]

# Generate a consistent secret key for this deployment
GRADIO_SECRET_KEY = secrets.token_hex(32)

@app.function(
    gpu="L40S",
    volumes={"/cache": vol},
    secrets=_ui_secrets,
    env={"GRADIO_SECRET_KEY": GRADIO_SECRET_KEY},
    timeout=86400,  # Max function runtime: 24 hours
    container_idle_timeout=600,  # Keep container warm for 10 min after last request
    keep_warm=0,  # Keep 1 container pre-warmed and ready
    max_containers=1,
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=180)
def ui():
    """Gradio Web 界面"""
    import subprocess

    subprocess.Popen(["python", "/app/gradio_app.py"])


# =============================================================================
# S4.0: Optional Heartbeat (Keeps container warm - usually not needed with keep_warm=1)
# =============================================================================
# Uncomment below if you want extra insurance to keep containers alive

# from modal import Period
# 
# @app.function(
#     schedule=Period(minutes=5),  # Ping every 5 minutes
#     secrets=_ui_secrets,
# )
# def heartbeat():
#     """Optional: Ping service to prevent cold starts"""
#     import requests
#     import os
#     
#     service_url = os.getenv("SERVICE_URL")  # Set in Modal dashboard
#     if not service_url:
#         print("⚠️ SERVICE_URL not set, skipping heartbeat")
#         return
#     
#     try:
#         response = requests.get(f"{service_url}/", timeout=10)
#         print(f"✅ Heartbeat OK: {response.status_code}")
#     except Exception as e:
#         print(f"⚠️ Heartbeat failed: {e}")


# =============================================================================
# S4.5: Debug Test Function
# =============================================================================
@app.function(
    gpu="L40S",
    volumes={"/cache": vol},
    secrets=_ui_secrets,
    timeout=600,
)
def test_img2img():
    """Test img2img generation with detailed logging"""
    import sys
    sys.path.insert(0, '/app')
    
    print("=" * 60)
    print("Testing img2img generation...")
    print("=" * 60)
    
    try:
        from gradio_app import load_pipeline, create_generate_img2img
        from PIL import Image
        
        print("\n1. Loading models...")
        pipe, vae = load_pipeline()
        print("✅ Models loaded successfully")
        
        print("\n2. Creating generator function...")
        generate_img2img = create_generate_img2img(pipe, vae)
        print("✅ Generator function created")
        
        print("\n3. Creating test image...")
        test_image = Image.new('RGB', (512, 512), color='red')
        print(f"✅ Test image created: {test_image.size}")
        
        print("\n4. Running img2img generation...")
        result_image, seed = generate_img2img(
            prompt="a beautiful landscape with mountains",
            input_image=test_image,
            denoise_strength=0.7,
            num_steps=8,
            seed=42,
            random_seed=False,
            shift=3.0
        )
        
        print(f"\n✅ SUCCESS! Generated image with seed: {seed}")
        print(f"   Result image size: {result_image.size}")
        return f"SUCCESS - Seed: {seed}"
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return f"FAILED: {str(e)}"


# =============================================================================
# S5: 本地入口点
# =============================================================================
@app.local_entrypoint()
def test():
    """Run img2img test"""
    print("\n🧪 Running img2img test...\n")
    result = test_img2img.remote()
    print(f"\n📊 Test Result: {result}\n")


@app.local_entrypoint()
def main():
    print("=" * 60)
    print("Z-Image-Turbo Inference Service")
    print("=" * 60)
    print(f"\nModel: {MODEL_ID}")
    print("\nFeatures:")
    print("   - 6B parameter efficient image generation")
    print("   - Chinese and English prompt support")
    print("   - 9-step fast generation")
    print("   - Gradio Web UI")
    print("   - REST API endpoint")
    print("\n" + "=" * 60)
    print("USAGE:")
    print("=" * 60)
    print("\n🧪 Test img2img:     modal run main.py::test")
    print("🔥 Dev mode:         modal serve main.py")
    print("🚀 Deploy:           modal deploy main.py")
    print("\n" + "=" * 60)
