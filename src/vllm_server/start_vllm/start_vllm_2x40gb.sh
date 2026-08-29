#!/bin/bash

source .venv/bin/activate

#automatically rename gpus
source rename_gpus.sh

echo "Using CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

# print gpu info to logs
nvidia-smi

uv pip list

#server start and run in background
bash src/vllm_server/init_server/init_server_2x40gb.sh & 
SERVER_PID=$!

#ping endpoint every 20 seconds until it returns status 200
until curl -s http://localhost:8000/v1/models | grep -q "id"; do
	echo "Waiting for model to load..."
	sleep 20
done

echo "Model is loaded"
echo "Server started on $(hostname)"
echo "Server PID: $SERVER_PID"

#keep server running until the script is terminated
wait $SERVER_PID
