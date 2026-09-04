#!/bin/bash

HOST="0.0.0.0"
PORT="11434"

echo "Starting vLLM server on $HOST:$PORT"

vllm serve /scratch/common_models/Qwen3-Embedding-0.6B \
	--host "$HOST" \
	--port "$PORT" \
	--quantization fp8 \
	--gpu-memory-utilization 0.70 

echo "Started vLLM server on $HOST:$PORT"


