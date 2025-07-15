# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OmniDev Supreme is a unified AI development orchestrator that consolidates 29 specialized AI agents from 5 different systems into one platform. It combines agent-based architecture, multi-model orchestration (OpenAI, Anthropic, Ollama), and advanced memory systems to provide a unified development experience.

**The 5 Agent Systems:**
- **The-Agency** (6 agents): Core development pipeline (architect, coder, tester, reviewer, fixer, deployer)
- **MeistroCraft** (5 agents): Strategic orchestration with GPT-4/Claude integration
- **OBELISK** (7 agents): Specialized development intelligence with creative and quality features
- **AI-Development-Team** (6 agents): MCP protocol-based team coordination
- **Village-of-Intelligence** (5 agents): Self-evolving collective intelligence ecosystem

## Development Commands

### Environment Setup
```bash
# Quick setup for testing (sets placeholder API keys)
source ./setup_env.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI server
python -m backend.main

# Start the frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Backend tests (when available)
pytest backend/tests/

# Frontend tests
cd frontend
npm test

# Frontend linting
cd frontend
npm run lint

# Frontend build
cd frontend
npm run build
```

### Development Tools
```bash
# Format Python code
black backend/

# Python type checking
mypy backend/

# Python linting
flake8 backend/
```

### API Endpoints
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Agent Status**: http://localhost:8000/agents

### Frontend Interface
- **Web Interface**: http://localhost:3000
- **Monaco Editor**: VS Code-style editor with syntax highlighting
- **Agent Dashboard**: Real-time monitoring and control

## Architecture Overview

### Core Components

#### 1. Agent Registry System (`backend/agents/registry/`)
- **BaseAgent**: Abstract base class all agents must inherit from
- **AgentType**: Enum defining agent categories (ARCHITECT, CODER, TESTER, etc.)
- **AgentMetadata**: Configuration and capability metadata for agents
- **AgentStatus**: Runtime status tracking (IDLE, BUSY, ERROR, DISABLED)

Key requirements for new agents:
- Must implement `execute(task: Dict[str, Any]) -> Dict[str, Any]`
- Must implement `validate_task(task: Dict[str, Any]) -> bool`
- Constructor signature: `__init__(self, config: Dict[str, Any])`
- Call `super().__init__(metadata, config)` in constructor

#### 2. Integration Manager (`backend/agents/integration_manager.py`)
- **AgentIntegrationManager**: Coordinates all agent systems
- Manages agent lifecycle and registration
- Provides multi-agent workflow execution
- Handles cross-system coordination

#### 3. Memory System (`backend/memory/`)
- **UnifiedMemoryManager**: Consolidates all memory systems
- **Vector Memory**: FAISS-based semantic search (requires numpy, faiss-cpu, sentence-transformers)
- **Relational Memory**: SQLite-based structured storage
- **Session Memory**: Context persistence across interactions
- **MemoryType**: Enum for memory categorization (CODE, TASK, AGENT, etc.)

#### 4. Model Orchestration (`backend/orchestration/`)
- **ModelOrchestrator**: Intelligent routing between AI models
- **ModelType**: Enum for supported models (OpenAI, Anthropic, Ollama)
- **TaskRequest**: Structured task execution with complexity routing
- Supports OpenAI GPT-4/3.5, Anthropic Claude, and Ollama local models

#### 5. Agent Systems (by directory):
- **agency/**: The-Agency agents for core development lifecycle
- **meistrocraft/**: MeistroCraft agents for strategic orchestration
- **obelisk/**: OBELISK agents for specialized development intelligence
- **ai_dev_team/**: AI-Development-Team agents for team coordination
- **village/**: Village-of-Intelligence agents for self-evolving ecosystem

#### 6. Frontend System (`frontend/`):
- **React 18 + TypeScript**: Modern component-based architecture
- **Monaco Editor**: VS Code-style code editor with syntax highlighting
- **Redux Toolkit**: State management with slices for agents, tasks, projects, memory
- **WebSocket Integration**: Real-time updates via Socket.io
- **Tailwind CSS**: Responsive design with dark theme
- **Vite**: Fast build tool and development server

### Three-Layer Architecture

**Layer 1: Agent Systems** (`backend/agents/`)
- Each system has its own directory with agent implementations
- All agents inherit from `BaseAgent` and implement `execute()` and `validate_task()` methods
- Agents are registered through factory functions like `create_<agent_name>_agent(config)`

**Layer 2: Integration & Orchestration** (`backend/`)
- **AgentIntegrationManager**: Coordinates all 29 agents across systems
- **ModelOrchestrator**: Routes tasks to appropriate AI models (OpenAI, Anthropic, Ollama)
- **UnifiedMemoryManager**: Handles vector, relational, and session memory

**Layer 3: API & Frontend** (`backend/main.py`, `frontend/`)
- FastAPI backend with REST endpoints and WebSocket support
- React + TypeScript frontend with Monaco Editor integration
- Real-time agent monitoring and project management

### Agent Integration Pattern

Each agent system follows this pattern:
1. Agent inherits from `BaseAgent` with required methods
2. Factory function creates agent instances
3. Registration in `AgentIntegrationManager`
4. Task validation based on content keywords
5. Async execution with memory storage

### Memory Integration Pattern

All agents store results using:
```python
await self.memory_manager.store_memory(
    content=result_description,
    memory_type=MemoryType.TASK,
    priority=MemoryPriority.HIGH,
    metadata={"agent": self.metadata.name, "task_id": task_id},
    tags=["relevant", "tags"],
    session_id=session_id
)
```

### Configuration Requirements

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API access
- `ANTHROPIC_API_KEY`: Anthropic API access
- `OLLAMA_HOST`: Ollama local model endpoint (optional)
- `OLLAMA_ENABLED`: Enable Ollama integration (optional)

## Development Guidelines

### Adding New Agents

1. Create agent class inheriting from `BaseAgent` in appropriate system directory
2. Implement `execute()` and `validate_task()` methods
3. Create factory function `create_<agent_name>_agent(config)`
4. Register in `AgentIntegrationManager._integrate_<system>_agents()`
5. Update agent type enum in `backend/agents/registry/agent_registry.py`

### Agent Implementation Template

```python
class NewAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="new_agent",
            agent_type=AgentType.YOUR_TYPE,
            capabilities=["capability1", "capability2"],
            description="Agent description"
        )
        super().__init__(metadata, config)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.status = AgentStatus.BUSY
            # Implementation here
            self.status = AgentStatus.IDLE
            return {"success": True, "result": result}
        except Exception as e:
            self.status = AgentStatus.ERROR
            return {"success": False, "error": str(e)}
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        content = task.get("content", "").lower()
        keywords = ["keyword1", "keyword2"]
        return any(keyword in content for keyword in keywords)
```

### Working with Multi-Agent Workflows

The system supports complex workflows through:
- **Sequential Execution**: Tasks flow through agent pipeline
- **Parallel Processing**: Multiple agents working concurrently
- **Conditional Routing**: Based on task validation and agent capabilities
- **Memory Sharing**: Cross-agent context via unified memory system

### Key Integration Points

When working with this codebase:

1. **Agent Development**: Focus on the BaseAgent interface and validation patterns
2. **Memory Management**: Use the unified memory system for persistence
3. **Model Selection**: Leverage model orchestrator for optimal AI model routing
4. **Workflow Design**: Consider multi-agent coordination and error handling
5. **Testing**: Verify agent integration through integration manager

The system is designed to be extensible - new agent systems can be added by following the established patterns in the existing directories.