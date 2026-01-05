"""
Qwen-Image-Edit-2511 Gradio Web UI
Standalone script for the Gradio interface.
"""

import os
import random
import traceback
import secrets as py_secrets

import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import gradio as gr
import torch
from PIL import Image

# =============================================================================
# Configuration
# =============================================================================
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
CACHE_DIR = "/cache/models/Qwen-Image-Edit-2511"

EXAMPLE_PROMPTS = [
    "Make the background a sunset beach scene.",
    "Add a cute cat sitting next to the subject.",
    "Transform this into a watercolor painting style.",
    "Remove the background and replace with a starry night sky.",
    "Make the person wear a red hat.",
]


# =============================================================================
# Model Loading
# =============================================================================
def load_pipeline():
    """Load the Qwen-Image-Edit pipeline."""
    from diffusers import QwenImageEditPlusPipeline

    hf_token = os.getenv("HF_TOKEN")

    print("Loading Qwen-Image-Edit model for Gradio UI...")

    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        dtype=torch.float16,# replace bfloat16
        cache_dir=CACHE_DIR,
        token=hf_token,
    )
    # Use CPU offloading to fit model in GPU memory
    # pipe.enable_model_cpu_offload()
    pipe.to("cuda")

    print("Model loaded!")
    return pipe


# =============================================================================
# Generation Function
# =============================================================================
def create_generate_fn(pipe):
    """Create the image editing generation function."""

    def generate(
        image1,
        image2,
        prompt,
        num_inference_steps,
        guidance_scale,
        true_cfg_scale,
        seed,
        random_seed,
    ):
        try:
            if image1 is None:
                raise gr.Error("Please upload an image")
            if not prompt.strip():
                raise gr.Error("Please enter a prompt")

            # Convert to PIL if needed
            if not isinstance(image1, Image.Image):
                image1 = Image.fromarray(image1)
            image1 = image1.convert("RGB")

            # Build image list - single image or dual image mode
            if image2 is not None:
                if not isinstance(image2, Image.Image):
                    image2 = Image.fromarray(image2)
                image2 = image2.convert("RGB")
                images = [image1, image2]
            else:
                images = [image1]

            if random_seed:
                seed = random.randint(1, 1000000)

            generator = torch.manual_seed(int(seed))

            inputs = {
                "image": images,
                "prompt": prompt,
                "generator": generator,
                "true_cfg_scale": true_cfg_scale,
                "negative_prompt": " ",
                "num_inference_steps": int(num_inference_steps),
                "guidance_scale": guidance_scale,
                "num_images_per_prompt": 1,
            }

            with torch.inference_mode():
                output = pipe(**inputs)
                output_image = output.images[0]

            return output_image, int(seed)
        except Exception as e:
            traceback.print_exc()
            if isinstance(e, gr.Error):
                raise e
            raise gr.Error(f"Generation failed: {e}")

    return generate


# =============================================================================
# Gradio UI
# =============================================================================
def create_ui(pipe):
    """Create the Gradio interface."""
    generate_fn = create_generate_fn(pipe)

    with gr.Blocks(title="Qwen-Image-Edit-2511") as demo:
        gr.Markdown("""
# Qwen-Image-Edit-2511

**AI-powered Image Editing by Qwen**

Upload an image and describe how you want it edited. Optionally add a second image for combining/merging.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Input")

                image1_input = gr.Image(
                    label="Image to Edit",
                    type="pil",
                    height=300,
                )

                with gr.Accordion("Add Second Image (Optional)", open=False):
                    image2_input = gr.Image(
                        label="Second Image (for combining/merging)",
                        type="pil",
                        height=200,
                    )

                prompt_input = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe how you want the images combined or edited...",
                    lines=3,
                )

                gr.Markdown("### Generation Settings")

                with gr.Row():
                    num_steps_input = gr.Slider(
                        label="Inference Steps",
                        minimum=10,
                        maximum=100,
                        value=40,
                        step=1,
                    )
                    guidance_scale_input = gr.Slider(
                        label="Guidance Scale",
                        minimum=0.0,
                        maximum=10.0,
                        value=1.0,
                        step=0.1,
                    )

                with gr.Row():
                    true_cfg_scale_input = gr.Slider(
                        label="True CFG Scale",
                        minimum=1.0,
                        maximum=10.0,
                        value=4.0,
                        step=0.1,
                        info="Higher values = stronger prompt adherence",
                    )

                with gr.Row():
                    seed_input = gr.Number(label="Seed", value=42, precision=0)
                    random_seed_input = gr.Checkbox(label="Random Seed", value=True)

                generate_btn = gr.Button("Generate", variant="primary", size="lg")

                gr.Markdown("### Example Prompts")
                gr.Examples(
                    examples=[[p] for p in EXAMPLE_PROMPTS],
                    inputs=prompt_input,
                )

            with gr.Column(scale=1):
                gr.Markdown("### Output")
                output_image = gr.Image(label="Generated Image", type="pil", height=512)
                output_seed = gr.Number(label="Seed Used", interactive=False)

                gr.Markdown("""
### Tips
- **Image to Edit**: Upload the main image you want to modify
- **Second Image (Optional)**: Add a second image if you want to combine/merge elements
- **Prompt**: Describe the desired edit or transformation
- **Inference Steps**: More steps = better quality but slower (40 recommended)
- **True CFG Scale**: Higher = stronger adherence to prompt (4.0 is default)
                """)

        generate_btn.click(
            fn=generate_fn,
            inputs=[
                image1_input,
                image2_input,
                prompt_input,
                num_steps_input,
                guidance_scale_input,
                true_cfg_scale_input,
                seed_input,
                random_seed_input,
            ],
            outputs=[output_image, output_seed],
        )

    return demo


# =============================================================================
# Main Entry Point
# =============================================================================
def main():
    """Main entry point for the Gradio app."""
    # Load models
    pipe = load_pipeline()

    # Create UI
    demo = create_ui(pipe)

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

    # Always use FastAPI with proper session middleware for file uploads and auth
    app = FastAPI()

    # Add session middleware for persistent sessions (required for file uploads)
    if secret_key:
        print("Persistent session storage enabled (secret_key provided)")
        app.add_middleware(
            SessionMiddleware,
            secret_key=secret_key,
            max_age=86400,  # 24 hours
            same_site="lax",
            https_only=False,  # Set to True in production with HTTPS
        )
    else:
        print("Using temporary session storage (no secret_key)")
        # Use a temporary key for this session only
        temp_key = py_secrets.token_hex(32)
        app.add_middleware(
            SessionMiddleware,
            secret_key=temp_key,
            max_age=3600,  # 1 hour for temporary sessions
            same_site="lax",
            https_only=False,
        )

    # Setup authentication
    auth_dependency = authenticate if (auth_user and auth_pass) else None

    # Mount Gradio app
    app = gr.mount_gradio_app(
        app,
        demo,
        path="/",
        auth=auth_dependency,
        auth_message="Please login to access Qwen-Image-Edit"
        if auth_dependency
        else None,
    )

    # Status messages
    if auth_user and auth_pass:
        print(f"Authentication enabled for user: {auth_user}")
    else:
        print(
            "No authentication configured. Set GRADIO_USER and GRADIO_PASS for security."
        )

    # Run server
    uvicorn.run(
        app,
        host=server_name,
        port=server_port,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
