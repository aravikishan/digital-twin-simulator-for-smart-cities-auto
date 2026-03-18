#!/bin/bash
set -e
echo "Starting Digital Twin Simulator for Smart Cities..."
uvicorn app:app --host 0.0.0.0 --port 9015 --workers 1
