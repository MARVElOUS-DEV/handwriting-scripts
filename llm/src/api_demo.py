import os

import uvicorn

from llmtuner import ChatModel, create_app


def main():
    chat_model = ChatModel()
    app = create_app(chat_model)
    print("Visit http://localhost:{}/docs for API document.".format(os.environ.get("API_PORT", 8000)))
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("API_PORT", 8000)), workers=1)


if __name__ == "__main__":

    import sys
    sys.argv.append("--template=qwen")
    sys.argv.append("--model_name_or_path=/Users/developer/Workspace/Models/20240314/Qwen1.5-0.5B-Chat")

    main()
