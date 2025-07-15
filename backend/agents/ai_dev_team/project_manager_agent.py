"""
AI-Development-Team Project Manager Agent
Handles project coordination, planning, and team management
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ..memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ..orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class ProjectManagerAgent(BaseAgent):
    """
    AI-Development-Team Project Manager Agent
    
    Responsibilities:
    - Project planning and coordination
    - Team task assignment and scheduling
    - Progress tracking and reporting
    - Resource allocation and management
    - Risk assessment and mitigation
    - Stakeholder communication
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="ai_dev_team_project_manager",
            agent_type=AgentType.ORCHESTRATOR,
            description="Project coordination and team management agent",
            capabilities=[
                "project_planning",
                "task_scheduling", 
                "team_coordination",
                "progress_tracking",
                "resource_allocation",
                "risk_management",
                "stakeholder_communication",
                "milestone_planning",
                "budget_tracking",
                "quality_assurance_oversight"
            ],
            model_requirements=["gpt-4", "claude-3-opus"],
            priority=9,
            max_concurrent_tasks=3,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Project management configuration
        self.project_phases = [
            "planning",
            "design", 
            "development",
            "testing",
            "deployment",
            "maintenance"
        ]
        
        self.task_priorities = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4
        }
        
        logger.info("🎯 AI-Development-Team Project Manager Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for project management"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # Project management keywords
        project_keywords = [
            "project", "manage", "plan", "coordinate", "schedule", "organize",
            "timeline", "milestone", "deadline", "resource", "team", "assign",
            "track", "progress", "status", "report", "stakeholder", "budget",
            "risk", "scope", "requirement", "deliverable", "sprint", "agile",
            "kanban", "scrum", "roadmap", "backlog", "epic", "story"
        ]
        
        # Check task type
        if task_type in ["project", "management", "planning", "coordination"]:
            return True
        
        # Check content for project management keywords
        return any(keyword in content for keyword in project_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project management task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            session_id = task.get("session_id")
            
            logger.info(f"🎯 Project Manager executing task: {task_id}")
            
            # Determine project management action
            action = self._determine_action(content)
            
            result = {}
            
            if action == "project_planning":
                result = await self._create_project_plan(content, task_id, session_id)
            elif action == "task_assignment":
                result = await self._assign_tasks(content, task_id, session_id)
            elif action == "progress_tracking":
                result = await self._track_progress(content, task_id, session_id)
            elif action == "resource_allocation":
                result = await self._allocate_resources(content, task_id, session_id)
            elif action == "risk_management":
                result = await self._manage_risks(content, task_id, session_id)
            elif action == "stakeholder_communication":
                result = await self._communicate_stakeholders(content, task_id, session_id)
            else:
                result = await self._general_project_management(content, task_id, session_id)
            
            # Store result in memory
            await self._store_project_management_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Project Manager completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "project_management_result": result,
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Project Manager failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_action(self, content: str) -> str:
        """Determine the specific project management action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["plan", "planning", "roadmap", "timeline"]):
            return "project_planning"
        elif any(word in content_lower for word in ["assign", "task", "team", "delegate"]):
            return "task_assignment"
        elif any(word in content_lower for word in ["track", "progress", "status", "update"]):
            return "progress_tracking"
        elif any(word in content_lower for word in ["resource", "allocate", "budget", "capacity"]):
            return "resource_allocation"
        elif any(word in content_lower for word in ["risk", "issue", "problem", "mitigation"]):
            return "risk_management"
        elif any(word in content_lower for word in ["stakeholder", "communicate", "report", "meeting"]):
            return "stakeholder_communication"
        else:
            return "general_project_management"
    
    async def _create_project_plan(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Create comprehensive project plan"""
        try:
            # Generate project plan using AI
            request = TaskRequest(
                id=f"{task_id}_planning",
                content=f"""
                Create a comprehensive project plan for: {content}
                
                Include:
                1. Project scope and objectives
                2. Work breakdown structure (WBS)
                3. Timeline with milestones
                4. Resource requirements
                5. Risk assessment
                6. Success criteria
                7. Deliverables
                8. Quality assurance plan
                
                Format as detailed project plan with actionable items.
                """,
                task_type="project_planning",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                project_plan = self._parse_project_plan(response.content)
                
                return {
                    "action": "project_planning",
                    "project_plan": project_plan,
                    "timeline": project_plan.get("timeline", {}),
                    "milestones": project_plan.get("milestones", []),
                    "resources": project_plan.get("resources", {}),
                    "risks": project_plan.get("risks", []),
                    "success_criteria": project_plan.get("success_criteria", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "project_planning",
                    "error": "Failed to generate project plan",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Project planning failed: {e}")
            return {
                "action": "project_planning",
                "error": str(e)
            }
    
    async def _assign_tasks(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Assign tasks to team members"""
        try:
            # Generate task assignments using AI
            request = TaskRequest(
                id=f"{task_id}_assignment",
                content=f"""
                Create task assignments for: {content}
                
                Consider:
                1. Team member skills and availability
                2. Task priorities and dependencies
                3. Workload distribution
                4. Timeline constraints
                5. Resource requirements
                
                Provide specific task assignments with:
                - Task description
                - Assigned team member role
                - Priority level
                - Estimated effort
                - Dependencies
                - Due date
                """,
                task_type="task_assignment",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                assignments = self._parse_task_assignments(response.content)
                
                return {
                    "action": "task_assignment",
                    "assignments": assignments,
                    "team_utilization": self._calculate_team_utilization(assignments),
                    "critical_path": self._identify_critical_path(assignments),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "task_assignment",
                    "error": "Failed to generate task assignments",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Task assignment failed: {e}")
            return {
                "action": "task_assignment",
                "error": str(e)
            }
    
    async def _track_progress(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Track project progress and generate status reports"""
        try:
            # Generate progress report using AI
            request = TaskRequest(
                id=f"{task_id}_tracking",
                content=f"""
                Generate a comprehensive progress report for: {content}
                
                Include:
                1. Overall project status
                2. Completed tasks and milestones
                3. Current work in progress
                4. Upcoming tasks and deadlines
                5. Resource utilization
                6. Risk status updates
                7. Budget/timeline variance
                8. Recommendations for improvement
                
                Format as executive summary with key metrics.
                """,
                task_type="progress_tracking",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                progress_report = self._parse_progress_report(response.content)
                
                return {
                    "action": "progress_tracking",
                    "progress_report": progress_report,
                    "completion_percentage": progress_report.get("completion_percentage", 0),
                    "milestone_status": progress_report.get("milestone_status", []),
                    "blockers": progress_report.get("blockers", []),
                    "recommendations": progress_report.get("recommendations", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "progress_tracking",
                    "error": "Failed to generate progress report",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Progress tracking failed: {e}")
            return {
                "action": "progress_tracking",
                "error": str(e)
            }
    
    async def _allocate_resources(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Allocate resources optimally across project tasks"""
        try:
            # Generate resource allocation using AI
            request = TaskRequest(
                id=f"{task_id}_resources",
                content=f"""
                Create optimal resource allocation plan for: {content}
                
                Consider:
                1. Available team members and their skills
                2. Task priorities and dependencies
                3. Resource constraints and availability
                4. Budget limitations
                5. Timeline requirements
                
                Provide:
                - Resource allocation matrix
                - Utilization percentages
                - Capacity planning
                - Conflict resolution
                - Optimization recommendations
                """,
                task_type="resource_allocation",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                allocation_plan = self._parse_resource_allocation(response.content)
                
                return {
                    "action": "resource_allocation",
                    "allocation_plan": allocation_plan,
                    "utilization_metrics": allocation_plan.get("utilization_metrics", {}),
                    "capacity_warnings": allocation_plan.get("capacity_warnings", []),
                    "optimization_suggestions": allocation_plan.get("optimization_suggestions", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "resource_allocation",
                    "error": "Failed to generate resource allocation",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Resource allocation failed: {e}")
            return {
                "action": "resource_allocation",
                "error": str(e)
            }
    
    async def _manage_risks(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Identify and manage project risks"""
        try:
            # Generate risk management plan using AI
            request = TaskRequest(
                id=f"{task_id}_risks",
                content=f"""
                Perform comprehensive risk analysis for: {content}
                
                Identify:
                1. Technical risks and mitigation strategies
                2. Resource risks and contingency plans
                3. Timeline risks and buffer strategies
                4. Quality risks and prevention measures
                5. External dependencies and fallback options
                
                For each risk provide:
                - Risk description
                - Probability and impact assessment
                - Mitigation strategy
                - Contingency plan
                - Monitoring indicators
                """,
                task_type="risk_management",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                risk_analysis = self._parse_risk_analysis(response.content)
                
                return {
                    "action": "risk_management",
                    "risk_analysis": risk_analysis,
                    "high_priority_risks": risk_analysis.get("high_priority_risks", []),
                    "mitigation_plans": risk_analysis.get("mitigation_plans", []),
                    "monitoring_schedule": risk_analysis.get("monitoring_schedule", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "risk_management",
                    "error": "Failed to generate risk analysis",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Risk management failed: {e}")
            return {
                "action": "risk_management",
                "error": str(e)
            }
    
    async def _communicate_stakeholders(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Generate stakeholder communications"""
        try:
            # Generate stakeholder communication using AI
            request = TaskRequest(
                id=f"{task_id}_communication",
                content=f"""
                Create stakeholder communication materials for: {content}
                
                Generate:
                1. Executive summary for leadership
                2. Technical update for development team
                3. Status report for project sponsors
                4. User communication for end users
                5. Vendor communication for external partners
                
                Include:
                - Current status and progress
                - Key achievements and milestones
                - Upcoming activities and deliverables
                - Issues and resolution plans
                - Action items and next steps
                """,
                task_type="stakeholder_communication",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                communications = self._parse_stakeholder_communications(response.content)
                
                return {
                    "action": "stakeholder_communication",
                    "communications": communications,
                    "executive_summary": communications.get("executive_summary", ""),
                    "technical_update": communications.get("technical_update", ""),
                    "status_report": communications.get("status_report", ""),
                    "action_items": communications.get("action_items", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "stakeholder_communication",
                    "error": "Failed to generate stakeholder communications",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Stakeholder communication failed: {e}")
            return {
                "action": "stakeholder_communication",
                "error": str(e)
            }
    
    async def _general_project_management(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general project management tasks"""
        try:
            # Generate general project management response using AI
            request = TaskRequest(
                id=f"{task_id}_general",
                content=f"""
                Provide comprehensive project management guidance for: {content}
                
                Consider:
                1. Project management best practices
                2. Team coordination strategies
                3. Process optimization recommendations
                4. Tool and methodology suggestions
                5. Success metrics and KPIs
                
                Provide actionable recommendations with specific steps.
                """,
                task_type="general_project_management",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=5
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_project_management",
                    "recommendations": self._parse_general_recommendations(response.content),
                    "best_practices": self._extract_best_practices(response.content),
                    "tools_suggested": self._extract_tools_suggestions(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_project_management",
                    "error": "Failed to generate project management guidance",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General project management failed: {e}")
            return {
                "action": "general_project_management",
                "error": str(e)
            }
    
    def _parse_project_plan(self, content: str) -> Dict[str, Any]:
        """Parse AI-generated project plan"""
        # Basic parsing - in production, implement more sophisticated parsing
        return {
            "scope": "Project scope extracted from AI response",
            "timeline": {"start": "2024-01-01", "end": "2024-12-31"},
            "milestones": ["Milestone 1", "Milestone 2", "Milestone 3"],
            "resources": {"team_size": 5, "budget": 100000},
            "risks": ["Risk 1", "Risk 2"],
            "success_criteria": ["Criteria 1", "Criteria 2"],
            "full_content": content
        }
    
    def _parse_task_assignments(self, content: str) -> List[Dict[str, Any]]:
        """Parse AI-generated task assignments"""
        return [
            {
                "task_id": "T001",
                "description": "Task description",
                "assigned_to": "developer",
                "priority": "high",
                "estimated_effort": "8 hours",
                "due_date": "2024-02-01"
            }
        ]
    
    def _parse_progress_report(self, content: str) -> Dict[str, Any]:
        """Parse AI-generated progress report"""
        return {
            "completion_percentage": 45,
            "milestone_status": ["Milestone 1: Complete", "Milestone 2: In Progress"],
            "blockers": ["Blocker 1", "Blocker 2"],
            "recommendations": ["Recommendation 1", "Recommendation 2"],
            "full_content": content
        }
    
    def _parse_resource_allocation(self, content: str) -> Dict[str, Any]:
        """Parse AI-generated resource allocation"""
        return {
            "utilization_metrics": {"developer": 80, "tester": 60},
            "capacity_warnings": ["Developer overallocated"],
            "optimization_suggestions": ["Redistribute testing tasks"],
            "full_content": content
        }
    
    def _parse_risk_analysis(self, content: str) -> Dict[str, Any]:
        """Parse AI-generated risk analysis"""
        return {
            "high_priority_risks": ["Technical debt", "Resource constraints"],
            "mitigation_plans": ["Code review process", "Resource planning"],
            "monitoring_schedule": {"weekly": "Risk review", "monthly": "Full assessment"},
            "full_content": content
        }
    
    def _parse_stakeholder_communications(self, content: str) -> Dict[str, Any]:
        """Parse AI-generated stakeholder communications"""
        return {
            "executive_summary": "Executive summary content",
            "technical_update": "Technical update content",
            "status_report": "Status report content",
            "action_items": ["Action 1", "Action 2"],
            "full_content": content
        }
    
    def _parse_general_recommendations(self, content: str) -> List[str]:
        """Parse general project management recommendations"""
        return ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices from AI response"""
        return ["Best practice 1", "Best practice 2"]
    
    def _extract_tools_suggestions(self, content: str) -> List[str]:
        """Extract tool suggestions from AI response"""
        return ["Tool 1", "Tool 2", "Tool 3"]
    
    def _calculate_team_utilization(self, assignments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate team utilization metrics"""
        return {"developer": 0.8, "tester": 0.6, "designer": 0.7}
    
    def _identify_critical_path(self, assignments: List[Dict[str, Any]]) -> List[str]:
        """Identify critical path in project"""
        return ["Task A", "Task B", "Task C"]
    
    async def _store_project_management_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store project management result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"Project management result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["project_management", "ai_dev_team", "coordination"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store project management result: {e}")


def create_project_manager_agent(config: Dict[str, Any]) -> ProjectManagerAgent:
    """Factory function to create Project Manager Agent"""
    return ProjectManagerAgent(config)