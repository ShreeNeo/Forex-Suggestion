#!/bin/bash

# Setup script for XAU/USD Forex Trading Assistant
# This script sets up the environment and installs dependencies

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     XAU/USD Forex Trading Assistant - Setup Script            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Make main script executable
echo "🔧 Making main script executable..."
chmod +x forex_trader.py

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! ✅                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python forex_trader.py"
echo ""
echo "  3. (Optional) Configure API keys in config.json"
echo ""
echo "📖 For more information, see README.md"
echo ""
