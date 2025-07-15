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
from .agency.tester_agent import create_tester_agent
from .agency.reviewer_agent import create_reviewer_agent
from .agency.fixer_agent import create_fixer_agent
from .agency.deployer_agent import create_deployer_agent
from .meistrocraft.gpt4_orchestrator_agent import create_gpt4_orchestrator_agent
from .meistrocraft.claude_executor_agent import create_claude_executor_agent
from .meistrocraft.session_manager_agent import create_session_manager_agent
from .meistrocraft.github_integrator_agent import create_github_integrator_agent
from .meistrocraft.token_tracker_agent import create_token_tracker_agent
from .obelisk.code_architect_agent import create_code_architect_agent
from .obelisk.code_generator_agent import create_code_generator_agent
from .obelisk.quality_checker_agent import create_quality_checker_agent
from .obelisk.test_harness_agent import create_test_harness_agent
from .obelisk.ideas_agent import create_ideas_agent
from .obelisk.creativity_agent import create_creativity_agent
from .obelisk.self_scoring_agent import create_self_scoring_agent
from .ai_dev_team.project_manager_agent import create_project_manager_agent
from .ai_dev_team.architect_agent import create_architect_agent
from .ai_dev_team.developer_agent import create_developer_agent
from .ai_dev_team.qa_agent import create_qa_agent
from .ai_dev_team.devops_agent import create_devops_agent
from .ai_dev_team.review_agent import create_review_agent
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
            
            # Create and register Tester Agent
            tester_agent = create_tester_agent(self.config)
            if self.registry.register_agent(tester_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Tester Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Tester Agent integration failed")
            
            # Create and register Reviewer Agent
            reviewer_agent = create_reviewer_agent(self.config)
            if self.registry.register_agent(reviewer_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Reviewer Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Reviewer Agent integration failed")
            
            # Create and register Fixer Agent
            fixer_agent = create_fixer_agent(self.config)
            if self.registry.register_agent(fixer_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Fixer Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Fixer Agent integration failed")
            
            # Create and register Deployer Agent
            deployer_agent = create_deployer_agent(self.config)
            if self.registry.register_agent(deployer_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Deployer Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Deployer Agent integration failed")
            
            self.integration_stats["systems_integrated"].append("The-Agency")
            
        except Exception as e:
            logger.error(f"❌ The-Agency integration failed: {e}")
            self.integration_stats["failed_integrations"] += 1
    
    async def _integrate_meistrocraft_agents(self):
        """Integrate MeistroCraft agents"""
        logger.info("🎯 Integrating MeistroCraft agents...")
        
        try:
            # Create and register GPT-4 Orchestrator Agent
            gpt4_orchestrator = create_gpt4_orchestrator_agent(self.config)
            if self.registry.register_agent(gpt4_orchestrator):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ GPT-4 Orchestrator Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ GPT-4 Orchestrator Agent integration failed")
            
            # Create and register Claude Executor Agent
            claude_executor = create_claude_executor_agent(self.config)
            if self.registry.register_agent(claude_executor):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Claude Executor Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Claude Executor Agent integration failed")
            
            # Create and register Session Manager Agent
            session_manager = create_session_manager_agent(self.config)
            if self.registry.register_agent(session_manager):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Session Manager Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Session Manager Agent integration failed")
            
            # Create and register GitHub Integrator Agent
            github_integrator = create_github_integrator_agent(self.config)
            if self.registry.register_agent(github_integrator):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ GitHub Integrator Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ GitHub Integrator Agent integration failed")
            
            # Create and register Token Tracker Agent
            token_tracker = create_token_tracker_agent(self.config)
            if self.registry.register_agent(token_tracker):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Token Tracker Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Token Tracker Agent integration failed")
            
            self.integration_stats["systems_integrated"].append("MeistroCraft")
            
        except Exception as e:
            logger.error(f"❌ MeistroCraft integration failed: {e}")
            self.integration_stats["failed_integrations"] += 1
    
    async def _integrate_obelisk_agents(self):
        """Integrate OBELISK agents"""
        logger.info("🔮 Integrating OBELISK agents...")
        
        try:
            # Create and register Code Architect Agent
            code_architect = create_code_architect_agent(self.config)
            if self.registry.register_agent(code_architect):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Code Architect Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Code Architect Agent integration failed")
            
            # Create and register Code Generator Agent
            code_generator = create_code_generator_agent(self.config)
            if self.registry.register_agent(code_generator):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Code Generator Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Code Generator Agent integration failed")
            
            # Create and register Quality Checker Agent
            quality_checker = create_quality_checker_agent(self.config)
            if self.registry.register_agent(quality_checker):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Quality Checker Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Quality Checker Agent integration failed")
            
            # Create and register Test Harness Agent
            test_harness = create_test_harness_agent(self.config)
            if self.registry.register_agent(test_harness):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Test Harness Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Test Harness Agent integration failed")
            
            # Create and register Ideas Agent
            ideas_agent = create_ideas_agent(self.config)
            if self.registry.register_agent(ideas_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Ideas Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Ideas Agent integration failed")
            
            # Create and register Creativity Agent
            creativity_agent = create_creativity_agent(self.config)
            if self.registry.register_agent(creativity_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Creativity Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Creativity Agent integration failed")
            
            # Create and register Self-Scoring Agent
            self_scoring = create_self_scoring_agent(self.config)
            if self.registry.register_agent(self_scoring):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Self-Scoring Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Self-Scoring Agent integration failed")
            
            self.integration_stats["systems_integrated"].append("OBELISK")
            
        except Exception as e:
            logger.error(f"❌ OBELISK integration failed: {e}")
            self.integration_stats["failed_integrations"] += 1
    
    async def _integrate_ai_dev_team_agents(self):
        """Integrate AI-Development-Team agents"""
        logger.info("👥 Integrating AI-Development-Team agents...")
        
        try:
            # Create and register Project Manager Agent
            project_manager = create_project_manager_agent(self.config)
            if self.registry.register_agent(project_manager):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Project Manager Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Project Manager Agent integration failed")
            
            # Create and register Architect Agent
            architect = create_architect_agent(self.config)
            if self.registry.register_agent(architect):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Architect Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Architect Agent integration failed")
            
            # Create and register Developer Agent
            developer = create_developer_agent(self.config)
            if self.registry.register_agent(developer):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Developer Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Developer Agent integration failed")
            
            # Create and register QA Agent
            qa_agent = create_qa_agent(self.config)
            if self.registry.register_agent(qa_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ QA Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ QA Agent integration failed")
            
            # Create and register DevOps Agent
            devops_agent = create_devops_agent(self.config)
            if self.registry.register_agent(devops_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ DevOps Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ DevOps Agent integration failed")
            
            # Create and register Review Agent
            review_agent = create_review_agent(self.config)
            if self.registry.register_agent(review_agent):
                self.integration_stats["successful_integrations"] += 1
                logger.info("✅ Review Agent integrated")
            else:
                self.integration_stats["failed_integrations"] += 1
                logger.error("❌ Review Agent integration failed")
            
            self.integration_stats["systems_integrated"].append("AI-Development-Team")
            
        except Exception as e:
            logger.error(f"❌ AI-Development-Team integration failed: {e}")
            self.integration_stats["failed_integrations"] += 1
    
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
            
            # Stage 3: Testing
            tester_agent = self.registry.get_agent("tester")
            if tester_agent and workflow_results["success"]:
                logger.info("🧪 Stage 3: Testing")
                
                # Extract generated code from previous stage
                generated_code = ""
                if len(workflow_results["stages"]) > 1:
                    code_result = workflow_results["stages"][1]["result"]
                    if "code_files" in code_result:
                        generated_code = code_result["code_files"][0].get("content", "")
                
                testing_task = {
                    "id": f"{workflow_id}_testing",
                    "content": f"Create comprehensive tests for: {user_request}",
                    "type": "testing",
                    "language": "python",
                    "code_to_test": generated_code,
                    "session_id": session_id
                }
                
                test_result = await tester_agent.execute(testing_task)
                workflow_results["stages"].append({
                    "stage": "testing",
                    "agent": "tester",
                    "result": test_result
                })
                
                if not test_result.get("success"):
                    workflow_results["success"] = False
                    workflow_results["error"] = f"Testing stage failed: {test_result.get('error')}"
                    return workflow_results
            
            # Stage 4: Code Review
            reviewer_agent = self.registry.get_agent("reviewer")
            if reviewer_agent and workflow_results["success"]:
                logger.info("🔍 Stage 4: Code Review")
                
                # Extract generated code from coding stage
                generated_code = ""
                if len(workflow_results["stages"]) > 1:
                    code_result = workflow_results["stages"][1]["result"]
                    if "code_files" in code_result:
                        generated_code = code_result["code_files"][0].get("content", "")
                
                review_task = {
                    "id": f"{workflow_id}_review",
                    "content": f"Review code quality for: {user_request}",
                    "type": "review",
                    "language": "python",
                    "code_to_review": generated_code,
                    "session_id": session_id
                }
                
                review_result = await reviewer_agent.execute(review_task)
                workflow_results["stages"].append({
                    "stage": "review",
                    "agent": "reviewer",
                    "result": review_result
                })
                
                if not review_result.get("success"):
                    workflow_results["success"] = False
                    workflow_results["error"] = f"Review stage failed: {review_result.get('error')}"
                    return workflow_results
            
            # Stage 5: Fixing (if review found issues)
            fixer_agent = self.registry.get_agent("fixer")
            if fixer_agent and workflow_results["success"]:
                # Check if review found critical issues
                review_critical = False
                if len(workflow_results["stages"]) > 3:
                    review_result = workflow_results["stages"][3]["result"]
                    if "review_results" in review_result:
                        review_data = review_result["review_results"]
                        critical_issues = review_data.get("quality_metrics", {}).get("critical_issues", 0)
                        if critical_issues > 0:
                            review_critical = True
                
                if review_critical:
                    logger.info("🔧 Stage 5: Fixing Critical Issues")
                    
                    # Extract generated code from coding stage
                    generated_code = ""
                    if len(workflow_results["stages"]) > 1:
                        code_result = workflow_results["stages"][1]["result"]
                        if "code_files" in code_result:
                            generated_code = code_result["code_files"][0].get("content", "")
                    
                    fixing_task = {
                        "id": f"{workflow_id}_fixing",
                        "content": f"Fix critical issues found in code review for: {user_request}",
                        "type": "fixing",
                        "language": "python",
                        "broken_code": generated_code,
                        "error_message": "Critical issues found in code review",
                        "session_id": session_id
                    }
                    
                    fix_result = await fixer_agent.execute(fixing_task)
                    workflow_results["stages"].append({
                        "stage": "fixing",
                        "agent": "fixer",
                        "result": fix_result
                    })
                    
                    if not fix_result.get("success"):
                        workflow_results["success"] = False
                        workflow_results["error"] = f"Fixing stage failed: {fix_result.get('error')}"
                        return workflow_results
            
            # Stage 6: Deployment
            deployer_agent = self.registry.get_agent("deployer")
            if deployer_agent and workflow_results["success"]:
                logger.info("🚀 Stage 6: Deployment")
                
                # Extract final code (either from coding or fixing stage)
                final_code = ""
                if len(workflow_results["stages"]) > 4:  # Has fixing stage
                    fix_result = workflow_results["stages"][4]["result"]
                    if "fix_results" in fix_result:
                        final_code = fix_result["fix_results"].get("fixed_code", "")
                elif len(workflow_results["stages"]) > 1:  # Use coding stage
                    code_result = workflow_results["stages"][1]["result"]
                    if "code_files" in code_result:
                        final_code = code_result["code_files"][0].get("content", "")
                
                deployment_task = {
                    "id": f"{workflow_id}_deployment",
                    "content": f"Create deployment configuration for: {user_request}",
                    "type": "deployment",
                    "platform": "docker",  # Default platform
                    "environment": "development",
                    "project_code": final_code,
                    "session_id": session_id
                }
                
                deployment_result = await deployer_agent.execute(deployment_task)
                workflow_results["stages"].append({
                    "stage": "deployment",
                    "agent": "deployer",
                    "result": deployment_result
                })
                
                if not deployment_result.get("success"):
                    workflow_results["success"] = False
                    workflow_results["error"] = f"Deployment stage failed: {deployment_result.get('error')}"
                    return workflow_results
            
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