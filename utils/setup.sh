#!/bin/bash

echo "🔧 Setting up your trading bot environment..."

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python packages..."
pip install flask requests pandas tabulate pandas_ta

# Create audit log file if missing
if [ ! -f audit_log.json ]; then
    echo "🧾 Creating empty audit log..."
    touch audit_log.json
fi

# Launch dashboard
echo "🚀 Launching dashboard at http://localhost:8080"
python dashboard.py
