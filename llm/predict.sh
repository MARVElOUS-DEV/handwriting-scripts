#!/bin/bash

env

if [[ "${ENABLE_AISPACE_RDMA}" == "open" ]]; then
    export NCCL_IB_DISABLE=0
else
    export NCCL_IB_DISABLE=1
fi

export NCCL_NVLS_ENABLE=0

# export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32

# export CUDA_VISIBLE_DEVICES=0

# export MODEL_TYPE=chatglm3
# export BASE_MODEL_PATH=/llm/chatglm3-6b
# export SERVICE_PORT=6008
# export QUANTIZATION_BIT=4
# export AISPACE_PREDICT_TEMPLATE_CONFIG="{\"default_system\":\"1242321321321\"}"

python3 predict.py
