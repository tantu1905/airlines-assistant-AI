#!/bin/bash

# Gerekli sistem bağımlılıklarını yükleyin
apt-get update
apt-get install -y portaudio19-dev

# Python bağımlılıklarını yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
uvicorn main:app --host 0.0.0.0 --port 8000