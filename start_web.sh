#!/bin/bash

# Start the web UI for XAU/USD Forex Trading Assistant

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     XAU/USD Forex Trading Assistant - Web Dashboard           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment not activated. Activating..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "❌ Virtual environment not found. Please run ./setup.sh first"
        exit 1
    fi
fi

echo "🚀 Starting web dashboard..."
echo "📊 Dashboard will open in your browser"
echo "🔄 To stop, press Ctrl+C"
echo ""

# Start streamlit
streamlit run web_ui.py --server.port 8501 --server.address localhost

echo ""
echo "✅ Dashboard stopped."
