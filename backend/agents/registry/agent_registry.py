"""
OmniDev Supreme Agent Registry
Central registry for all AI agents from all systems
"""

from typing import Dict, List, Optional, Type, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Agent type classification"""
    ARCHITECT = "architect"
    CODER = "coder"
    TESTER = "tester"
    REVIEWER = "reviewer"
    FIXER = "fixer"
    DEPLOYER = "deployer"
    ORCHESTRATOR = "orchestrator"
    MEMORY = "memory"
    CREATIVE = "creative"
    GUARDIAN = "guardian"
    ANALYZER = "analyzer"


class AgentStatus(Enum):
    """Agent status states"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class AgentMetadata:
    """Agent metadata and configuration"""
    name: str
    agent_type: AgentType
    description: str
    capabilities: List[str]
    model_requirements: List[str]
    priority: int = 1
    max_concurrent_tasks: int = 1
    timeout_seconds: int = 300
    retry_count: int = 3


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, metadata: AgentMetadata, config: Dict[str, Any]):
        self.metadata = metadata
        self.config = config
        self.status = AgentStatus.IDLE
        self.current_tasks: List[str] = []
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_response_time": 0.0,
            "total_tokens_used": 0
        }
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task and return results"""
        pass
    
    @abstractmethod
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if agent can handle the task"""
        pass
    
    def can_accept_task(self) -> bool:
        """Check if agent can accept new tasks"""
        return (
            self.status == AgentStatus.IDLE and
            len(self.current_tasks) < self.metadata.max_concurrent_tasks
        )
    
    def update_stats(self, task_result: Dict[str, Any]):
        """Update agent statistics"""
        if task_result.get("success"):
            self.stats["tasks_completed"] += 1
        else:
            self.stats["tasks_failed"] += 1
        
        if "response_time" in task_result:
            current_avg = self.stats["average_response_time"]
            total_tasks = self.stats["tasks_completed"] + self.stats["tasks_failed"]
            self.stats["average_response_time"] = (
                (current_avg * (total_tasks - 1) + task_result["response_time"]) / total_tasks
            )
        
        if "tokens_used" in task_result:
            self.stats["total_tokens_used"] += task_result["tokens_used"]


class AgentRegistry:
    """Central registry for all AI agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[AgentType, List[str]] = {
            agent_type: [] for agent_type in AgentType
        }
        self.task_queue: List[Dict[str, Any]] = []
        logger.info("🚀 Agent Registry initialized")
    
    def register_agent(self, agent: BaseAgent) -> bool:
        """Register a new agent"""
        try:
            agent_name = agent.metadata.name
            
            if agent_name in self.agents:
                logger.warning(f"⚠️  Agent {agent_name} already registered, replacing")
            
            self.agents[agent_name] = agent
            self.agent_types[agent.metadata.agent_type].append(agent_name)
            
            logger.info(f"✅ Registered agent: {agent_name} ({agent.metadata.agent_type.value})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register agent: {e}")
            return False
    
    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent"""
        try:
            if agent_name not in self.agents:
                logger.warning(f"⚠️  Agent {agent_name} not found")
                return False
            
            agent = self.agents[agent_name]
            self.agent_types[agent.metadata.agent_type].remove(agent_name)
            del self.agents[agent_name]
            
            logger.info(f"🗑️  Unregistered agent: {agent_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to unregister agent: {e}")
            return False
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get agent by name"""
        return self.agents.get(agent_name)
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[BaseAgent]:
        """Get all agents of a specific type"""
        agent_names = self.agent_types.get(agent_type, [])
        return [self.agents[name] for name in agent_names if name in self.agents]
    
    def get_available_agents(self, agent_type: Optional[AgentType] = None) -> List[BaseAgent]:
        """Get all available agents (can accept tasks)"""
        if agent_type:
            candidates = self.get_agents_by_type(agent_type)
        else:
            candidates = list(self.agents.values())
        
        return [agent for agent in candidates if agent.can_accept_task()]
    
    def find_best_agent(self, task: Dict[str, Any]) -> Optional[BaseAgent]:
        """Find the best agent for a task"""
        task_type = task.get("type")
        required_capabilities = task.get("capabilities", [])
        
        # Get agents of the required type
        if task_type:
            try:
                agent_type = AgentType(task_type)
                candidates = self.get_available_agents(agent_type)
            except ValueError:
                candidates = self.get_available_agents()
        else:
            candidates = self.get_available_agents()
        
        # Filter by capabilities
        if required_capabilities:
            candidates = [
                agent for agent in candidates
                if all(cap in agent.metadata.capabilities for cap in required_capabilities)
            ]
        
        if not candidates:
            return None
        
        # Sort by priority and performance
        candidates.sort(key=lambda agent: (
            -agent.metadata.priority,
            agent.stats["average_response_time"],
            -agent.stats["tasks_completed"]
        ))
        
        return candidates[0]
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the best available agent"""
        try:
            agent = self.find_best_agent(task)
            if not agent:
                return {
                    "success": False,
                    "error": "No suitable agent available",
                    "task_id": task.get("id")
                }
            
            # Validate task
            if not await agent.validate_task(task):
                return {
                    "success": False,
                    "error": "Task validation failed",
                    "task_id": task.get("id"),
                    "agent": agent.metadata.name
                }
            
            # Execute task
            agent.status = AgentStatus.BUSY
            agent.current_tasks.append(task.get("id", "unknown"))
            
            result = await agent.execute(task)
            
            # Update agent state
            agent.status = AgentStatus.IDLE
            if task.get("id") in agent.current_tasks:
                agent.current_tasks.remove(task.get("id"))
            
            agent.update_stats(result)
            
            return {
                **result,
                "agent": agent.metadata.name,
                "task_id": task.get("id")
            }
            
        except Exception as e:
            logger.error(f"❌ Task execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id")
            }
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_agents": len(self.agents),
            "agents_by_type": {
                agent_type.value: len(agent_names)
                for agent_type, agent_names in self.agent_types.items()
            },
            "available_agents": len(self.get_available_agents()),
            "agents_status": {
                agent.metadata.name: {
                    "status": agent.status.value,
                    "current_tasks": len(agent.current_tasks),
                    "stats": agent.stats
                }
                for agent in self.agents.values()
            }
        }
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get all agent capabilities"""
        return {
            agent.metadata.name: agent.metadata.capabilities
            for agent in self.agents.values()
        }


# Global registry instance
agent_registry = AgentRegistry()