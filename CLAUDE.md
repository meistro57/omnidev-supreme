# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OmniDev Supreme is a unified AI development orchestrator that consolidates multiple AI agent systems into one platform. It's designed as "The One Platform to Rule Them All" and integrates 29 specialized AI agents from different systems:

- **The-Agency** (6 agents): Core development pipeline (architect, coder, tester, reviewer, fixer, deployer)
- **MeistroCraft** (5 agents): Strategic orchestration (GPT-4 orchestrator, Claude executor, session manager, GitHub integrator, token tracker)
- **OBELISK** (7 agents): Specialized development intelligence (code architect, code generator, quality checker, test harness, ideas, creativity, self-scoring)
- **AI-Development-Team** (6 agents): MCP protocol-based team coordination (project manager, architect, developer, qa, devops, review)
- **Village-of-Intelligence** (5 agents): Self-evolving agent ecosystem (thinker, builder, artist, guardian, trainer)

## Development Commands

### Environment Setup
```bash
# Quick setup for testing (sets placeholder API keys)
source ./setup_env.sh

# Full setup with dependencies
./start.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI server
python -m backend.main

# Alternative with uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Agent Integration
```bash
# Test agent integration in Python
python -c "
import sys
sys.path.append('backend')
from backend.agents.integration_manager import create_integration_manager
import asyncio

config = {
    'openai': {'api_key': 'test'},
    'anthropic': {'api_key': 'test'},
    'obelisk': {}
}

async def test_integration():
    manager = create_integration_manager(config)
    await manager.initialize_all_agents()
    stats = manager.get_integration_stats()
    print(f'Integration Stats: {stats}')

asyncio.run(test_integration())
"
```

### API Endpoints
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Agent Status**: http://localhost:8000/agents

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

### Agent Integration Pattern

Each agent system follows this pattern:
1. **Agent Implementation**: Inherits from BaseAgent with required methods
2. **Factory Function**: `create_<agent_name>_agent(config)` for instantiation
3. **Integration**: Registered via AgentIntegrationManager
4. **Validation**: Task validation based on content keywords
5. **Execution**: Async execution with memory storage and orchestration

### Memory Integration Pattern

All agents store results using:
```python
self.memory_manager.store_memory(
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

Configuration structure:
```python
config = {
    'openai': {'api_key': 'sk-...'},
    'anthropic': {'api_key': 'sk-ant-...'},
    'obelisk': {},
    'the_agency': {},
    'meistrocraft': {}
}
```

## Development Guidelines

### Adding New Agents

1. **Create Agent Class**: Inherit from BaseAgent in appropriate system directory
2. **Implement Required Methods**: `execute()` and `validate_task()`
3. **Create Factory Function**: `create_<agent_name>_agent(config)`
4. **Register in Integration Manager**: Add to `_integrate_<system>_agents()`
5. **Update Documentation**: Add to AGENTS.md and API.md

### Working with Multi-Agent Workflows

The system supports complex multi-agent workflows through:
- **Sequential Execution**: Tasks flow through agent pipeline
- **Parallel Processing**: Multiple agents can work concurrently
- **Conditional Routing**: Based on task validation and agent capabilities
- **Memory Sharing**: Cross-agent context via unified memory system

### Error Handling Pattern

All agents should follow this error handling pattern:
```python
try:
    self.status = AgentStatus.BUSY
    # ... processing ...
    self.status = AgentStatus.IDLE
    return {"success": True, "result": result}
except Exception as e:
    self.status = AgentStatus.ERROR
    logger.error(f"Agent {self.metadata.name} failed: {e}")
    return {"success": False, "error": str(e)}
```

## Current Development Status

- **Phase 1**: Foundation architecture ✅
- **Phase 2**: Core integration (29/29 agents) ✅
  - The-Agency: 6/6 agents ✅
  - MeistroCraft: 5/5 agents ✅
  - OBELISK: 7/7 agents ✅
  - AI-Development-Team: 6/6 agents ✅
  - Village-of-Intelligence: 5/5 agents ✅
- **Phase 3**: Advanced features (knowledge graph, web interface) 🚧
- **Phase 4**: Production deployment ⏳

## Key Integration Points

When working with this codebase:

1. **Agent Development**: Focus on the BaseAgent interface and validation patterns
2. **Memory Management**: Use the unified memory system for persistence
3. **Model Selection**: Leverage model orchestrator for optimal AI model routing
4. **Workflow Design**: Consider multi-agent coordination and error handling
5. **Testing**: Verify agent integration through integration manager tests

The system is designed to be extensible - new agent systems can be added by following the established patterns in the existing agency/, meistrocraft/, obelisk/, ai_dev_team/, and village/ directories.

## Village-of-Intelligence Agents

The Village-of-Intelligence system brings collective intelligence and self-evolution to the platform:

- **ThinkerAgent**: Strategic thinking, decision-making, and planning
- **BuilderAgent**: Construction, implementation, and systematic building
- **ArtistAgent**: Creative design, aesthetics, and user experience
- **GuardianAgent**: Security, protection, and compliance
- **TrainerAgent**: Training, learning, and knowledge development

These agents work together in a collective intelligence framework, sharing knowledge and insights through the unified memory system.