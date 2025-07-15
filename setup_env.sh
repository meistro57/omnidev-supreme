#!/bin/bash
# OmniDev Supreme Environment Setup Script
# Quick setup for testing - DO NOT USE IN PRODUCTION

echo "🚀 Setting up OmniDev Supreme environment..."

# TODO: Replace with your actual API keys
export OPENAI_API_KEY="your-openai-api-key-here"
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# Optional: Ollama configuration
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_ENABLED="true"

# Python environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✅ Environment variables set:"
echo "   - OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."
echo "   - ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:10}..."
echo "   - OLLAMA_HOST: ${OLLAMA_HOST}"
echo "   - PYTHONPATH: ${PYTHONPATH}"

echo ""
echo "🔧 To use these variables, run:"
echo "   source ./setup_env.sh"
echo ""
echo "⚠️  IMPORTANT: This is for testing only!"
echo "   - Replace with your actual API keys"
echo "   - Never commit real keys to version control"
echo "   - Use proper secrets management in production"
echo ""
echo "🚀 Ready to start OmniDev Supreme!"
echo "   python -m backend.main"
