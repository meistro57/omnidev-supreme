# Common Issues & Solutions

Comprehensive troubleshooting guide for OmniDev Supreme. This page covers the most frequently encountered issues and their solutions.

## 🚨 Quick Diagnosis

### **System Health Check**
Before troubleshooting specific issues, run a quick system health check:

```bash
# Check system status
curl http://localhost:8000/health

# Check agent availability
curl http://localhost:8000/agents

# Check frontend connectivity
curl http://localhost:3000

# Check database connection
python -c "from backend.database import test_connection; test_connection()"
```

### **Log Files**
Check these log files for detailed error information:
- **Backend**: `logs/backend.log`
- **Frontend**: Browser console (F12 → Console)
- **Agents**: `logs/agents.log`
- **Database**: `logs/database.log`

## 🔧 Installation & Setup Issues

### **1. Python Environment Issues**

#### **Problem**: Wrong Python version
```bash
$ python --version
Python 2.7.18
```

#### **Solution**:
```bash
# Install Python 3.11+
# On macOS with Homebrew:
brew install python@3.11

# On Ubuntu:
sudo apt-get install python3.11 python3.11-venv

# Use pyenv for version management:
pyenv install 3.11.7
pyenv local 3.11.7
python --version  # Should show 3.11.7
```

#### **Problem**: Virtual environment not activating
```bash
$ source venv/bin/activate
-bash: venv/bin/activate: No such file or directory
```

#### **Solution**:
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python  # Should show path to venv/bin/python
```

### **2. Node.js & npm Issues**

#### **Problem**: Node.js version compatibility
```bash
$ node --version
v14.21.3
# OmniDev Supreme requires Node.js 18+
```

#### **Solution**:
```bash
# Install Node.js 18+ using nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# Install and use Node.js 18
nvm install 18
nvm use 18
nvm alias default 18

# Verify version
node --version  # Should show v18.x.x
```

#### **Problem**: npm permission issues
```bash
$ npm install
Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules'
```

#### **Solution**:
```bash
# Option 1: Use nvm (recommended)
nvm use 18

# Option 2: Configure npm to use different directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 3: Fix permissions (not recommended for system-wide)
sudo chown -R $(whoami) ~/.npm
```

### **3. Dependency Installation Issues**

#### **Problem**: pip install fails
```bash
$ pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement package==1.0.0
```

#### **Solution**:
```bash
# Update pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -r requirements.txt -v

# Install specific problematic packages manually
pip install problematic-package==version

# Use alternative index if needed
pip install -r requirements.txt -i https://pypi.org/simple/
```

#### **Problem**: Frontend dependencies fail
```bash
$ npm install
npm ERR! peer dep missing: react@^18.0.0, required by @testing-library/react@13.4.0
```

#### **Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Install dependencies
npm install

# Fix peer dependencies
npm install --legacy-peer-deps

# Install specific versions
npm install react@18.2.0 react-dom@18.2.0
```

## 🚀 Startup & Configuration Issues

### **4. Environment Configuration**

#### **Problem**: Missing environment variables
```bash
$ python -m backend.main
KeyError: 'OPENAI_API_KEY'
```

#### **Solution**:
```bash
# Copy and configure .env file
cp .env.example .env

# Edit .env with your values
nano .env

# Required variables:
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
DATABASE_URL=sqlite:///./omnidev_supreme.db
SECRET_KEY=your-secret-key-here

# Load environment variables
source .env

# Or use direnv for automatic loading
echo "dotenv" > .envrc
direnv allow
```

#### **Problem**: Invalid API keys
```bash
$ curl -X POST http://localhost:8000/agents/execute
{"error": "Invalid API key"}
```

#### **Solution**:
```bash
# Verify API key format
echo $OPENAI_API_KEY | grep -E "^sk-[a-zA-Z0-9]{48}$"

# Test API key directly
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Generate new API key if needed
# Visit: https://platform.openai.com/api-keys

# Update .env with new key
echo "OPENAI_API_KEY=sk-new-key-here" >> .env
```

### **5. Port & Network Issues**

#### **Problem**: Port already in use
```bash
$ python -m backend.main
OSError: [Errno 48] Address already in use
```

#### **Solution**:
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use different port
export PORT=8001
python -m backend.main

# For frontend (port 3000)
kill -9 $(lsof -ti:3000)
# Or set different port
export PORT=3001 && npm start
```

#### **Problem**: Cannot connect to backend
```bash
$ curl http://localhost:8000/health
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

#### **Solution**:
```bash
# Check if backend is running
ps aux | grep "python -m backend.main"

# Start backend
python -m backend.main

# Check backend logs
tail -f logs/backend.log

# Verify backend is listening
netstat -tlnp | grep 8000

# Test with verbose curl
curl -v http://localhost:8000/health
```

## 🤖 Agent Issues

### **6. Agent Not Responding**

#### **Problem**: Agent timeout
```bash
{"error": "Agent timeout after 300 seconds"}
```

#### **Solution**:
```bash
# Check agent status
curl http://localhost:8000/agents

# Restart specific agent
curl -X POST http://localhost:8000/agents/architect_agent/restart

# Check agent logs
tail -f logs/agents.log | grep "architect_agent"

# Increase timeout in config
# Edit backend/config/agents.yaml
agents:
  architect_agent:
    timeout_seconds: 600  # Increase from 300
```

#### **Problem**: Agent validation failures
```bash
{"error": "Task validation failed: Agent cannot handle this task type"}
```

#### **Solution**:
```bash
# Check agent capabilities
curl http://localhost:8000/agents/architect_agent

# Verify task format
{
  "content": "Design a web application",
  "type": "architecture_design",
  "context": {
    "language": "python",
    "framework": "fastapi"
  }
}

# Check agent keywords
# Architecture keywords: "architecture", "design", "system", "plan"
# Coding keywords: "generate", "create", "implement", "code"
```

### **7. Memory System Issues**

#### **Problem**: Memory search not working
```bash
{"error": "Vector database not initialized"}
```

#### **Solution**:
```bash
# Initialize vector database
python -c "
from backend.memory.vector_memory import VectorMemory
memory = VectorMemory({'faiss_index_path': './data/vector_db'})
memory.initialize()
"

# Check memory system status
curl http://localhost:8000/memory/status

# Rebuild vector index
python -c "
from backend.memory.memory_manager import UnifiedMemoryManager
memory = UnifiedMemoryManager({})
memory.rebuild_vector_index()
"
```

#### **Problem**: Memory storage errors
```bash
{"error": "Failed to store memory: Database locked"}
```

#### **Solution**:
```bash
# Check database locks
fuser database.db

# Kill processes using database
pkill -f "python.*database"

# Restart with clean database
rm -f database.db
python -c "
from backend.database import init_db
import asyncio
asyncio.run(init_db())
"
```

### **8. Model Orchestration Issues**

#### **Problem**: Model selection errors
```bash
{"error": "No suitable model found for task complexity"}
```

#### **Solution**:
```bash
# Check model availability
curl http://localhost:8000/models/status

# Verify model configuration
# Edit backend/config/models.yaml
models:
  openai:
    enabled: true
    models:
      - gpt-4
      - gpt-3.5-turbo
  anthropic:
    enabled: true
    models:
      - claude-3-opus
      - claude-3-sonnet

# Test model directly
curl -X POST http://localhost:8000/models/test \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "prompt": "Hello"}'
```

## 🌐 Frontend Issues

### **9. React Application Issues**

#### **Problem**: White screen of death
```bash
# Console shows:
Uncaught TypeError: Cannot read property 'map' of undefined
```

#### **Solution**:
```bash
# Check console for errors
# Open browser → F12 → Console

# Common fixes:
# 1. Check API connection
curl http://localhost:8000/health

# 2. Verify environment variables
echo $REACT_APP_API_URL

# 3. Clear browser cache
# Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

# 4. Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### **Problem**: Monaco Editor not loading
```bash
# Console shows:
Failed to load Monaco Editor
```

#### **Solution**:
```bash
# Check Monaco Editor installation
npm list monaco-editor

# Reinstall if needed
npm install monaco-editor@^0.44.0

# Check webpack configuration
# Ensure proper loading in vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      external: ['monaco-editor/esm/vs/editor/editor.worker']
    }
  }
})
```

### **10. WebSocket Connection Issues**

#### **Problem**: Real-time updates not working
```bash
# Console shows:
WebSocket connection failed
```

#### **Solution**:
```bash
# Check WebSocket endpoint
curl -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Key: test" \
     -H "Sec-WebSocket-Version: 13" \
     http://localhost:8000/ws

# Verify WebSocket configuration
# In backend/main.py:
from fastapi import WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # ... websocket logic

# Check firewall/proxy settings
# Ensure WebSocket traffic is allowed
```

## 💾 Database Issues

### **11. SQLite Database Issues**

#### **Problem**: Database locked
```bash
sqlite3.OperationalError: database is locked
```

#### **Solution**:
```bash
# Check for open connections
lsof database.db

# Kill processes using database
pkill -f "python.*database"

# Enable WAL mode for better concurrency
sqlite3 database.db "PRAGMA journal_mode=WAL;"

# Increase busy timeout
# In backend/database.py:
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)
```

#### **Problem**: Migration failures
```bash
alembic.util.exc.CommandError: Can't locate revision identified by 'abc123'
```

#### **Solution**:
```bash
# Check migration history
alembic history

# Reset to base
alembic downgrade base

# Delete migration files
rm alembic/versions/*.py

# Create new initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### **12. Vector Database Issues**

#### **Problem**: FAISS index corruption
```bash
{"error": "FAISS index is corrupted or invalid"}
```

#### **Solution**:
```bash
# Remove corrupted index
rm -rf data/vector_db/*

# Rebuild index
python -c "
from backend.memory.vector_memory import VectorMemory
memory = VectorMemory({'faiss_index_path': './data/vector_db'})
memory.initialize()
memory.rebuild_index()
"

# Verify index integrity
python -c "
import faiss
index = faiss.read_index('./data/vector_db/index.faiss')
print(f'Index size: {index.ntotal}')
"
```

## 🔐 Security Issues

### **13. Authentication Problems**

#### **Problem**: JWT token invalid
```bash
{"error": "Invalid authentication credentials"}
```

#### **Solution**:
```bash
# Check JWT secret key
echo $JWT_SECRET_KEY

# Generate new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env file
echo "JWT_SECRET_KEY=new-secret-key-here" >> .env

# Verify token structure
# JWT should have format: xxxxx.yyyyy.zzzzz
echo $JWT_TOKEN | cut -d. -f1 | base64 -d
```

#### **Problem**: CORS errors
```bash
Access to XMLHttpRequest at 'http://localhost:8000/api' from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### **Solution**:
```bash
# Check CORS configuration in backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For development, allow all origins (not for production)
allow_origins=["*"]
```

### **14. API Key Security**

#### **Problem**: API key exposed in logs
```bash
# Log file shows:
INFO: Using API key: sk-abc123...
```

#### **Solution**:
```bash
# Check log configuration
# Edit backend/config/logging.yaml
formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # Ensure no sensitive data in logs

# Sanitize environment variables
# In backend/config.py:
import os
def get_api_key():
    key = os.getenv('OPENAI_API_KEY')
    if key:
        return key
    raise ValueError("API key not found")

# Use environment variable files with proper permissions
chmod 600 .env
```

## 🚀 Performance Issues

### **15. Slow Response Times**

#### **Problem**: Agents taking too long to respond
```bash
{"error": "Request timeout after 120 seconds"}
```

#### **Solution**:
```bash
# Check system resources
htop
df -h

# Monitor agent performance
curl http://localhost:8000/agents/stats

# Optimize agent configuration
# Edit backend/config/agents.yaml
agents:
  coder_agent:
    max_concurrent_tasks: 3  # Increase parallelism
    timeout_seconds: 300     # Adjust timeout
    model_preference: "gpt-3.5-turbo"  # Use faster model

# Enable caching
# In backend/config/cache.yaml
cache:
  enabled: true
  redis_url: "redis://localhost:6379"
  ttl: 3600
```

### **16. Memory Usage Issues**

#### **Problem**: High memory consumption
```bash
# System shows high memory usage
Memory: 7.5GB/8GB used
```

#### **Solution**:
```bash
# Check memory usage by process
ps aux --sort=-%mem | head -10

# Optimize vector database
# Reduce vector dimensions or entries
# Edit backend/config/memory.yaml
memory:
  vector_store:
    max_entries: 50000  # Reduce from 100000
    dimension: 512      # Reduce from 1536

# Enable garbage collection
# In backend/main.py:
import gc
gc.collect()

# Monitor memory usage
pip install memory-profiler
python -m memory_profiler backend/main.py
```

## 🔧 Development Issues

### **17. Code Generation Issues**

#### **Problem**: Generated code has syntax errors
```bash
{"error": "SyntaxError: invalid syntax"}
```

#### **Solution**:
```bash
# Check agent model configuration
# Prefer GPT-4 for code generation
curl -X PUT http://localhost:8000/agents/coder_agent/config \
  -H "Content-Type: application/json" \
  -d '{"model_preference": "gpt-4"}'

# Validate generated code
python -m py_compile generated_file.py

# Use more specific prompts
# Instead of: "Create a web app"
# Use: "Create a FastAPI web application with user authentication using JWT tokens"
```

### **18. Testing Issues**

#### **Problem**: Tests failing unexpectedly
```bash
$ pytest
FAILED tests/test_agent.py::test_agent_execute - AssertionError
```

#### **Solution**:
```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/test_agent.py::test_agent_execute -v

# Check test dependencies
pip install pytest-mock pytest-asyncio

# Clear test cache
pytest --cache-clear

# Run tests in isolated environment
python -m pytest tests/
```

## 🛠️ Advanced Troubleshooting

### **19. Docker Issues**

#### **Problem**: Docker containers not starting
```bash
$ docker-compose up
ERROR: Container exited with code 1
```

#### **Solution**:
```bash
# Check Docker logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check resource allocation
docker system df
docker system prune

# Verify Dockerfile syntax
docker build -t test-backend ./backend
```

### **20. Production Deployment Issues**

#### **Problem**: SSL certificate errors
```bash
curl: (60) SSL certificate problem: self signed certificate
```

#### **Solution**:
```bash
# Check certificate validity
openssl x509 -in cert.pem -text -noout

# Renew Let's Encrypt certificate
certbot renew

# Configure nginx properly
# /etc/nginx/sites-available/omnidev-supreme
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🆘 Getting Help

### **Diagnostic Commands**
```bash
# System information
python --version
node --version
npm --version
docker --version

# Service status
systemctl status nginx
systemctl status redis
ps aux | grep python
ps aux | grep node

# Network connectivity
curl -I http://localhost:8000/health
curl -I http://localhost:3000
netstat -tlnp | grep -E ":(8000|3000)"

# Log analysis
tail -f logs/backend.log
tail -f logs/frontend.log
journalctl -u nginx -f
```

### **Support Channels**
- **Discord**: Real-time community support
- **GitHub Issues**: Bug reports and feature requests
- **Stack Overflow**: Technical questions with tags `omnidev-supreme`, `ai-agents`
- **Documentation**: Comprehensive guides and tutorials

### **Before Seeking Help**
1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Review the relevant documentation
4. Gather system information and logs
5. Try to reproduce the issue

### **When Reporting Issues**
Include:
- System information (OS, Python version, Node.js version)
- Error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior
- Relevant configuration files
- Log files (sanitized of sensitive information)

---

<div align="center">
  <p><strong>🔧 Most issues can be resolved with these solutions</strong></p>
  <p>If you're still experiencing problems, don't hesitate to reach out for help!</p>
  
  <a href="installation.md">
    <strong>Check Installation Issues →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/troubleshooting/common-issues.md)*