# Development Setup

Complete guide to setting up a development environment for OmniDev Supreme. This comprehensive setup will prepare you for contributing to the platform that orchestrates 29 AI agents.

## 🎯 Prerequisites

### **System Requirements**
- **Operating System**: Linux, macOS, or Windows (with WSL2 recommended)
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 10GB free space for dependencies and data
- **Network**: Stable internet connection for AI model API calls

### **Required Software**

#### **1. Python Environment**
```bash
# Python 3.11 or higher
python3 --version  # Should be 3.11+

# Install pyenv for Python version management (optional but recommended)
curl https://pyenv.run | bash

# Install Python 3.11 with pyenv
pyenv install 3.11.7
pyenv global 3.11.7
```

#### **2. Node.js Environment**
```bash
# Node.js 18 or higher
node --version  # Should be 18+

# Install nvm for Node.js version management (optional but recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 18 with nvm
nvm install 18
nvm use 18
```

#### **3. Git and Development Tools**
```bash
# Git for version control
git --version

# curl for API testing
curl --version

# Docker (optional for containerized development)
docker --version
docker-compose --version
```

## 🚀 Environment Setup

### **1. Clone the Repository**
```bash
# Clone the main repository
git clone https://github.com/meistro57/omnidev-supreme.git
cd omnidev-supreme

# Verify the repository structure
ls -la
```

### **2. Quick Setup Script**
```bash
# Run the quick setup script
chmod +x setup_env.sh
./setup_env.sh

# This script will:
# - Create virtual environment
# - Install Python dependencies
# - Set up environment variables
# - Install frontend dependencies
# - Create necessary directories
```

### **3. Manual Setup (Alternative)**

#### **Python Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### **Frontend Dependencies**
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Install development dependencies
npm install --only=dev

# Return to root directory
cd ..
```

### **4. Environment Variables**
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```

#### **Environment Configuration**
```bash
# === API Keys ===
# OpenAI API Key (required for most agents)
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic API Key (required for Claude integration)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# === Database Configuration ===
# SQLite database path
DATABASE_URL=sqlite:///./omnidev_supreme.db

# Redis configuration (optional for production)
REDIS_URL=redis://localhost:6379
REDIS_ENABLED=false

# === Ollama Configuration (optional) ===
# Local model hosting
OLLAMA_HOST=http://localhost:11434
OLLAMA_ENABLED=false

# === Development Settings ===
# Debug mode
DEBUG=true
LOG_LEVEL=DEBUG

# FastAPI settings
API_HOST=0.0.0.0
API_PORT=8000

# Frontend settings
FRONTEND_HOST=localhost
FRONTEND_PORT=3000

# === Security Settings ===
# JWT secret key (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# === Agent Configuration ===
# Maximum concurrent tasks per agent
MAX_CONCURRENT_TASKS=3

# Default task timeout in seconds
DEFAULT_TASK_TIMEOUT=300

# === Memory Configuration ===
# Vector database settings
VECTOR_DB_PATH=./data/vector_db
MAX_VECTOR_ENTRIES=100000

# Relational database settings
MAX_RELATIONAL_ENTRIES=50000

# Session timeout in seconds
SESSION_TIMEOUT=3600
```

## 🔧 Development Tools

### **1. Code Quality Tools**
```bash
# Install development tools
pip install black flake8 mypy pytest pytest-asyncio pytest-cov

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Set up code formatting
black --check .
flake8 .
mypy backend/
```

### **2. Database Tools**
```bash
# Install database utilities
pip install alembic sqlalchemy-utils

# Initialize database
python -c "
from backend.database import init_db
import asyncio
asyncio.run(init_db())
"

# Run database migrations
alembic upgrade head
```

### **3. Testing Tools**
```bash
# Run backend tests
pytest backend/tests/ -v

# Run frontend tests
cd frontend
npm test

# Run integration tests
pytest tests/integration/ -v

# Generate coverage report
pytest --cov=backend --cov-report=html
```

## 📊 IDE Configuration

### **1. Visual Studio Code**
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["backend/tests"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/node_modules": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "eslint.workingDirectories": ["frontend"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["backend/tests/", "-v"],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

### **2. PyCharm**
1. **Open Project**: File → Open → Select omnidev-supreme directory
2. **Python Interpreter**: Settings → Project → Python Interpreter → Add → Existing environment → Select `venv/bin/python`
3. **Code Style**: Settings → Editor → Code Style → Python → Set to Black
4. **Run Configuration**: Run → Edit Configurations → Add Python configuration with module `uvicorn` and parameters `backend.main:app --reload`

### **3. Frontend IDE Setup**
For frontend development, configure TypeScript and React settings:

```json
// .vscode/settings.json (additional settings)
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "emmet.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  },
  "files.associations": {
    "*.tsx": "typescriptreact"
  }
}
```

## 🏃 Running the Development Environment

### **1. Start Backend Services**
```bash
# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server
python -m backend.main

# Alternative with uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# The backend will be available at http://localhost:8000
```

### **2. Start Frontend Development**
```bash
# In a new terminal, navigate to frontend
cd frontend

# Start the development server
npm run dev

# The frontend will be available at http://localhost:3000
```

### **3. Start Additional Services (Optional)**

#### **Redis (for production-like environment)**
```bash
# Install Redis
# On macOS: brew install redis
# On Ubuntu: sudo apt-get install redis-server

# Start Redis
redis-server

# Test Redis connection
redis-cli ping  # Should return PONG
```

#### **Ollama (for local AI models)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Install a model
ollama pull llama2

# Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello, world!"
}'
```

## 🧪 Development Workflow

### **1. Daily Development Routine**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install/update dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 4. Run tests
pytest backend/tests/ -v
cd frontend && npm test && cd ..

# 5. Start development servers
# Terminal 1: Backend
python -m backend.main

# Terminal 2: Frontend
cd frontend && npm run dev
```

### **2. Code Quality Checks**
```bash
# Format code
black backend/
cd frontend && npm run format

# Lint code
flake8 backend/
cd frontend && npm run lint

# Type checking
mypy backend/
cd frontend && npm run type-check

# Run all checks
./scripts/check_code_quality.sh
```

### **3. Testing Workflow**
```bash
# Run unit tests
pytest backend/tests/unit/ -v

# Run integration tests
pytest backend/tests/integration/ -v

# Run frontend tests
cd frontend && npm test

# Run end-to-end tests
pytest tests/e2e/ -v

# Generate coverage report
pytest --cov=backend --cov-report=html
```

## 🛠️ Debugging Guide

### **1. Backend Debugging**
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debugger
python -m debugpy --listen 5678 --wait-for-client -m backend.main

# Or use pdb for interactive debugging
python -m pdb -m backend.main
```

### **2. Frontend Debugging**
```bash
# Start with debugging enabled
cd frontend
npm run dev

# Chrome DevTools
# Open http://localhost:3000 in Chrome
# Press F12 to open DevTools
# Use Console, Network, and Sources tabs
```

### **3. Agent Debugging**
```python
# Add debugging to agent code
import logging

logger = logging.getLogger(__name__)

class YourAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Agent {self.metadata.name} executing task: {task}")
        
        try:
            # Your agent logic here
            result = await self.process_task(task)
            logger.info(f"Agent {self.metadata.name} completed task successfully")
            return result
        except Exception as e:
            logger.error(f"Agent {self.metadata.name} failed: {e}", exc_info=True)
            raise
```

## 📋 Common Development Tasks

### **1. Adding a New Agent**
```bash
# 1. Create agent file
touch backend/agents/your_system/your_agent.py

# 2. Implement agent class
# (See agent development guide)

# 3. Add to integration manager
# Edit backend/agents/integration_manager.py

# 4. Add tests
touch backend/tests/agents/test_your_agent.py

# 5. Update documentation
# Edit relevant wiki pages
```

### **2. Database Schema Changes**
```bash
# 1. Edit models in backend/database/models.py

# 2. Create migration
alembic revision --autogenerate -m "Description of changes"

# 3. Review migration file
# Edit alembic/versions/xxx_description.py if needed

# 4. Apply migration
alembic upgrade head

# 5. Test migration
pytest backend/tests/database/
```

### **3. Frontend Component Development**
```bash
# 1. Create component
mkdir frontend/src/components/YourComponent
touch frontend/src/components/YourComponent/YourComponent.tsx
touch frontend/src/components/YourComponent/YourComponent.module.css

# 2. Implement component
# (See frontend development guide)

# 3. Add to storybook
touch frontend/src/components/YourComponent/YourComponent.stories.tsx

# 4. Add tests
touch frontend/src/components/YourComponent/YourComponent.test.tsx

# 5. Export component
# Edit frontend/src/components/index.ts
```

## 🚨 Troubleshooting

### **1. Common Issues**

#### **Python Version Issues**
```bash
# Check Python version
python --version

# If wrong version, use pyenv
pyenv install 3.11.7
pyenv local 3.11.7
```

#### **Permission Issues**
```bash
# Fix pip permissions
pip install --user -r requirements.txt

# Fix npm permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

#### **Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

#### **Database Issues**
```bash
# Reset database
rm omnidev_supreme.db
alembic upgrade head

# Reset migrations
rm alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### **2. Performance Issues**
```bash
# Profile Python code
pip install py-spy
py-spy record -o profile.svg -- python -m backend.main

# Monitor memory usage
pip install memory-profiler
python -m memory_profiler backend/main.py

# Monitor frontend performance
cd frontend
npm run analyze
```

### **3. Getting Help**
- **Documentation**: Check the wiki for detailed guides
- **GitHub Issues**: Search existing issues or create new ones
- **Discord**: Join the community for real-time help
- **Stack Overflow**: Use tags `omnidev-supreme`, `ai-agents`

## 🎯 Next Steps

After completing the development setup:

1. **[Backend Development](backend.md)** - Deep dive into backend architecture
2. **[Frontend Development](frontend.md)** - Learn the React/TypeScript frontend
3. **[Testing Guide](testing.md)** - Comprehensive testing strategies
4. **[Agent Development](../agents/agent-development.md)** - Create custom agents
5. **[Contributing Guide](../contributing/guide.md)** - How to contribute to the project

## 📊 Development Environment Health Check

Run this script to verify your development environment:

```bash
#!/bin/bash
# Development environment health check

echo "🔍 Checking development environment..."

# Check Python
python --version && echo "✅ Python OK" || echo "❌ Python not found"

# Check Node.js
node --version && echo "✅ Node.js OK" || echo "❌ Node.js not found"

# Check virtual environment
source venv/bin/activate && echo "✅ Virtual environment OK" || echo "❌ Virtual environment not found"

# Check Python dependencies
pip check && echo "✅ Python dependencies OK" || echo "❌ Python dependencies issues"

# Check frontend dependencies
cd frontend && npm ls --depth=0 && echo "✅ Frontend dependencies OK" || echo "❌ Frontend dependencies issues"

# Check database
python -c "from backend.database import test_connection; test_connection()" && echo "✅ Database OK" || echo "❌ Database issues"

# Check API keys
python -c "import os; print('✅ OpenAI API key set' if os.getenv('OPENAI_API_KEY') else '⚠️ OpenAI API key not set')"
python -c "import os; print('✅ Anthropic API key set' if os.getenv('ANTHROPIC_API_KEY') else '⚠️ Anthropic API key not set')"

echo "🎉 Development environment check complete!"
```

---

<div align="center">
  <p><strong>🛠️ Development environment ready for building the future!</strong></p>
  <p>You're now equipped to contribute to the 29-agent AI platform.</p>
  
  <a href="backend.md">
    <strong>Start Backend Development →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/development/setup.md)*