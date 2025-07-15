# Quick Start Guide

Get OmniDev Supreme up and running in just 5 minutes! This guide will have you creating your first project and interacting with AI agents in no time.

## ⚡ 5-Minute Setup

### Prerequisites
- **Node.js 18+** and **npm** installed
- **Python 3.11+** with **pip** installed
- **Git** for version control
- **API Keys** for OpenAI and/or Anthropic (optional for testing)

### Step 1: Clone the Repository
```bash
git clone https://github.com/meistro57/omnidev-supreme.git
cd omnidev-supreme
```

### Step 2: Quick Environment Setup
```bash
# Run the quick setup script
./setup_env.sh

# Or manually:
cp .env.example .env
# Edit .env with your API keys (optional for testing)
```

### Step 3: Start the Backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m backend.main
```

You should see:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Start the Frontend
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

You should see:
```
  VITE v5.4.19  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 5: Access the Platform
Open your browser and navigate to:
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## 🎉 First Look

### Dashboard Overview
When you first open OmniDev Supreme, you'll see:

1. **System Status**: Overview of all 29 agents
2. **Agent Activity**: Real-time status updates
3. **Memory Usage**: Knowledge base statistics
4. **Recent Projects**: Your project workspace

### Navigation
- **Dashboard**: System overview and monitoring
- **Editor**: Monaco Editor with VS Code experience
- **Agents**: Manage and monitor all 29 agents
- **Projects**: Multi-project workspace
- **Memory**: Knowledge graph and search
- **Tasks**: Task queue and execution

## 🚀 Your First Project

### Create a New Project
1. Click **Projects** in the navigation
2. Click **New Project**
3. Enter project details:
   - **Name**: `my-first-project`
   - **Description**: `My first OmniDev Supreme project`
   - **Language**: `JavaScript`
   - **Framework**: `React` (optional)

### Open the Editor
1. Click **Editor** in the navigation
2. Create a new file: `hello-world.js`
3. Start typing - you'll see:
   - **Syntax highlighting**
   - **IntelliSense suggestions**
   - **Real-time validation**

### Interact with Agents
1. Type a comment: `// Create a simple React component`
2. The **Coder Agent** will suggest code
3. Accept suggestions with `Tab` or `Enter`
4. Save the file with `Ctrl+S`

## 🤖 Agent Interaction Examples

### Example 1: Code Generation
```javascript
// Create a React component for a user profile card
```

The **Coder Agent** will generate:
```javascript
import React from 'react';

const UserProfileCard = ({ user }) => {
  return (
    <div className="profile-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
};

export default UserProfileCard;
```

### Example 2: Code Review
Select your code and the **Reviewer Agent** will provide:
- **Code quality analysis**
- **Security recommendations**
- **Performance suggestions**
- **Best practice guidance**

### Example 3: Test Generation
Type: `// Generate tests for this component`

The **Tester Agent** will create:
```javascript
import { render, screen } from '@testing-library/react';
import UserProfileCard from './UserProfileCard';

describe('UserProfileCard', () => {
  const mockUser = {
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://example.com/avatar.jpg'
  };

  it('renders user information correctly', () => {
    render(<UserProfileCard user={mockUser} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('src', mockUser.avatar);
  });
});
```

## 🔧 Configuration Tips

### API Keys Setup
For full functionality, add your API keys to `.env`:
```bash
# OpenAI (recommended)
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Ollama (optional, for local models)
OLLAMA_HOST=http://localhost:11434
OLLAMA_ENABLED=true
```

### Agent Configuration
Customize agent behavior in `backend/config/agents.yaml`:
```yaml
agents:
  coder:
    priority: 10
    max_concurrent_tasks: 3
    default_language: "javascript"
  
  reviewer:
    priority: 8
    strict_mode: true
    security_focus: true
```

### Memory Settings
Configure memory limits in `backend/config/memory.yaml`:
```yaml
memory:
  vector_store:
    max_entries: 100000
    embedding_model: "text-embedding-ada-002"
  
  relational:
    max_connections: 50
    query_timeout: 30
```

## 📊 Health Check

Verify everything is working:

### Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.6.0",
  "agents": {
    "total": 29,
    "active": 29,
    "error": 0
  },
  "memory": {
    "vector_entries": 1250,
    "relational_entries": 890,
    "session_entries": 45
  }
}
```

### Frontend Health
Visit http://localhost:3000 and check:
- ✅ Page loads without errors
- ✅ Navigation works
- ✅ Agent status shows "Connected"
- ✅ Monaco Editor loads properly

### Agent Status
```bash
curl http://localhost:8000/agents
```

Should show all 29 agents with status "idle" or "busy".

## 🎯 Next Steps

Now that you have OmniDev Supreme running, here's what to do next:

### 1. **Explore the Agents**
- Visit the **Agents** page to see all 29 agents
- Read about each agent's capabilities
- Try different types of tasks

### 2. **Learn the Editor**
- Explore Monaco Editor features
- Try different programming languages
- Use keyboard shortcuts (Ctrl+Shift+P for command palette)

### 3. **Understand Memory**
- Visit the **Memory** page
- Search through the knowledge base
- See how agents store and retrieve information

### 4. **Create Real Projects**
- Build a full application
- Use multiple agents in sequence
- Experience the multi-agent workflow

### 5. **Join the Community**
- Join our Discord server
- Follow the GitHub repository
- Share your experiences

## 🆘 Troubleshooting

### Common Issues

**"Port already in use"**
```bash
# Kill existing processes
pkill -f "python -m backend.main"
pkill -f "npm run dev"

# Or use different ports
export PORT=8001  # for backend
export VITE_PORT=3001  # for frontend
```

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
cd frontend && npm install
```

**"Agents not responding"**
```bash
# Check API keys
cat .env | grep API_KEY

# Restart the backend
python -m backend.main
```

### Getting Help
- **Discord**: Real-time community support
- **GitHub Issues**: Report bugs and get help
- **Documentation**: Check the [troubleshooting guide](../troubleshooting/common-issues.md)

## 🎉 Success!

Congratulations! You now have OmniDev Supreme running and ready for development. You've just taken your first step into the future of AI-powered development.

### What You've Accomplished
- ✅ Installed and configured OmniDev Supreme
- ✅ Started both backend and frontend services
- ✅ Created your first project
- ✅ Interacted with AI agents
- ✅ Experienced the Monaco Editor

### Ready for More?
- **[First Steps](first-steps.md)** - Dive deeper into project creation
- **[Agent Overview](../agents/overview.md)** - Learn about all 29 agents
- **[Development Guide](../development/setup.md)** - Advanced development setup
- **[Tutorials](../tutorials/first-project.md)** - Step-by-step learning

---

<div align="center">
  <p><strong>Welcome to the future of development!</strong></p>
  <p>You're now ready to build amazing things with AI agents.</p>
  
  <a href="first-steps.md">
    <strong>Continue Learning →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/getting-started/quick-start.md)*