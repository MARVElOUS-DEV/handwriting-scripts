import io
import os
import sys
from pathlib import Path

import modal

# Add repo root to sys.path to allow importing modal_libs
repo_root = Path(__file__).parent.parent
sys.path.append(str(repo_root))

from modal_libs import get_base_image, get_hf_secret, get_model_cache_volume

# =============================================================================
# S1: Setup Image
# =============================================================================
LOCAL_DIR = Path(__file__).parent

image = (
    get_base_image(
        python_version="3.12", pip_packages=["gradio>=6.0.0", "itsdangerous"]
    )
    .add_local_python_source("modal_libs")
    .add_local_file(LOCAL_DIR / "gradio_app.py", "/app/gradio_app.py")
)

# Secrets & Volumes
hf_secret = get_hf_secret()
gradio_auth_secret = get_hf_secret("gradio-auth")
vol = get_model_cache_volume("qwen-image-edit-cache")

app = modal.App(name="qwen-image-edit", image=image)

MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
# =============================================================================
# S2: Gradio Web UI
# =============================================================================
_ui_secrets = [s for s in [hf_secret, gradio_auth_secret] if s is not None]


@app.function(
    gpu="A100-80GB",
    volumes={"/cache": vol},
    secrets=_ui_secrets,
    timeout=86400,  # Max function runtime: 24 hours
    scaledown_window=600,  # Keep container warm for 10 min after last request
    min_containers=0,  # Keep 0 containers pre-warmed (cost optimization)
    max_containers=1,
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=180)
def ui():
    """Gradio Web UI"""
    import subprocess

    subprocess.Popen(["python", "/app/gradio_app.py"])


@app.local_entrypoint()
def main():
    print("=" * 60)
    print(f"Qwen Image Edit Service ({MODEL_ID})")
    print("=" * 60)
    print("Dev mode:        modal serve main.py")
    print("Deploy:          modal deploy main.py")
    print("\n" + "=" * 60)
