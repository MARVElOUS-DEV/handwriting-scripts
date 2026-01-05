from typing import List, Optional, Dict
import modal
import os
import subprocess
from pathlib import Path


def get_base_image(
    python_version: str = "3.12",
    pip_packages: Optional[List[str]] = None,
    extra_env: Optional[Dict[str, str]] = None,
) -> modal.Image:
    """
    Creates a base Modal image with common configuration.

    Args:
        python_version: Python version to use.
        pip_packages: List of additional pip packages to install.
        extra_env: Dictionary of environment variables to set.

    Returns:
        Configured modal.Image
    """
    base_packages = [
        "torch>=2.4.0",
        "torchvision>=0.19.0",
        "diffusers>=0.33.0",
        "transformers>=4.47.0",
        "accelerate>=1.2.0",
        "safetensors>=0.4.0",
        "sentencepiece>=0.2.0",
        "huggingface_hub[hf_transfer]>=0.27.0",
        "fastapi[standard]>=0.115.0",
        "pillow>=10.0.0",
        "uvicorn",
        "numpy",
    ]

    if pip_packages:
        base_packages.extend(pip_packages)

    image = (
        modal.Image.debian_slim(python_version=python_version)
        .apt_install("git", "wget", "curl")
        .pip_install(*base_packages)
    )

    env_vars = {"HF_HUB_ENABLE_HF_TRANSFER": "1"}
    if extra_env:
        env_vars.update(extra_env)

    image = image.env(env_vars)
    return image


def get_hf_secret(secret_name: str = "huggingface-secret") -> Optional[modal.Secret]:
    """
    Safely retrieves the HuggingFace secret.
    """
    try:
        return modal.Secret.from_name(secret_name)
    except modal.exception.NotFoundError:
        print(f"⚠️ Warning: Secret '{secret_name}' not found.")
        return None


def get_model_cache_volume(name: str = "model-cache-vol") -> modal.Volume:
    """
    Gets or creates a Modal Volume for model caching.
    """
    return modal.Volume.from_name(name, create_if_missing=True)


def download_hf_model_file(
    repo_id: str,
    filename: str,
    target_dir: str,
    token: Optional[str] = None,
    cache_dir: str = "/cache",
) -> str:
    """
    Downloads a single file from HuggingFace using hf_hub_download.
    Handles caching and symlinking to target directory.
    """
    from huggingface_hub import hf_hub_download

    print(f"📥 Downloading {filename} from {repo_id}...")

    cached_path = hf_hub_download(
        repo_id=repo_id, filename=filename, cache_dir=cache_dir, token=token
    )

    # Create target directory
    target_path = Path(target_dir) / Path(filename).name
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Create symlink
    if target_path.exists():
        if target_path.is_symlink():
            target_path.unlink()
        else:
            # If it's a real file, keep it or warn? For now, we assume we want the symlink
            pass

    subprocess.run(f"ln -sf {cached_path} {target_path}", shell=True, check=True)
    print(f"   ✅ Installed at {target_path}")

    return str(target_path)
