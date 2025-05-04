#!/bin/bash

tmux new-session -d -s api 
tmux send-keys -t api "echo '[Run App] Created new session called api'" Enter

tmux send-keys -t api "python3 -m venv venv" Enter
tmux send-keys -t api "echo '[Run App] Created new virtual environment called venv'" Enter
tmux send-keys -t api "source venv/bin/activate" Enter
tmux send-keys -t api "echo '[Run App] Activated venv'" Enter

tmux send-keys -t api "echo '[Run App] Installing dependencies...'" Enter
tmux send-keys -t api "pip install -r requirements.txt" Enter
tmux send-keys -t api "echo '[Run App] Dependencies installed'" Enter

tmux send-keys -t api "echo '[Run App] Starting Flask App...'" Enter
tmux send-keys -t api "python3 app.py" Enter

tmux attach -t api
