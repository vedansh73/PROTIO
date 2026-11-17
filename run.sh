#!/bin/bash
echo "=========================================="
echo "      SETTING UP & STARTING PROTIO        "
echo "=========================================="
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 is not installed. Please install Python3 first."
    exit 1
fi
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment (venv)..."
    python3 -m venv venv
fi
echo "[*] Activating virtual environment..."
source venv/bin/activate
echo "[*] Installing required dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "[+] Setup complete! Starting PROTIO Suite..."
echo "=========================================="
python3 scanner.py
