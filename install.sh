#!/bin/bash

echo "🚀 Starting installation of CES Framework on Kali Linux..."

echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing required system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential libssl-dev libffi-dev python3-dev libxml2 libxml2-dev libxslt1-dev \
    zlib1g-dev libjpeg-dev libpq-dev libbz2-dev libreadline-dev libsqlite3-dev

echo "🔧 Checking and updating pip..."
python3 -m ensurepip
python3 -m pip install --upgrade pip

echo "🛠️ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "📌 Installing additional required Python libraries..."
pip install beautifulsoup4 lxml requests colorama pyyaml tqdm

echo "🛠️ Installing optional pentesting tools..."
sudo apt install -y dirb wfuzz nmap sqlmap

echo "✅ Installation complete!"
echo "🔥 To start CES Framework, run: source venv/bin/activate && python3 CES.py"
