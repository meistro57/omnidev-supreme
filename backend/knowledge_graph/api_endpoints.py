"""
API Endpoints for Knowledge Graph System

This module provides FastAPI endpoints for interacting with the knowledge graph
system in the OmniDev Supreme platform.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, FileResponse
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
import tempfile
import json
import os

from .knowledge_graph import KnowledgeGraph
from .agent_analyzer import AgentAnalyzer
from .agent_selector import GraphBasedAgentSelector, SelectionStrategy
from .schema import GraphNode, GraphRelationship

logger = logging.getLogger(__name__)

# Initialize knowledge graph components
knowledge_graph = KnowledgeGraph()
agent_analyzer = AgentAnalyzer(knowledge_graph)
agent_selector = GraphBasedAgentSelector(knowledge_graph)

# Create router
router = APIRouter(prefix="/knowledge-graph", tags=["knowledge-graph"])


@router.get("/", response_model=Dict[str, Any])
async def get_knowledge_graph():
    """Get the complete knowledge graph data"""
    try:
        # Get all nodes and relationships
        nodes = []
        for node in knowledge_graph.schema.nodes.values():
            nodes.append(node.to_dict())
        
        relationships = []
        for rel in knowledge_graph.schema.relationships.values():
            relationships.append(rel.to_dict())
        
        statistics = knowledge_graph.get_graph_statistics()
        
        return {
            "nodes": nodes,
            "relationships": relationships,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting knowledge graph: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_and_populate_graph(background_tasks: BackgroundTasks):
    """Analyze existing agents and populate the knowledge graph"""
    try:
        # Run analysis in background
        background_tasks.add_task(run_analysis)
        
        return {
            "message": "Analysis started",
            "status": "processing",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def run_analysis():
    """Background task to run agent analysis"""
    try:
        logger.info("Starting agent analysis and knowledge graph population")
        await agent_analyzer.analyze_and_populate()
        logger.info("Agent analysis completed successfully")
    except Exception as e:
        logger.error(f"Error in analysis background task: {str(e)}")


@router.get("/statistics")
async def get_graph_statistics():
    """Get detailed statistics about the knowledge graph"""
    try:
        stats = knowledge_graph.get_graph_statistics()
        
        # Add additional analytics
        agents = knowledge_graph.get_agents()
        capabilities = knowledge_graph.get_capabilities()
        
        # System distribution
        system_stats = {}
        for agent in agents:
            system = agent.system_name
            if system not in system_stats:
                system_stats[system] = {"agents": 0, "total_capabilities": 0}
            system_stats[system]["agents"] += 1
            system_stats[system]["total_capabilities"] += len(agent.capabilities)
        
        # Capability usage
        capability_usage = {}
        for agent in agents:
            for cap in agent.capabilities:
                capability_usage[cap] = capability_usage.get(cap, 0) + 1
        
        # Most connected agents (by relationship count)
        agent_connections = {}
        for agent in agents:
            connections = len(knowledge_graph.schema.get_node_relationships(agent.id))
            agent_connections[agent.name] = connections
        
        # Sort by connection count
        most_connected = sorted(agent_connections.items(), key=lambda x: x[1], reverse=True)[:10]
        
        enhanced_stats = {
            **stats,
            "system_distribution": system_stats,
            "top_capabilities": sorted(capability_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            "most_connected_agents": most_connected,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return enhanced_stats
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend-agents")
async def recommend_agents(
    task: Dict[str, Any],
    strategy: Optional[str] = "optimal_sequence",
    max_agents: Optional[int] = 5,
    min_confidence: Optional[float] = 0.3
):
    """Get agent recommendations for a task using the knowledge graph"""
    try:
        # Validate strategy
        try:
            selection_strategy = SelectionStrategy(strategy)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid strategy. Must be one of: {[s.value for s in SelectionStrategy]}"
            )
        
        # Get recommendations
        result = await agent_selector.select_agents(
            task=task,
            strategy=selection_strategy,
            max_agents=max_agents,
            min_confidence=min_confidence
        )
        
        # Format response
        response = {
            "task": task,
            "strategy": result.strategy.value,
            "recommended_agents": [
                {
                    "agent": {
                        "id": agent.id,
                        "name": agent.name,
                        "type": agent.agent_type,
                        "system": agent.system_name,
                        "capabilities": agent.capabilities,
                        "status": agent.status
                    },
                    "score": score.score,
                    "confidence": score.confidence,
                    "reasoning": score.reasoning
                }
                for agent, score in zip(result.agents, result.scores)
            ],
            "execution_plan": result.execution_plan,
            "total_confidence": result.total_confidence,
            "metadata": result.metadata,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent-insights/{agent_name}")
async def get_agent_insights(agent_name: str):
    """Get detailed insights about a specific agent"""
    try:
        insights = await agent_analyzer.get_agent_insights(agent_name)
        
        if "error" in insights:
            raise HTTPException(status_code=404, detail=insights["error"])
        
        return insights
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/collaborators")
async def get_agent_collaborators(agent_id: str):
    """Get agents that collaborate with the specified agent"""
    try:
        collaborators = knowledge_graph.find_agent_collaborators(agent_id)
        
        return {
            "agent_id": agent_id,
            "collaborators": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "system": agent.system_name
                }
                for agent in collaborators
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting collaborators: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/dependencies")
async def get_agent_dependencies(agent_id: str):
    """Get agents that the specified agent depends on"""
    try:
        dependencies = knowledge_graph.find_agent_dependencies(agent_id)
        
        return {
            "agent_id": agent_id,
            "dependencies": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "system": agent.system_name
                }
                for agent in dependencies
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dependencies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities/{capability}/agents")
async def get_agents_by_capability(capability: str):
    """Get all agents that have a specific capability"""
    try:
        agents = knowledge_graph.find_agents_by_capability(capability)
        
        return {
            "capability": capability,
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "system": agent.system_name,
                    "status": agent.status
                }
                for agent in agents
            ],
            "count": len(agents),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting agents by capability: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/performance")
async def update_agent_performance(agent_id: str, performance_data: Dict[str, Any]):
    """Update performance metrics for an agent"""
    try:
        knowledge_graph.update_agent_performance(agent_id, performance_data)
        
        return {
            "message": "Performance metrics updated",
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating performance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/optimal-sequence")
async def get_optimal_agent_sequence(capabilities: List[str]):
    """Get the optimal sequence of agents for given capabilities"""
    try:
        sequence = knowledge_graph.get_optimal_agent_sequence(capabilities)
        
        return {
            "required_capabilities": capabilities,
            "optimal_sequence": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "system": agent.system_name,
                    "capabilities": agent.capabilities
                }
                for agent in sequence
            ],
            "sequence_length": len(sequence),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting optimal sequence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/json")
async def export_graph_json():
    """Export the knowledge graph as JSON"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            
        # Export to temporary file
        knowledge_graph.export_to_json(temp_path)
        
        # Return file response
        return FileResponse(
            temp_path,
            filename=f"knowledge_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            media_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error exporting JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/selection-analytics")
async def get_selection_analytics():
    """Get analytics about agent selection performance"""
    try:
        analytics = await agent_selector.get_selection_analytics()
        return analytics
    except Exception as e:
        logger.error(f"Error getting selection analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend-strategy")
async def recommend_strategy(task: Dict[str, Any]):
    """Recommend the optimal selection strategy for a task"""
    try:
        strategy = await agent_selector.recommend_optimal_strategy(task)
        
        return {
            "task": task,
            "recommended_strategy": strategy.value,
            "reasoning": f"Based on task complexity and requirements",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error recommending strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reset")
async def reset_knowledge_graph():
    """Reset the knowledge graph (clear all data)"""
    try:
        # Clear in-memory data
        knowledge_graph.schema.nodes.clear()
        knowledge_graph.schema.relationships.clear()
        knowledge_graph.schema.node_indices.clear()
        knowledge_graph.schema.relationship_indices.clear()
        
        # Clear database
        import sqlite3
        conn = sqlite3.connect(knowledge_graph.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM relationships')
        cursor.execute('DELETE FROM nodes')
        conn.commit()
        conn.close()
        
        return {
            "message": "Knowledge graph reset successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error resetting knowledge graph: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for the knowledge graph system"""
    try:
        stats = knowledge_graph.get_graph_statistics()
        
        return {
            "status": "healthy",
            "nodes": stats.get("total_nodes", 0),
            "relationships": stats.get("total_relationships", 0),
            "database_path": knowledge_graph.db_path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }