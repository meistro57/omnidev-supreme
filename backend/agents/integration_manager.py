"""
OmniDev Supreme Agent Integration Manager
Coordinates all agents from different systems
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .registry.agent_registry import agent_registry, AgentType
from .agency.architect_agent import create_architect_agent
from .agency.coder_agent import create_coder_agent
from ..memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ..orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class AgentIntegrationManager:
    """
    Manages integration of all agents from different systems:
    - The-Agency agents
    - MeistroCraft agents
    - OBELISK agents
    - AI-Development-Team agents
    - Village-of-Intelligence agents
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.registry = agent_registry
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        self.integration_stats = {
            "total_agents": 0,
            "successful_integrations": 0,
            "failed_integrations": 0,
            "systems_integrated": []
        }
        
        logger.info("🔗 Agent Integration Manager initialized")
    
    async def initialize_all_agents(self):
        """Initialize and register all agents from all systems"""
        logger.info("🚀 Starting agent integration process...")
        
        # Phase 1: The-Agency agents
        await self._integrate_agency_agents()
        
        # Phase 2: MeistroCraft agents (planned)
        await self._integrate_meistrocraft_agents()
        
        # Phase 3: OBELISK agents (planned)
        await self._integrate_obelisk_agents()
        
        # Phase 4: AI-Development-Team agents (planned)
        await self._integrate_ai_dev_team_agents()
        
        # Phase 5: Village-of-Intelligence agents (planned)
        await self._integrate_village_agents()
        
        # Log integration results
        await self._log_integration_results()
        
        logger.info(f"✅ Agent integration complete: {self.integration_stats}")
    
    async def _integrate_agency_agents(self):
        """Integrate The-Agency agents"""
        logger.info("🏗️  Integrating The-Agency agents...")
        
        try:
            # Create and register Architect Agent
            architect_agent = create_architect_agent(self.config)
            if self.registry.register_agent(architect_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Architect Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Architect Agent integration failed")
            
            # Create and register Coder Agent
            coder_agent = create_coder_agent(self.config)
            if self.registry.register_agent(coder_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Coder Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Coder Agent integration failed")
            
            # TODO: Add Tester, Reviewer, Fixer, Deployer agents
            
            self.integration_stats["systems_integrated"].append("The-Agency")
            
        except Exception as e:
            logger.error(f"❌ The-Agency integration failed: {e}")
            self.integration_stats["failed_integrations"] += 1
    
    async def _integrate_meistrocraft_agents(self):
        """Integrate MeistroCraft agents"""
        logger.info("🎯 Integrating MeistroCraft agents...")
        
        try:
            # TODO: Integrate MeistroCraft agents
            # - GPT-4 Orchestrator
            # - Claude Executor
            # - Session Manager
            # - GitHub Integrator
            # - Token Tracker
            
            logger.info("⏳ MeistroCraft integration planned for next phase")
            
        except Exception as e:
            logger.error(f"❌ MeistroCraft integration failed: {e}")
    
    async def _integrate_obelisk_agents(self):
        """Integrate OBELISK agents"""
        logger.info("🔮 Integrating OBELISK agents...")
        
        try:
            # TODO: Integrate OBELISK agents
            # - Code Architect
            # - Code Generator
            # - Quality Checker
            # - Test Harness Agent
            # - Ideas Agent
            # - Creativity Agent
            # - Self-Scoring Agent
            
            logger.info("⏳ OBELISK integration planned for next phase")
            
        except Exception as e:
            logger.error(f"❌ OBELISK integration failed: {e}")
    
    async def _integrate_ai_dev_team_agents(self):
        """Integrate AI-Development-Team agents"""
        logger.info("👥 Integrating AI-Development-Team agents...")
        
        try:
            # TODO: Integrate AI-Development-Team agents
            # - ProjectManagerAgent
            # - ArchitectAgent
            # - DeveloperAgent
            # - QAAgent
            # - DevOpsAgent
            # - ReviewAgent
            
            logger.info("⏳ AI-Development-Team integration planned for next phase")
            
        except Exception as e:
            logger.error(f"❌ AI-Development-Team integration failed: {e}")
    
    async def _integrate_village_agents(self):
        """Integrate Village-of-Intelligence agents"""
        logger.info("🏘️  Integrating Village-of-Intelligence agents...")
        
        try:
            # TODO: Integrate Village-of-Intelligence agents
            # - ThinkerAgent
            # - BuilderAgent
            # - ArtistAgent
            # - GuardianAgent
            # - TrainerAgent
            
            logger.info("⏳ Village-of-Intelligence integration planned for next phase")
            
        except Exception as e:
            logger.error(f"❌ Village-of-Intelligence integration failed: {e}")
    
    async def _log_integration_results(self):
        """Log integration results to memory"""
        integration_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": self.registry.get_registry_stats()["total_agents"],
            "successful_integrations": self.integration_stats["successful_integrations"],
            "failed_integrations": self.integration_stats["failed_integrations"],
            "systems_integrated": self.integration_stats["systems_integrated"],
            "agent_types": self.registry.get_registry_stats()["agents_by_type"]
        }
        
        # Store in memory
        self.memory_manager.store_memory(
            content=f"Agent integration completed: {json.dumps(integration_summary, indent=2)}",
            memory_type=MemoryType.AGENT,
            priority=MemoryPriority.HIGH,
            metadata={
                "integration_manager": True,
                "integration_summary": integration_summary
            },
            tags=["integration", "agents", "systems"]
        )
    
    async def execute_workflow(self, workflow_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a multi-agent workflow
        
        Example workflow:
        1. Architect plans the project
        2. Coder implements the plan
        3. Tester creates tests
        4. Reviewer checks quality
        5. Fixer addresses issues
        6. Deployer handles deployment
        """
        try:
            workflow_id = workflow_request.get("id", "unknown")
            user_request = workflow_request.get("content", "")
            session_id = workflow_request.get("session_id")
            
            logger.info(f"🔄 Starting workflow execution: {workflow_id}")
            
            workflow_results = {
                "workflow_id": workflow_id,
                "stages": [],
                "success": True,
                "error": None
            }
            
            # Stage 1: Architecture Planning
            architect_agent = self.registry.get_agent("architect")
            if architect_agent:
                logger.info("🏗️  Stage 1: Architecture Planning")
                architecture_task = {
                    "id": f"{workflow_id}_architecture",
                    "content": user_request,
                    "type": "architecture",
                    "session_id": session_id
                }
                
                arch_result = await architect_agent.execute(architecture_task)
                workflow_results["stages"].append({
                    "stage": "architecture",
                    "agent": "architect",
                    "result": arch_result
                })
                
                if not arch_result.get("success"):
                    workflow_results["success"] = False
                    workflow_results["error"] = f"Architecture stage failed: {arch_result.get('error')}"
                    return workflow_results
            
            # Stage 2: Code Implementation
            coder_agent = self.registry.get_agent("coder")
            if coder_agent and workflow_results["success"]:
                logger.info("💻 Stage 2: Code Implementation")
                
                # Extract plan from architecture result
                plan = workflow_results["stages"][0]["result"].get("plan", {})
                coding_request = self._create_coding_request_from_plan(user_request, plan)
                
                coding_task = {
                    "id": f"{workflow_id}_coding",
                    "content": coding_request,
                    "type": "coding",
                    "language": "python",  # TODO: Make this configurable
                    "context": {"plan": plan},
                    "session_id": session_id
                }
                
                code_result = await coder_agent.execute(coding_task)
                workflow_results["stages"].append({
                    "stage": "coding",
                    "agent": "coder",
                    "result": code_result
                })
                
                if not code_result.get("success"):
                    workflow_results["success"] = False
                    workflow_results["error"] = f"Coding stage failed: {code_result.get('error')}"
                    return workflow_results
            
            # TODO: Add more stages (testing, review, fixing, deployment)
            
            # Store workflow results
            self.memory_manager.store_memory(
                content=f"Workflow execution completed: {json.dumps(workflow_results, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "workflow_id": workflow_id,
                    "stages_completed": len(workflow_results["stages"]),
                    "success": workflow_results["success"]
                },
                tags=["workflow", "execution", "multi-agent"],
                session_id=session_id
            )
            
            logger.info(f"✅ Workflow execution completed: {workflow_id}")
            return workflow_results
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            return {
                "workflow_id": workflow_request.get("id", "unknown"),
                "stages": [],
                "success": False,
                "error": str(e)
            }
    
    def _create_coding_request_from_plan(self, original_request: str, plan: Dict[str, Any]) -> str:
        """Create a coding request based on architectural plan"""
        try:
            if "tasks" in plan and plan["tasks"]:
                # Take first few tasks for initial implementation
                tasks = plan["tasks"][:3]
                task_descriptions = [task.get("description", "") for task in tasks]
                
                return f"""
Based on the architectural plan, implement the following:

Original Request: {original_request}

Priority Tasks:
{chr(10).join(f"- {task}" for task in task_descriptions)}

Please provide a complete implementation with proper structure, error handling, and documentation.
"""
            else:
                return f"""
Implement the following request with a complete, well-structured solution:

{original_request}

Please provide production-ready code with proper error handling and documentation.
"""
        except Exception as e:
            logger.warning(f"⚠️  Failed to create coding request from plan: {e}")
            return original_request
    
    def get_available_agents(self) -> Dict[str, Any]:
        """Get all available agents and their capabilities"""
        return {
            "total_agents": len(self.registry.agents),
            "agents_by_type": self.registry.get_registry_stats()["agents_by_type"],
            "available_agents": [
                {
                    "name": agent.metadata.name,
                    "type": agent.metadata.agent_type.value,
                    "capabilities": agent.metadata.capabilities,
                    "status": agent.status.value,
                    "can_accept_tasks": agent.can_accept_task()
                }
                for agent in self.registry.agents.values()
            ]
        }
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        return {
            **self.integration_stats,
            "registry_stats": self.registry.get_registry_stats(),
            "memory_stats": self.memory_manager.get_memory_stats()
        }


# Global integration manager instance
integration_manager = None

def create_integration_manager(config: Dict[str, Any]) -> AgentIntegrationManager:
    """Create and initialize agent integration manager"""
    global integration_manager
    integration_manager = AgentIntegrationManager(config)
    return integration_manager

async def initialize_unified_agents(config: Dict[str, Any]):
    """Initialize all unified agents"""
    manager = create_integration_manager(config)
    await manager.initialize_all_agents()
    return manager