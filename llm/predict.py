import os

# os.environ["MODEL_TYPE"]= "chatglm3"
# os.environ["BASE_MODEL_PATH"]= "/llm/chatglm3-6b"
# os.environ["SERVICE_PORT"]= "6008"
# os.environ["AISPACE_PREDICT_TEMPLATE_CONFIG"]= "{\"default_system\":\"test\"}"


import sys

# sys.path.append('/workspace/src')
sys.path.append('/root/llm/src')

import json
import uvicorn

from llmtuner import ChatModel, create_app


def main():
    chat_model = ChatModel()
    app = create_app(chat_model)
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("SERVICE_PORT", 6000)), workers=1)


def make_config():
    env_to_arg_map = {
        "MODEL_TYPE": "template",
        "BASE_MODEL_PATH": "model_name_or_path",
        "QUANTIZATION_BIT": "quantization_bit"
    }

    config = {
        "template": "default",
        "quantization_bit": -1,
        "infer_backend": "huggingface",
        "vllm_maxlen": 2048,
        "vllm_gpu_util": 0.95,
        "vllm_enforce_eager": True
    }

    user_config = {}

    if os.getenv("AISPACE_PREDICT_CONFIG") is None:
        for env_var, arg in env_to_arg_map.items():
            value = os.environ.get(env_var)
            if value is not None:
                user_config[arg] = value
    else:
        user_config = json.loads(os.getenv("AISPACE_PREDICT_CONFIG"))

    config.update(user_config)

    if os.getenv("AISPACE_PREDICT_CONFIG_EXT") is not None:
        config_ext = json.loads(os.getenv("AISPACE_PREDICT_CONFIG_EXT"))
        config.update(config_ext)

    if config["template"] == "sus":
        config["template"] = "xverse"

    if "quantization_bit" in config and (config["quantization_bit"] != 4 and config["quantization_bit"] != 8 and config["quantization_bit"] != "4" and config["quantization_bit"] != "8"):
        config.pop("quantization_bit", None)

    for key, value in config.items():
        sys.argv.append(f'--{key}={value}')


def add_template():
    from llmtuner.data.template import _register_template
    from llmtuner.data.formatter import StringFormatter

    _register_template(
        name="llama3",
        format_user=StringFormatter(
            slots=[
                (
                    "<|start_header_id|>user<|end_header_id|>\n\n{{content}}<|eot_id|>"
                    "<|start_header_id|>assistant<|end_header_id|>\n\n"
                )
            ]
        ),
        format_system=StringFormatter(
            slots=[{"bos_token"}, "<|start_header_id|>system<|end_header_id|>\n\n{{content}}<|eot_id|>"]
        ),
        format_observation=StringFormatter(
            slots=[
                (
                    "<|start_header_id|>tool<|end_header_id|>\n\n{{content}}<|eot_id|>"
                    "<|start_header_id|>assistant<|end_header_id|>\n\n"
                )
            ]
        ),
        default_system="You are a helpful assistant. If you do not need to use a tool or reply to a fixed data structure (such as json format) separately, please reply in Chinese as much as possible. ",
        stop_words=["<|eot_id|>"],
        replace_eos=True,
    )


def regist_template():

    args_sys = sys.argv[1:]

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', type=str, default='')
    args, other = parser.parse_known_args(args_sys)
    name = args.template

    from llmtuner.data import templates
    template = templates.get(name, None)
    if template is None:
        raise ValueError("Template {} does not exist.".format(name))

    if os.getenv("AISPACE_PREDICT_TEMPLATE_CONFIG") is not None:
        print("======regist_template======")
        templ = json.loads(os.getenv("AISPACE_PREDICT_TEMPLATE_CONFIG"))
        if "default_system" in templ:
            template.default_system = templ["default_system"]

    print(template)


if __name__ == "__main__":
    make_config()
    add_template()
    regist_template()
    main()
