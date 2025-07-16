"""
OmniDev Supreme - Main FastAPI Application
The One Platform to Rule Them All
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .agents.integration_manager import initialize_unified_agents
from .orchestration.model_orchestrator import create_orchestrator
from .memory.memory_manager import memory_manager
from .knowledge_graph.api_endpoints import router as knowledge_graph_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for API requests
class TaskRequest(BaseModel):
    content: str
    task_type: Optional[str] = "general"
    language: Optional[str] = "python"
    session_id: Optional[str] = None
    priority: Optional[int] = 1


class WorkflowRequest(BaseModel):
    content: str
    workflow_type: str = "full_development"
    session_id: Optional[str] = None
    language: Optional[str] = "python"


class MemoryQuery(BaseModel):
    query: str
    memory_type: Optional[str] = None
    limit: Optional[int] = 10


# Global configuration
CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "ollama_enabled": True,
    "ollama_url": "http://localhost:11434"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Starting OmniDev Supreme...")
    
    # Initialize orchestrator
    orchestrator = create_orchestrator(CONFIG)
    
    # Initialize agents
    integration_manager = await initialize_unified_agents(CONFIG)
    
    # Store references in app state
    app.state.orchestrator = orchestrator
    app.state.integration_manager = integration_manager
    app.state.memory_manager = memory_manager
    
    logger.info("✅ OmniDev Supreme initialized successfully")
    
    yield
    
    logger.info("🛑 Shutting down OmniDev Supreme...")


# Create FastAPI app
app = FastAPI(
    title="OmniDev Supreme",
    description="The One Platform to Rule Them All - Unified AI Development Orchestrator",
    version="0.1.0",
    lifespan=lifespan
)

# Include knowledge graph router
app.include_router(knowledge_graph_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 Welcome to OmniDev Supreme - The One Platform to Rule Them All!",
        "version": "0.1.0",
        "status": "operational",
        "capabilities": [
            "multi_agent_orchestration",
            "code_generation",
            "architecture_planning",
            "memory_management",
            "multi_model_routing"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check orchestrator health
        orchestrator_health = await app.state.orchestrator.health_check_all()
        
        # Check agent registry
        agent_stats = app.state.integration_manager.registry.get_registry_stats()
        
        # Check memory system
        memory_stats = app.state.memory_manager.get_memory_stats()
        
        return {
            "status": "healthy",
            "orchestrator": orchestrator_health,
            "agents": agent_stats,
            "memory": memory_stats
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/agents")
async def get_agents():
    """Get all available agents"""
    try:
        return app.state.integration_manager.get_available_agents()
    except Exception as e:
        logger.error(f"❌ Failed to get agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task")
async def execute_task(request: TaskRequest):
    """Execute a single task using the best available agent"""
    try:
        # Create task object
        task = {
            "id": f"task_{request.session_id or 'default'}_{hash(request.content)}",
            "content": request.content,
            "type": request.task_type,
            "language": request.language,
            "session_id": request.session_id,
            "priority": request.priority
        }
        
        # Execute task using agent registry
        result = await app.state.integration_manager.registry.execute_task(task)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Task execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow")
async def execute_workflow(request: WorkflowRequest):
    """Execute a multi-agent workflow"""
    try:
        # Create workflow object
        workflow = {
            "id": f"workflow_{request.session_id or 'default'}_{hash(request.content)}",
            "content": request.content,
            "workflow_type": request.workflow_type,
            "language": request.language,
            "session_id": request.session_id
        }
        
        # Execute workflow
        result = await app.state.integration_manager.execute_workflow(workflow)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/search")
async def search_memory(query: MemoryQuery):
    """Search memory system"""
    try:
        # Convert string memory type to enum if provided
        memory_type = None
        if query.memory_type:
            memory_type = getattr(memory_manager.MemoryType, query.memory_type.upper(), None)
        
        # Search memory
        results = app.state.memory_manager.search_memory(
            query=query.query,
            memory_type=memory_type,
            limit=query.limit
        )
        
        # Convert results to JSON-serializable format
        serialized_results = []
        for item in results:
            serialized_results.append({
                "id": item.id,
                "content": item.content,
                "memory_type": item.memory_type.value,
                "priority": item.priority.value,
                "created_at": item.created_at.isoformat(),
                "metadata": item.metadata,
                "tags": item.tags
            })
        
        return {
            "query": query.query,
            "results": serialized_results,
            "total": len(serialized_results)
        }
        
    except Exception as e:
        logger.error(f"❌ Memory search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory system statistics"""
    try:
        return app.state.memory_manager.get_memory_stats()
    except Exception as e:
        logger.error(f"❌ Failed to get memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orchestrator/stats")
async def get_orchestrator_stats():
    """Get orchestrator statistics"""
    try:
        return app.state.orchestrator.get_orchestrator_stats()
    except Exception as e:
        logger.error(f"❌ Failed to get orchestrator stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/integration/stats")
async def get_integration_stats():
    """Get integration statistics"""
    try:
        return app.state.integration_manager.get_integration_stats()
    except Exception as e:
        logger.error(f"❌ Failed to get integration stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")