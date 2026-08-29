#!/bin/bash

HOST="0.0.0.0"
PORT="8000"

echo "Starting vLLM server on $HOST:$PORT"

vllm serve /scratch/common_models/Qwen3-8B \
	--host "$HOST" \
	--port "$PORT" \
	--enable-auto-tool-choice \
	--tool-call-parser hermes \
	--reasoning-parser qwen3 

echo "Started vLLM server on $HOST:$PORT"


