#!/bin/bash

MODEL_PATH=$1
HOST="127.0.0.1"
PORT="8000"
vllm serve /scratch/common_models/Qwen3-8B \
	--host "$HOST" \
	--port "$PORT" \
	--enable-reasoning \
	--reasoning-parser deepseek_r1 
