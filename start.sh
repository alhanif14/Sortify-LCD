#!/bin/bash

# Run FastAPI di background
uvicorn app:app --host=0.0.0.0 --port=${PORT} &

# Jalankan script MQTT listener
python routes/mqtt-qr-script.py
