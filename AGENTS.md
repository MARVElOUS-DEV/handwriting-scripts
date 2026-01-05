# Agent Operational Guidelines

## 1. Repository Context
This is a multi-purpose repository containing:
- **`common-code/`**: JavaScript algorithmic solutions (LeetCode, handwriting, data structures).
- **`llm/`**: LLM fine-tuning and inference framework (Python).
- **`z-imge-turbo/` & `Qwen-Image-Edit-2511/`**: Modal-based AI applications.
- **`ddddocr/`**: OCR related Python code.

## 2. Build, Test, and Lint Commands

### Python Projects
- **Package Management**: 
  - `z-imge-turbo` & `Qwen-Image-Edit-2511` use `uv`. Look for `uv.lock`.
  - Others use standard `requirements.txt`.
- **Running Tests**:
  - **Modal Apps (`z-imge-turbo`, `Qwen...`)**:
    ```bash
    modal run main.py::test  # Run specific test entrypoint
    ```
  - **LLM Project**:
    - No central test runner. Check `evaluate.py` or specific script entry points.
    - Usage: `python llm/evaluate.py ...`

### JavaScript (`common-code`)
- **Running Files**: 
  - Scripts are standalone. Run directly with Node.js:
    ```bash
    node common-code/path/to/file.js
    ```
- **Testing**:
  - Verification is done via `console.log` calls at the bottom of files.
  - **Action**: When modifying, add a `console.log` case to verify your change, run it, then remove/comment it if it clutters.

## 3. Code Style & Conventions

### Python (General)
- **Style**: Follow PEP 8.
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes.
- **Type Hints**: **MANDATORY** for `llm/` and new architectural code.
  - Use `typing` (List, Dict, Optional, etc.).
  - Example: `def chat(self, messages: List[Dict[str, str]]) -> Response:`
- **Imports**: 
  - Sort imports: Standard lib -> Third party -> Local.
  - Use `if TYPE_CHECKING:` to avoid circular imports.
- **Error Handling**: Use specific `try-except` blocks. Avoid bare `except:`.

### JavaScript (`common-code`)
- **Style**: Algorithmic / LeetCode style.
- **Naming**: `camelCase` for functions and variables.
- **Documentation**: Use JSDoc for function headers.
  ```javascript
  /**
   * @param {string} digits
   * @return {string[]}
   */
  ```
- **Formatting**: 4-space indentation is common in this directory.

## 4. Workflow Rules
- **Dependencies**: 
  - Do not add new dependencies without explicit instruction.
  - If working in `z-imge-turbo`, use `uv add <package>` if permitted.
- **Refactoring**: 
  - In `common-code`, focus on readability and algorithmic efficiency.
  - In `llm/`, maintain strict typing and modularity.
- **Safety**: 
  - Never commit API keys or credentials.
  - Avoid modifying `common-code` logic unless fixing a bug or requested optimization.

## 5. Specific directory instructions

### `llm/`
- This is a complex module. Respect the `Engine` -> `Model` -> `UI` architecture.
- Async `await/async` is heavily used. Ensure event loops are handled correctly.

### `z-imge-turbo/` & `Qwen-Image-Edit-2511/`
- Designed for **Modal.com**.
- Development Loop:
  1. `modal run main.py::test` (Debug)
  2. `modal serve main.py` (Dev)
  3. `modal deploy main.py` (Prod)
