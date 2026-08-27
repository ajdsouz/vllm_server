#!/bin/bash

source .venv/bin/activate

export CUDA_VISIBLE_DEVICES=0
echo "Using CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

nvidia-smi

uv pip list

bash init_server.sh & 
SERVER_PID=$!

until curl -s http://localhost:8000/v1/models | grep -q "id"; do
	echo "Waiting for model to load..."
	sleep 2
done

echo "Model is loaded"
echo "Server started on $(hostname)"
echo "Server PID: $SERVER_PID"

wait $SERVER_PID
