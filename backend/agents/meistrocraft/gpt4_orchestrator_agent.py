"""
MeistroCraft GPT-4 Orchestrator Agent Integration
Migrated from /home/mark/MeistroCraft/main.py
"""

import asyncio
import json
import os
import subprocess
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class GPT4OrchestratorAgent(BaseAgent):
    """
    GPT-4 Orchestrator Agent - Strategic task planning and orchestration
    Integrated from MeistroCraft system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="gpt4_orchestrator",
            agent_type=AgentType.ORCHESTRATOR,
            description="Strategic task planning and orchestration using GPT-4",
            capabilities=[
                "strategic_planning",
                "task_decomposition",
                "multi_agent_orchestration",
                "project_management",
                "resource_allocation",
                "workflow_optimization",
                "session_management",
                "context_coordination"
            ],
            model_requirements=["reasoning", "planning", "text_generation"],
            priority=10,  # Highest priority for orchestration
            max_concurrent_tasks=5,
            timeout_seconds=600  # Longer timeout for strategic planning
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Initialize OpenAI client
        self.openai_client = None
        if OpenAI and config.get("openai_api_key"):
            self.openai_client = OpenAI(api_key=config["openai_api_key"])
        
        # MeistroCraft-specific configuration
        self.meistrocraft_config = {
            "task_generation_model": "gpt-4o",
            "max_tasks_per_request": 10,
            "orchestration_style": "strategic",
            "session_persistence": True,
            "multi_agent_coordination": True
        }
        
        # Task orchestration patterns
        self.orchestration_patterns = {
            "sequential": "Execute tasks one after another",
            "parallel": "Execute tasks simultaneously where possible",
            "hierarchical": "Break down into subtasks with dependencies",
            "adaptive": "Adjust execution based on results",
            "collaborative": "Coordinate multiple agents"
        }
        
        logger.info("🎯 GPT-4 Orchestrator Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for orchestrator agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires orchestration
        orchestration_keywords = [
            "plan", "orchestrate", "coordinate", "manage", "organize",
            "strategy", "workflow", "process", "pipeline", "system"
        ]
        
        return any(keyword in content for keyword in orchestration_keywords) or task_type == "orchestration"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestration task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            session_id = task.get("session_id")
            orchestration_style = task.get("orchestration_style", "adaptive")
            
            # Get project context
            context = await self.get_project_context(session_id)
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"GPT-4 Orchestration task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "gpt4_orchestrator",
                    "task_id": task.get("id"),
                    "orchestration_style": orchestration_style,
                    "session_id": session_id
                },
                session_id=session_id
            )
            
            # Create orchestration prompt
            orchestration_prompt = self._create_orchestration_prompt(
                user_request, orchestration_style, context
            )
            
            # Generate strategic plan using GPT-4
            strategic_plan = await self._generate_strategic_plan(
                orchestration_prompt, task.get("id", "unknown")
            )
            
            # Process and structure the plan
            structured_plan = self._structure_orchestration_plan(strategic_plan)
            
            # Create agent assignments
            agent_assignments = self._create_agent_assignments(structured_plan)
            
            # Store orchestration plan in memory
            plan_memory_id = self.memory_manager.store_memory(
                content=f"Strategic orchestration plan: {json.dumps(structured_plan, indent=2)}",
                memory_type=MemoryType.PROJECT,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "gpt4_orchestrator",
                    "task_id": task.get("id"),
                    "orchestration_style": orchestration_style,
                    "agent_assignments": agent_assignments,
                    "task_count": len(structured_plan.get("tasks", [])),
                    "estimated_duration": structured_plan.get("estimated_duration", 0)
                },
                tags=["orchestration", "strategic_plan", orchestration_style],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "orchestration_plan": structured_plan,
                "agent_assignments": agent_assignments,
                "orchestration_style": orchestration_style,
                "memory_ids": [task_memory_id, plan_memory_id],
                "response_time": execution_time,
                "agent": "gpt4_orchestrator",
                "metadata": {
                    "planning_quality": "strategic",
                    "coordination_level": "high",
                    "agent_coordination": True,
                    "task_optimization": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ GPT-4 Orchestrator agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "agent": "gpt4_orchestrator"
            }
    
    async def _generate_strategic_plan(self, prompt: str, task_id: str) -> Dict[str, Any]:
        """Generate strategic plan using GPT-4"""
        try:
            if self.openai_client:
                # Use OpenAI directly for specialized orchestration
                response = self.openai_client.chat.completions.create(
                    model=self.meistrocraft_config["task_generation_model"],
                    messages=[
                        {
                            "role": "system",
                            "content": """You are an expert strategic orchestrator and project manager. 
                            Your role is to create comprehensive, actionable plans that coordinate multiple AI agents 
                            and resources to achieve complex goals efficiently."""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=2000,
                    temperature=0.3,  # Lower temperature for consistent planning
                    response_format={"type": "json_object"}
                )
                
                plan_content = response.choices[0].message.content
                return json.loads(plan_content)
            else:
                # Fallback to unified orchestrator
                orchestrator_request = TaskRequest(
                    id=f"gpt4_orchestrator_{task_id}",
                    content=prompt,
                    task_type="planning",
                    complexity=TaskComplexity.EXPERT,
                    required_capabilities=[
                        ModelCapability.REASONING,
                        ModelCapability.PLANNING,
                        ModelCapability.TEXT_GENERATION
                    ],
                    max_tokens=2000,
                    temperature=0.3,
                    priority=10,
                    metadata={
                        "agent": "gpt4_orchestrator",
                        "specialized_planning": True
                    }
                )
                
                response = await self.orchestrator.execute_task(orchestrator_request)
                
                if not response.success:
                    raise Exception(f"Strategic planning failed: {response.error}")
                
                return json.loads(response.content)
                
        except Exception as e:
            logger.error(f"❌ Strategic plan generation failed: {e}")
            raise
    
    def _create_orchestration_prompt(self, user_request: str, orchestration_style: str, context: Dict[str, Any]) -> str:
        """Create detailed orchestration prompt"""
        context_str = ""
        if context.get("project_info"):
            context_str = f"\n\nProject Context:\n{json.dumps(context['project_info'], indent=2)}"
        
        pattern_description = self.orchestration_patterns.get(orchestration_style, "Adaptive execution approach")
        
        return f"""
As an expert strategic orchestrator, create a comprehensive plan for the following request using {orchestration_style} orchestration.

Request: {user_request}

Orchestration Style: {orchestration_style}
Pattern: {pattern_description}

Available Agent Types:
- Architect: Project planning and architecture design
- Coder: Multi-language code generation
- Tester: Comprehensive testing and validation
- Reviewer: Code quality and security analysis
- Fixer: Bug resolution and optimization
- Deployer: Deployment and DevOps automation{context_str}

Create a strategic orchestration plan as JSON with the following structure:

{{
  "project_overview": {{
    "title": "Project title",
    "description": "Brief description",
    "complexity": "simple|medium|complex|expert",
    "estimated_duration": "duration in minutes",
    "success_criteria": ["criterion1", "criterion2"]
  }},
  "orchestration_strategy": {{
    "approach": "{orchestration_style}",
    "coordination_pattern": "pattern description",
    "resource_allocation": "allocation strategy",
    "risk_mitigation": "risk management approach"
  }},
  "tasks": [
    {{
      "id": "task_1",
      "title": "Task title",
      "description": "Detailed task description",
      "assigned_agent": "agent_name",
      "priority": "high|medium|low",
      "dependencies": ["task_id1", "task_id2"],
      "estimated_time": "time in minutes",
      "inputs": ["required inputs"],
      "outputs": ["expected outputs"],
      "success_criteria": ["criteria"],
      "parallel_execution": true/false
    }}
  ],
  "dependencies": {{
    "task_id": ["dependency_task_ids"]
  }},
  "resource_requirements": {{
    "agents": ["required_agents"],
    "models": ["required_models"],
    "tools": ["required_tools"]
  }},
  "quality_gates": [
    {{
      "checkpoint": "checkpoint_name",
      "criteria": ["quality criteria"],
      "required_score": "minimum score"
    }}
  ],
  "monitoring": {{
    "key_metrics": ["metrics to track"],
    "checkpoints": ["milestone checkpoints"],
    "alerts": ["alert conditions"]
  }},
  "contingency_plans": [
    {{
      "scenario": "failure scenario",
      "mitigation": "mitigation strategy",
      "fallback": "fallback plan"
    }}
  ]
}}

Focus on:
1. Strategic thinking and high-level coordination
2. Efficient resource allocation and agent utilization
3. Risk management and contingency planning
4. Quality assurance and success metrics
5. Scalable and maintainable execution patterns
"""
    
    def _structure_orchestration_plan(self, raw_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Structure and validate the orchestration plan"""
        try:
            # Validate required fields
            required_fields = ["project_overview", "orchestration_strategy", "tasks"]
            for field in required_fields:
                if field not in raw_plan:
                    logger.warning(f"Missing required field: {field}")
                    raw_plan[field] = {}
            
            # Ensure tasks have required fields
            for task in raw_plan.get("tasks", []):
                if "id" not in task:
                    task["id"] = str(uuid.uuid4())
                if "assigned_agent" not in task:
                    task["assigned_agent"] = "coder"  # Default agent
                if "priority" not in task:
                    task["priority"] = "medium"
                if "dependencies" not in task:
                    task["dependencies"] = []
                if "parallel_execution" not in task:
                    task["parallel_execution"] = False
            
            # Add orchestration metadata
            raw_plan["orchestration_metadata"] = {
                "created_at": datetime.now().isoformat(),
                "orchestrator": "gpt4_orchestrator",
                "version": "1.0",
                "total_tasks": len(raw_plan.get("tasks", [])),
                "estimated_duration": raw_plan.get("project_overview", {}).get("estimated_duration", 0)
            }
            
            return raw_plan
            
        except Exception as e:
            logger.error(f"❌ Plan structuring failed: {e}")
            return {
                "project_overview": {"title": "Emergency Plan", "description": "Fallback plan"},
                "orchestration_strategy": {"approach": "sequential"},
                "tasks": [{"id": "fallback_task", "title": "Execute request", "assigned_agent": "coder"}],
                "orchestration_metadata": {"created_at": datetime.now().isoformat(), "fallback": True}
            }
    
    def _create_agent_assignments(self, plan: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create agent assignments from orchestration plan"""
        assignments = {}
        
        for task in plan.get("tasks", []):
            agent = task.get("assigned_agent", "coder")
            if agent not in assignments:
                assignments[agent] = []
            assignments[agent].append(task.get("id", "unknown"))
        
        return assignments
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context for orchestration"""
        try:
            # Get recent orchestration plans
            plan_items = self.memory_manager.search_memory(
                query="orchestration plan",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=3
            )
            
            # Get session context
            session_items = self.memory_manager.search_memory(
                query="session context",
                memory_type=MemoryType.SESSION,
                use_vector=True,
                limit=2
            )
            
            context = {
                "project_info": {},
                "previous_plans": [],
                "session_context": {},
                "available_agents": ["architect", "coder", "tester", "reviewer", "fixer", "deployer"]
            }
            
            # Extract previous plans
            for item in plan_items:
                if "orchestration_style" in item.metadata:
                    context["previous_plans"].append({
                        "style": item.metadata["orchestration_style"],
                        "task_count": item.metadata.get("task_count", 0),
                        "created_at": item.created_at.isoformat()
                    })
            
            # Extract session context
            for item in session_items:
                if "session_id" in item.metadata:
                    context["session_context"] = {
                        "session_id": item.metadata["session_id"],
                        "created_at": item.created_at.isoformat()
                    }
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get orchestrator agent statistics"""
        return {
            **self.stats,
            "orchestration_patterns": list(self.orchestration_patterns.keys()),
            "meistrocraft_config": self.meistrocraft_config,
            "plans_created": len(self.memory_manager.search_memory(
                query="gpt4_orchestrator",
                memory_type=MemoryType.PROJECT,
                limit=1000
            )),
            "orchestration_capabilities": [
                "strategic_planning",
                "multi_agent_coordination",
                "resource_optimization",
                "risk_management",
                "quality_assurance",
                "workflow_automation"
            ]
        }


def create_gpt4_orchestrator_agent(config: Dict[str, Any]) -> GPT4OrchestratorAgent:
    """Factory function to create GPT-4 orchestrator agent"""
    return GPT4OrchestratorAgent(config)