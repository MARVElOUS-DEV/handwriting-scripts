"""
Z-Image-Turbo Gradio Web UI
Standalone script for the Gradio interface.
"""

import os
import random
import traceback
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import gradio as gr
import numpy as np
import torch
from PIL import Image
from diffusers import AutoencoderKL, FlowMatchEulerDiscreteScheduler, ZImagePipeline
from diffusers.models.transformers.transformer_z_image import ZImageTransformer2DModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# =============================================================================
# Configuration
# =============================================================================
MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"
CACHE_DIR = "/cache/models"

RESOLUTION_CHOICES = [
    "1024x1024 (1:1)",
    "1152x896 (9:7)",
    "896x1152 (7:9)",
    "1280x720 (16:9)",
    "720x1280 (9:16)",
    "1344x576 (21:9)",
    "576x1344 (9:21)",
]

EXAMPLE_PROMPTS = [
    ["一位优雅的中国女性，穿着红色旗袍，站在古典园林中，照片级真实，自然光线"],
    ["A majestic snow leopard resting on a rocky mountain peak at sunset, photorealistic"],
    ["极具氛围感的暗调人像，一位优雅的中国美女在黑暗的房间里，高对比度"],
    ["Cyberpunk cityscape at night, neon lights reflecting on wet streets, ultra detailed"],
    ["一杯热咖啡放在木桌上，旁边有一本打开的书，窗外是下雨的街景"],
]


# =============================================================================
# Model Loading
# =============================================================================
def load_pipeline():
    """Load the Z-Image-Turbo pipeline."""
    hf_token = os.getenv("HF_TOKEN")

    print("Loading model for Gradio UI...")

    vae = AutoencoderKL.from_pretrained(
        MODEL_ID,
        subfolder="vae",
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        token=hf_token,
    )
    text_encoder = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        subfolder="text_encoder",
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        token=hf_token,
    ).eval()
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        subfolder="tokenizer",
        cache_dir=CACHE_DIR,
        token=hf_token,
    )
    tokenizer.padding_side = "left"
    transformer = ZImageTransformer2DModel.from_pretrained(
        MODEL_ID,
        subfolder="transformer",
        cache_dir=CACHE_DIR,
        token=hf_token,
    ).to(torch.bfloat16)

    pipe = ZImagePipeline(
        scheduler=None,
        vae=vae,
        text_encoder=text_encoder,
        tokenizer=tokenizer,
        transformer=transformer,
    )
    pipe.to("cuda", torch.bfloat16)
    pipe.transformer.set_attention_backend("native")

    print("Model loaded!")
    return pipe, vae


# =============================================================================
# Helper Functions
# =============================================================================
def parse_resolution(resolution_str: str) -> tuple[int, int]:
    """Parse resolution string to width and height."""
    res = resolution_str.split(" ")[0]
    w, h = res.split("x")
    return int(w), int(h)


def prepare_latents_from_image(image, vae, generator, denoise_strength, num_steps, scheduler):
    """Encode image to latents and add noise based on denoise strength."""
    image = image.convert("RGB")
    w, h = image.size

    # Resize to multiple of 16
    w = (w // 16) * 16
    h = (h // 16) * 16
    image = image.resize((w, h), Image.LANCZOS)

    # Convert to tensor
    image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
    image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)
    image_tensor = (image_tensor - 0.5) * 2.0  # Normalize to [-1, 1]
    image_tensor = image_tensor.to(device="cuda", dtype=torch.bfloat16)

    # Encode to latent space
    with torch.no_grad():
        latent_dist = vae.encode(image_tensor).latent_dist
        latents = latent_dist.sample() * vae.config.scaling_factor

    # Calculate start step based on denoise strength
    start_step = int(num_steps * (1 - denoise_strength))

    # Add noise according to the scheduler
    noise = torch.randn(latents.shape, generator=generator, device=latents.device, dtype=latents.dtype)

    # Get the timestep for the start step
    timesteps = scheduler.timesteps
    if start_step < len(timesteps):
        t = timesteps[start_step]
        # For flow matching, we interpolate between noise and latents
        sigma = t / 1000.0
        noisy_latents = (1 - sigma) * latents + sigma * noise
    else:
        noisy_latents = latents

    return noisy_latents, w, h, start_step


# =============================================================================
# Generation Functions
# =============================================================================
def create_generate_txt2img(pipe):
    """Create text-to-image generation function."""

    def generate_txt2img(prompt, resolution, num_steps, seed, random_seed, shift):
        try:
            if not prompt.strip():
                raise gr.Error("Please enter a prompt")

            width, height = parse_resolution(resolution)

            if random_seed:
                seed = random.randint(1, 1000000)

            generator = torch.Generator("cuda").manual_seed(int(seed))
            scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000, shift=shift)
            pipe.scheduler = scheduler

            image = pipe(
                prompt=prompt,
                height=height,
                width=width,
                guidance_scale=0.0,
                num_inference_steps=int(num_steps) + 1,
                generator=generator,
                max_sequence_length=512,
            ).images[0]

            return image, int(seed)
        except Exception as e:
            traceback.print_exc()
            if isinstance(e, gr.Error):
                raise e
            raise gr.Error(f"Generation failed: {e}")

    return generate_txt2img


def create_generate_img2img(pipe, vae):
    """Create image-to-image generation function."""

    def generate_img2img(prompt, input_image, denoise_strength, num_steps, seed, random_seed, shift):
        try:
            if not prompt.strip():
                raise gr.Error("Please enter a prompt")

            if input_image is None:
                raise gr.Error("Please upload an input image")

            if random_seed:
                seed = random.randint(1, 1000000)

            generator = torch.Generator("cuda").manual_seed(int(seed))
            scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000, shift=shift)
            pipe.scheduler = scheduler

            num_steps = int(num_steps) + 1

            # Set timesteps
            scheduler.set_timesteps(num_steps, device="cuda")

            with torch.inference_mode():
                # Prepare latents from input image
                latents, width, height, start_step = prepare_latents_from_image(
                    input_image, vae, generator, denoise_strength, num_steps, scheduler
                )
                
                # Convert latents to float32 for scheduler (comes as bfloat16 from VAE)
                latents = latents.to(torch.float32)

                # Get prompt embeddings (no CFG for img2img)
                prompt_embeds, _ = pipe.encode_prompt(
                    prompt=prompt,
                    device="cuda",
                    do_classifier_free_guidance=False,
                    max_sequence_length=512,
                )

                # Prepare timesteps for denoising (skip early steps based on denoise strength)
                timesteps = scheduler.timesteps[start_step:]

                # Denoising loop
                for i, t in enumerate(timesteps):
                    # Convert latents to transformer dtype (bfloat16)
                    latent_model_input = latents.to(pipe.transformer.dtype)

                    # Prepare inputs for transformer (ZImageTransformer2DModel expects specific format)
                    # 1. Add temporal dimension and convert to list
                    latent_model_input = latent_model_input.unsqueeze(2)  # Add temporal dim
                    latent_model_input_list = list(latent_model_input.unbind(dim=0))
                    
                    # 2. Prepare timestep (normalized to [0, 1])
                    timestep = t.expand(latents.shape[0])
                    timestep = (1000 - timestep) / 1000  # Normalize
                    
                    # 3. Call transformer with correct signature: (x_list, t, cap_feats_list)
                    model_out_list = pipe.transformer(
                        latent_model_input_list,
                        timestep,
                        prompt_embeds,  # Already a list from encode_prompt
                        return_dict=False,
                    )[0]
                    
                    # 4. Convert output back to tensor
                    noise_pred = torch.stack([out.float() for out in model_out_list], dim=0)
                    noise_pred = noise_pred.squeeze(2)
                    noise_pred = -noise_pred  # Negate as per ZImagePipeline

                    # Compute previous noisy sample (scheduler expects float32)
                    latents = scheduler.step(noise_pred.to(torch.float32), t, latents, return_dict=False)[0]
                    assert latents.dtype == torch.float32  # Ensure latents remain in float32

                # Decode latents to image
                latents = latents.to(torch.bfloat16)  # Convert to VAE's dtype
                latents = (latents / vae.config.scaling_factor) + vae.config.shift_factor
                image = vae.decode(latents, return_dict=False)[0]

                # Post-process image (using image processor like ZImagePipeline)
                image = (image / 2 + 0.5).clamp(0, 1)
                image = (image * 255).permute(0, 2, 3, 1).cpu().byte().numpy()[0]
                image = Image.fromarray(image)

            return image, int(seed)
        except Exception as e:
            traceback.print_exc()
            if isinstance(e, gr.Error):
                raise e
            raise gr.Error(f"Generation failed: {e}")

    return generate_img2img


# =============================================================================
# Gradio UI
# =============================================================================
def create_ui(pipe, vae):
    """Create the Gradio interface."""
    generate_txt2img = create_generate_txt2img(pipe)
    generate_img2img = create_generate_img2img(pipe, vae)

    with gr.Blocks(title="Z-Image-Turbo") as demo:
        gr.Markdown("""
# Z-Image-Turbo

**6B parameter efficient image generation model by Alibaba Tongyi Lab**

- Supports Chinese and English prompts
- Text-to-Image and Image-to-Image modes
- 9-step fast generation
        """)

        with gr.Tabs():
            # Text-to-Image Tab
            with gr.TabItem("Text to Image"):
                with gr.Row():
                    with gr.Column(scale=1):
                        t2i_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="Enter your prompt here... (supports Chinese and English)",
                            lines=3,
                        )

                        t2i_resolution = gr.Dropdown(
                            label="Resolution",
                            choices=RESOLUTION_CHOICES,
                            value="1024x1024 (1:1)",
                        )

                        with gr.Row():
                            t2i_num_steps = gr.Slider(
                                label="Inference Steps",
                                minimum=1,
                                maximum=20,
                                value=8,
                                step=1,
                            )
                            t2i_shift = gr.Slider(
                                label="Time Shift",
                                minimum=1.0,
                                maximum=10.0,
                                value=3.0,
                                step=0.1,
                            )

                        with gr.Row():
                            t2i_seed = gr.Number(label="Seed", value=42, precision=0)
                            t2i_random_seed = gr.Checkbox(label="Random Seed", value=True)

                        t2i_generate_btn = gr.Button("Generate", variant="primary", size="lg")

                        gr.Markdown("### Example Prompts")
                        gr.Examples(
                            examples=EXAMPLE_PROMPTS,
                            inputs=t2i_prompt,
                        )

                    with gr.Column(scale=1):
                        t2i_output_image = gr.Image(label="Generated Image", type="pil", height=512)
                        t2i_output_seed = gr.Number(label="Seed Used", interactive=False)

                t2i_generate_btn.click(
                    fn=generate_txt2img,
                    inputs=[t2i_prompt, t2i_resolution, t2i_num_steps, t2i_seed, t2i_random_seed, t2i_shift],
                    outputs=[t2i_output_image, t2i_output_seed],
                )

            # Image-to-Image Tab
            with gr.TabItem("Image to Image"):
                with gr.Row():
                    with gr.Column(scale=1):
                        i2i_input_image = gr.Image(
                            label="Input Image",
                            type="pil",
                            height=300,
                        )

                        i2i_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="Describe what you want to generate based on the input image...",
                            lines=3,
                        )

                        i2i_denoise = gr.Slider(
                            label="Denoise Strength",
                            minimum=0.1,
                            maximum=1.0,
                            value=0.7,
                            step=0.05,
                            info="Higher = more changes, Lower = closer to original",
                        )

                        with gr.Row():
                            i2i_num_steps = gr.Slider(
                                label="Inference Steps",
                                minimum=1,
                                maximum=20,
                                value=8,
                                step=1,
                            )
                            i2i_shift = gr.Slider(
                                label="Time Shift",
                                minimum=1.0,
                                maximum=10.0,
                                value=3.0,
                                step=0.1,
                            )

                        with gr.Row():
                            i2i_seed = gr.Number(label="Seed", value=42, precision=0)
                            i2i_random_seed = gr.Checkbox(label="Random Seed", value=True)

                        i2i_generate_btn = gr.Button("Generate", variant="primary", size="lg")

                        gr.Markdown("""
### Tips for Image-to-Image
- **Denoise 0.1-0.3**: Subtle enhancements, keeps original structure
- **Denoise 0.4-0.6**: Moderate changes, balanced transformation
- **Denoise 0.7-1.0**: Creative changes, more deviation from original
                        """)

                    with gr.Column(scale=1):
                        i2i_output_image = gr.Image(label="Generated Image", type="pil", height=512)
                        i2i_output_seed = gr.Number(label="Seed Used", interactive=False)

                i2i_generate_btn.click(
                    fn=generate_img2img,
                    inputs=[
                        i2i_prompt,
                        i2i_input_image,
                        i2i_denoise,
                        i2i_num_steps,
                        i2i_seed,
                        i2i_random_seed,
                        i2i_shift,
                    ],
                    outputs=[i2i_output_image, i2i_output_seed],
                )

    return demo


# =============================================================================
# Main Entry Point
# =============================================================================
def main():
    """Main entry point for the Gradio app."""
    # Load models
    pipe, vae = load_pipeline()

    # Create UI
    demo = create_ui(pipe, vae)

    # Authentication setup
    auth_user = os.getenv("GRADIO_USER")
    auth_pass = os.getenv("GRADIO_PASS")

    def authenticate(username, password):
        """Custom auth function that properly handles session for uploads."""
        if auth_user and auth_pass:
            return username == auth_user and password == auth_pass
        return True

    # Launch
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "8000"))
    secret_key = os.getenv("GRADIO_SECRET_KEY")

    if secret_key:
        print("Starting with persistent session storage (secret_key provided)")
        app = FastAPI()
        # Note: We rely on Gradio to add SessionMiddleware internally using the GRADIO_SECRET_KEY env var
        
        auth_dependency = authenticate if (auth_user and auth_pass) else None

        app = gr.mount_gradio_app(
            app,
            demo,
            path="/",
            auth=auth_dependency,
            auth_message="Please login to access Z-Image-Turbo" if auth_dependency else None
        )
        
        if auth_user and auth_pass:
            print(f"Authentication enabled for user: {auth_user}")
        else:
            print("Warning: No authentication configured. Set GRADIO_USER and GRADIO_PASS for security.")

        uvicorn.run(app, host=server_name, port=server_port, proxy_headers=True, forwarded_allow_ips="*")
    elif auth_user and auth_pass:
        print(f"Authentication enabled for user: {auth_user}")
        demo.launch(
            server_name=server_name,
            server_port=server_port,
            auth=authenticate,
            auth_message="Please login to access Z-Image-Turbo",
            theme=gr.themes.Soft(),
        )
    else:
        print("Warning: No authentication configured. Set GRADIO_USER and GRADIO_PASS for security.")
        demo.launch(server_name=server_name, server_port=server_port, theme=gr.themes.Soft())


if __name__ == "__main__":
    main()
