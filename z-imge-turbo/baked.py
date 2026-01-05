# =============================================================================
# Z-Image-Turbo ComfyUI 一键部署服务
# =============================================================================
# 启动命令: modal deploy z_image_turbo_deploy.py
# =============================================================================

import json
import os
import subprocess
import sys
from pathlib import Path

import modal

# Add repo root to sys.path to allow importing modal_libs
repo_root = Path(__file__).parent.parent
sys.path.append(str(repo_root))

from modal_libs import (
    get_base_image,
    get_hf_secret,
    get_model_cache_volume,
    download_hf_model_file,
)

# =============================================================================
# S1: 环境准备 - 构建基础镜像
# =============================================================================
image = (
    get_base_image(
        python_version="3.12",
        pip_packages=[
            "fastapi[standard]==0.115.4",
            "comfy-cli==1.5.3",
            "requests==2.32.3",
            "huggingface_hub[hf_transfer]==0.34.4",
        ],
    )
    .run_commands("comfy --skip-prompt install --fast-deps --nvidia")
    .add_local_python_source("modal_libs")
)

# HuggingFace Secret
hf_secret = get_hf_secret()


# =============================================================================
# S2: 模型下载 - 从 Tongyi-MAI/Z-Image-Turbo 下载 3 个核心模型
# =============================================================================
def hf_download():
    """
    下载 Z-Image-Turbo 模型:
    - z_image_turbo_bf16.safetensors (主扩散模型)
    - qwen_3_4b.safetensors (CLIP 文本编码器)
    - ae.safetensors (VAE 解码器)
    """
    hf_token = os.getenv("HF_TOKEN")
    repo_id = "Comfy-Org/z_image_turbo"

    print(f"📦 从 {repo_id} 下载模型...")

    # 模型配置列表 (文件路径包含 split_files/ 前缀)
    models = [
        {
            "filename": "split_files/diffusion_models/z_image_turbo_bf16.safetensors",
            "target_dir": "/root/comfy/ComfyUI/models/diffusion_models",
            "target_name": "z_image_turbo_bf16.safetensors",
            "desc": "主扩散模型",
        },
        {
            "filename": "split_files/text_encoders/qwen_3_4b.safetensors",
            "target_dir": "/root/comfy/ComfyUI/models/clip",
            "target_name": "qwen_3_4b.safetensors",
            "desc": "CLIP 文本编码器",
        },
        {
            "filename": "split_files/vae/ae.safetensors",
            "target_dir": "/root/comfy/ComfyUI/models/vae",
            "target_name": "ae.safetensors",
            "desc": "VAE 解码器",
        },
    ]

    for model in models:
        print(f"📥 下载 {model['desc']}: {model['target_name']}...")

        # We need to manually symlink here because download_hf_model_file
        # symlinks to `target_dir/filename.name`.
        # But here `target_name` might be different or `filename` includes subdir.
        # Actually download_hf_model_file logic:
        # target_path = Path(target_dir) / Path(filename).name
        # Here filename has "split_files/..." prefix.
        # So Path(filename).name is just the file name.
        # target_name in dict is also just the file name.
        # So it matches.

        download_hf_model_file(
            repo_id=repo_id,
            filename=model["filename"],
            target_dir=model["target_dir"],
            token=hf_token,
        )
        print(f"   ✅ {model['desc']} 完成")

    print("🎉 所有模型下载完成!")


def create_workflow_file():
    """创建工作流 JSON 文件到 ComfyUI 用户目录"""
    workflow = {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "z_image_turbo_bf16.safetensors",
                "weight_dtype": "default",
            },
        },
        "2": {
            "class_type": "DualCLIPLoader",
            "inputs": {
                "clip_name1": "qwen_3_4b.safetensors",
                "clip_name2": "qwen_3_4b.safetensors",
                "type": "z_image",
            },
        },
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "一位美丽的亚洲女性，照片级真实，自然光线，高清细节",
                "clip": ["2", 0],
            },
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "低质量，模糊，畸形，丑陋，文字，水印",
                "clip": ["2", 0],
            },
        },
        "6": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0],
                "seed": 42,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["7", 0], "vae": ["3", 0]},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "z_image_turbo", "images": ["8", 0]},
        },
    }

    workflow_dir = Path("/root/comfy/ComfyUI/user/default/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_path = workflow_dir / "z_image_turbo.json"
    workflow_path.write_text(json.dumps(workflow, ensure_ascii=False, indent=2))
    print(f"📝 工作流文件已创建: {workflow_path}")


# =============================================================================
# S3: 服务配置
# =============================================================================
vol = get_model_cache_volume("z-image-turbo-cache")

image = image.run_function(
    hf_download, volumes={"/cache": vol}, secrets=[hf_secret] if hf_secret else []
).run_function(create_workflow_file)

app = modal.App(name="z-image-turbo", image=image)


# =============================================================================
# S4: UI 服务
# =============================================================================
@app.function(max_containers=1, gpu="L40S", volumes={"/cache": vol}, timeout=86400)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=60)
def ui():
    """ComfyUI Web 界面"""
    print("🌐 启动 Z-Image-Turbo Web 界面...")
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)


# =============================================================================
# S5: 本地入口点
# =============================================================================
@app.local_entrypoint()
def main():
    print("=" * 60)
    print("Z-Image-Turbo ComfyUI 一键部署")
    print("=" * 60)
    print("\n📦 模型来源: Comfy-Org/z_image_turbo")
    print("\n📋 已下载模型:")
    print("   - z_image_turbo_bf16.safetensors (主扩散模型)")
    print("   - qwen_3_4b.safetensors (CLIP 文本编码器)")
    print("   - ae.safetensors (VAE 解码器)")
    print("\n📌 部署命令: uv run modal deploy main.py")
    print("=" * 60)
