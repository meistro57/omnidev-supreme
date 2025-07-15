"""
The-Agency Architect Agent Integration
Migrated from /home/mark/The-Agency/agents/architect.py
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class ArchitectAgent(BaseAgent):
    """
    Architect Agent - Breaks down complex requests into structured development plans
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="architect",
            agent_type=AgentType.ARCHITECT,
            description="Breaks down complex requests into structured development plans",
            capabilities=[
                "project_planning",
                "architecture_design",
                "task_decomposition",
                "requirement_analysis",
                "technology_selection"
            ],
            model_requirements=["text_generation", "reasoning", "analysis"],
            priority=9,  # High priority for planning
            max_concurrent_tasks=3,
            timeout_seconds=300
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        logger.info("🏗️  Architect Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for architect agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires planning/architecture
        planning_keywords = [
            "create", "build", "design", "plan", "architect", "structure",
            "develop", "implement", "system", "application", "project"
        ]
        
        return any(keyword in content for keyword in planning_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute architectural planning task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            project_context = task.get("context", {})
            session_id = task.get("session_id")
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Architecture task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "architect",
                    "task_id": task.get("id"),
                    "project_context": project_context
                },
                session_id=session_id
            )
            
            # Create planning prompt
            planning_prompt = self._create_planning_prompt(user_request, project_context)
            
            # Use orchestrator to generate plan
            orchestrator_request = TaskRequest(
                id=f"architect_{task.get('id', 'unknown')}",
                content=planning_prompt,
                task_type="analysis",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.REASONING,
                    ModelCapability.ANALYSIS
                ],
                max_tokens=2000,
                temperature=0.3,  # Lower temperature for consistent planning
                priority=8,
                metadata={
                    "agent": "architect",
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Planning failed: {response.error}")
            
            # Parse the generated plan
            plan = self._parse_plan(response.content)
            
            # Store plan in memory
            plan_memory_id = self.memory_manager.store_memory(
                content=f"Architecture plan: {json.dumps(plan, indent=2)}",
                memory_type=MemoryType.PROJECT,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "architect",
                    "task_id": task.get("id"),
                    "plan_structure": plan,
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["architecture", "plan", "project"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "plan": plan,
                "memory_ids": [task_memory_id, plan_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "architect",
                "metadata": {
                    "planning_approach": "structured_decomposition",
                    "complexity_level": "complex",
                    "plan_quality": "high"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Architect agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "architect"
            }
    
    def _create_planning_prompt(self, user_request: str, context: Dict[str, Any]) -> str:
        """Create detailed planning prompt"""
        context_str = ""
        if context:
            context_str = f"\n\nProject Context:\n{json.dumps(context, indent=2)}"
        
        return f"""
As an expert software architect, analyze the following request and create a comprehensive development plan.

User Request: {user_request}{context_str}

Please provide a structured plan with the following sections:

1. **PROJECT OVERVIEW**
   - Brief description of the project
   - Main objectives and goals
   - Target audience/users

2. **TECHNICAL REQUIREMENTS**
   - Programming languages and frameworks
   - Database requirements
   - External APIs or services
   - Infrastructure needs

3. **ARCHITECTURE DESIGN**
   - High-level system architecture
   - Key components and their relationships
   - Data flow and processing
   - Security considerations

4. **DEVELOPMENT PHASES**
   - Phase 1: Core foundation
   - Phase 2: Main features
   - Phase 3: Advanced features
   - Phase 4: Testing and deployment

5. **IMPLEMENTATION TASKS**
   - Specific tasks for each phase
   - Dependencies between tasks
   - Estimated complexity (simple/medium/complex)
   - Priority levels

6. **TESTING STRATEGY**
   - Unit testing approach
   - Integration testing
   - End-to-end testing
   - Performance testing

7. **DEPLOYMENT PLAN**
   - Environment setup
   - Deployment strategy
   - Monitoring and maintenance

Please format your response as a well-structured plan that can be easily parsed and executed by development agents.
"""
    
    def _parse_plan(self, plan_content: str) -> Dict[str, Any]:
        """Parse the generated plan into structured format"""
        try:
            # Try to extract structured information from the plan
            plan = {
                "overview": self._extract_section(plan_content, "PROJECT OVERVIEW"),
                "technical_requirements": self._extract_section(plan_content, "TECHNICAL REQUIREMENTS"),
                "architecture": self._extract_section(plan_content, "ARCHITECTURE DESIGN"),
                "phases": self._extract_phases(plan_content),
                "tasks": self._extract_tasks(plan_content),
                "testing": self._extract_section(plan_content, "TESTING STRATEGY"),
                "deployment": self._extract_section(plan_content, "DEPLOYMENT PLAN"),
                "raw_content": plan_content
            }
            
            return plan
            
        except Exception as e:
            logger.warning(f"⚠️  Plan parsing failed, returning raw content: {e}")
            return {
                "raw_content": plan_content,
                "parsed": False,
                "error": str(e)
            }
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the plan"""
        try:
            lines = content.split('\n')
            section_lines = []
            capturing = False
            
            for line in lines:
                if section_name in line.upper():
                    capturing = True
                    continue
                elif capturing and line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '##')):
                    break
                elif capturing:
                    section_lines.append(line)
            
            return '\n'.join(section_lines).strip()
            
        except Exception:
            return ""
    
    def _extract_phases(self, content: str) -> List[Dict[str, Any]]:
        """Extract development phases from the plan"""
        phases = []
        try:
            phase_section = self._extract_section(content, "DEVELOPMENT PHASES")
            if phase_section:
                lines = phase_section.split('\n')
                current_phase = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('- Phase') or line.startswith('Phase'):
                        if current_phase:
                            phases.append(current_phase)
                        current_phase = {
                            "name": line,
                            "description": "",
                            "tasks": []
                        }
                    elif current_phase and line:
                        current_phase["description"] += line + " "
                
                if current_phase:
                    phases.append(current_phase)
                    
        except Exception as e:
            logger.warning(f"⚠️  Phase extraction failed: {e}")
        
        return phases
    
    def _extract_tasks(self, content: str) -> List[Dict[str, Any]]:
        """Extract implementation tasks from the plan"""
        tasks = []
        try:
            task_section = self._extract_section(content, "IMPLEMENTATION TASKS")
            if task_section:
                lines = task_section.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('-') or line.startswith('*'):
                        task_content = line[1:].strip()
                        if task_content:
                            tasks.append({
                                "description": task_content,
                                "complexity": self._estimate_complexity(task_content),
                                "priority": self._estimate_priority(task_content),
                                "dependencies": []
                            })
                            
        except Exception as e:
            logger.warning(f"⚠️  Task extraction failed: {e}")
        
        return tasks
    
    def _estimate_complexity(self, task_description: str) -> str:
        """Estimate task complexity based on description"""
        description_lower = task_description.lower()
        
        complex_keywords = ["integrate", "complex", "algorithm", "optimization", "security", "scalability"]
        medium_keywords = ["implement", "create", "build", "design", "configure"]
        
        if any(keyword in description_lower for keyword in complex_keywords):
            return "complex"
        elif any(keyword in description_lower for keyword in medium_keywords):
            return "medium"
        else:
            return "simple"
    
    def _estimate_priority(self, task_description: str) -> str:
        """Estimate task priority based on description"""
        description_lower = task_description.lower()
        
        high_keywords = ["core", "foundation", "critical", "essential", "security"]
        low_keywords = ["optional", "enhancement", "nice-to-have", "future"]
        
        if any(keyword in description_lower for keyword in high_keywords):
            return "high"
        elif any(keyword in description_lower for keyword in low_keywords):
            return "low"
        else:
            return "medium"
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context from memory"""
        try:
            context_items = self.memory_manager.search_memory(
                query="project context architecture",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=5
            )
            
            context = {}
            for item in context_items:
                if "plan_structure" in item.metadata:
                    context["previous_plans"] = item.metadata["plan_structure"]
                if "project_context" in item.metadata:
                    context.update(item.metadata["project_context"])
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get architect agent statistics"""
        return {
            **self.stats,
            "memory_items": len(self.memory_manager.search_memory(
                query="architect",
                memory_type=MemoryType.AGENT,
                limit=100
            )),
            "planning_approach": "structured_decomposition",
            "supported_project_types": [
                "web_applications",
                "mobile_apps",
                "desktop_applications",
                "apis",
                "microservices",
                "databases",
                "ai_systems"
            ]
        }


def create_architect_agent(config: Dict[str, Any]) -> ArchitectAgent:
    """Factory function to create architect agent"""
    return ArchitectAgent(config)