@echo off

echo "Simple websockets clients generator"
if exist .\venv\ (
    echo "Virtual env is already created"
) else (
    echo "Creating virtual env..."
    python -m venv .\venv
    echo "Installing all dependencies"
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
)
echo "run the code...."
.\venv\Scripts\python.exe client_websocket.py
