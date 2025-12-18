# Debugging Modal Apps - Quick Guide

## 🔥 Method 1: Modal Serve (Hot Reload - BEST for Development)

**Automatically reloads when you change code!**

```bash
# Run in development mode with hot reload
modal serve main.py
```

This will:
- ✅ Start your app
- ✅ Watch for file changes
- ✅ Automatically reload when you save changes to `gradio_app.py` or `main.py`
- ✅ Show logs in your terminal

**Note**: The container needs to rebuild when code changes, so there's a ~10-30s delay.

---

## 🐚 Method 2: Interactive Shell (Best for Testing)

Drop into a shell inside the Modal container:

```bash
# Shell into the container
modal shell main.py

# Inside the container, you can:
python /app/gradio_app.py  # Run your app manually
python -c "import torch; print(torch.cuda.is_available())"  # Test CUDA
# etc.
```

---

## 🧪 Method 3: Local Testing Function

Add a test function to `main.py`:

```python
@app.function(
    gpu="L40S",
    volumes={"/cache": vol},
    secrets=_ui_secrets,
    timeout=600,
)
def test_img2img():
    """Test img2img generation"""
    import sys
    sys.path.insert(0, '/app')
    
    from gradio_app import load_pipeline, create_generate_img2img
    from PIL import Image
    
    # Load models
    pipe, vae = load_pipeline()
    
    # Create generator
    generate_img2img = create_generate_img2img(pipe, vae)
    
    # Test with a sample image
    test_image = Image.new('RGB', (512, 512), color='red')
    
    try:
        result_image, seed = generate_img2img(
            prompt="a beautiful landscape",
            input_image=test_image,
            denoise_strength=0.7,
            num_steps=8,
            seed=42,
            random_seed=False,
            shift=3.0
        )
        print(f"✅ Success! Seed: {seed}")
        return "SUCCESS"
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return f"FAILED: {e}"

# Run the test
@app.local_entrypoint()
def test():
    result = test_img2img.remote()
    print(f"\nTest Result: {result}")
```

Then run:
```bash
modal run main.py::test
```

---

## 📊 Method 4: Enhanced Logging

Add detailed logging to your code:

```python
# In gradio_app.py, add at the top:
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Then in your functions:
def generate_img2img(...):
    try:
        logger.info(f"Starting img2img with prompt: {prompt[:50]}")
        logger.debug(f"Latents shape: {latents.shape}, dtype: {latents.dtype}")
        # ... rest of code
```

---

## 🔄 Quick Development Workflow

### For rapid iteration:

1. **Start with `modal serve`**:
   ```bash
   modal serve main.py
   ```

2. **Edit `gradio_app.py` in your local editor**

3. **Save the file** → Modal automatically rebuilds (10-30s)

4. **Refresh your browser** to test

5. **Check logs** in the terminal where `modal serve` is running

---

## 🐛 Debugging Specific Issues

### Check GPU availability:
```bash
modal run main.py --gpu "L40S" --cmd "nvidia-smi"
```

### Test model loading:
```bash
modal run main.py --cmd "python -c 'from diffusers import ZImagePipeline; print(ZImagePipeline)'"
```

### Check file contents in container:
```bash
modal shell main.py
# Inside container:
cat /app/gradio_app.py | head -n 50
```

---

## 💡 Pro Tips

1. **Use `print()` liberally** - Modal shows all stdout in logs
2. **Add try/except blocks** with detailed error messages
3. **Test small functions first** before testing the full pipeline
4. **Use `assert` statements** to catch issues early:
   ```python
   assert latents.dtype == torch.float32, f"Wrong dtype: {latents.dtype}"
   ```

---

## 🚀 When Ready for Production

```bash
# Deploy the stable version
modal deploy main.py
```

This creates a persistent endpoint that doesn't auto-reload.
