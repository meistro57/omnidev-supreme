#!/bin/bash
# OmniDev Supreme Quick Start Script

echo "🚀 Starting OmniDev Supreme - The One Platform to Rule Them All!"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using setup_env.sh for testing..."
    echo "   For production, copy .env.example to .env and configure properly"
    echo ""
    
    # Source the setup script
    source ./setup_env.sh
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-your-openai-key-here" ]; then
    echo "⚠️  WARNING: OpenAI API key not set or using placeholder"
    echo "   Please set your actual API key in setup_env.sh or .env"
fi

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-your-anthropic-key-here" ]; then
    echo "⚠️  WARNING: Anthropic API key not set or using placeholder"
    echo "   Please set your actual API key in setup_env.sh or .env"
fi

echo ""
echo "🎯 Starting OmniDev Supreme server..."
echo "   API Documentation: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""

# Start the server
python -m backend.main