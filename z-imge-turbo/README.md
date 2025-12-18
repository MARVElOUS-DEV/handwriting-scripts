# 🚀 Quick Start - Modal Development

## 📋 Available Commands

### 🧪 Test img2img (Quick Debug)
```bash
modal run main.py::test
```
This runs a focused test of the img2img function with detailed logging.

### 🔥 Development Mode (Hot Reload)
```bash
modal serve main.py
```
- Watches for file changes
- Auto-reloads when you save `gradio_app.py` or `main.py`
- Shows live logs
- **Best for iterative development!**

### 🚀 Production Deploy
```bash
modal deploy main.py
```
Deploys a stable version that doesn't auto-reload.

### 🐚 Interactive Shell
```bash
modal shell main.py
```
Drop into a shell inside the container for manual testing.

---

## 🔄 Recommended Workflow

### For Quick Bug Fixes:

1. **Test first to confirm the bug**:
   ```bash
   modal run main.py::test
   ```

2. **Start dev mode**:
   ```bash
   modal serve main.py
   ```

3. **Edit `gradio_app.py`** in your editor

4. **Save** → Modal rebuilds automatically (10-30s)

5. **Check logs** in the terminal to see if the issue is fixed

6. **Repeat steps 3-5** until bug is fixed

7. **Test again**:
   ```bash
   # Open a new terminal
   modal run main.py::test
   ```

8. **Deploy when stable**:
   ```bash
   modal deploy main.py
   ```

---

## 🐛 Debugging Tips

### View detailed logs:
```bash
modal run main.py::test
```
This test function has extensive logging at each step.

### Add your own debug prints:
```python
# In gradio_app.py
print(f"🔍 DEBUG: latents.shape = {latents.shape}, dtype = {latents.dtype}")
```

### Test locally first (if possible):
```bash
# Run gradio_app.py directly if you have GPU
python gradio_app.py
```

---

## 📊 Current Status

Your `main.py` now has:
- ✅ `test_img2img()` - Isolated test function
- ✅ `main.py::test` - Entrypoint to run the test
- ✅ Hot reload support with `modal serve`

---

## 💡 Next Steps

1. Run the test to verify the current state:
   ```bash
   modal run main.py::test
   ```

2. If it fails, start dev mode and iterate:
   ```bash
   modal serve main.py
   ```

3. Make changes to `gradio_app.py` and watch logs

4. Once working, deploy:
   ```bash
   modal deploy main.py
   ```
