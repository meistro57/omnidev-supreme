"""
OBELISK Code Architect Agent
Generates high-level architecture plans and system designs
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class CodeArchitectAgent(BaseAgent):
    """
    OBELISK Code Architect Agent
    
    Specializes in:
    - Software architecture design
    - System component planning
    - Technology stack selection
    - High-level system overview
    - Architecture documentation
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="code_architect",
            agent_type=AgentType.ARCHITECT,
            description="OBELISK Code Architect - Generates high-level architecture plans and system designs",
            capabilities=[
                "software_architecture_design",
                "system_component_planning", 
                "technology_stack_selection",
                "high_level_system_overview",
                "architecture_documentation",
                "component_relationship_mapping",
                "scalability_planning",
                "performance_architecture"
            ],
            model_requirements=["reasoning", "analysis", "planning"],
            priority=10,
            max_concurrent_tasks=2,
            timeout_seconds=600,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Architecture generation parameters
        self.architecture_templates = {
            "web_application": {
                "layers": ["frontend", "backend", "database", "cache", "monitoring"],
                "patterns": ["MVC", "microservices", "RESTful_API", "event_driven"],
                "components": ["authentication", "routing", "business_logic", "data_access"]
            },
            "microservice": {
                "layers": ["api_gateway", "services", "database", "message_queue", "monitoring"],
                "patterns": ["domain_driven_design", "CQRS", "event_sourcing", "saga"],
                "components": ["service_discovery", "load_balancing", "circuit_breaker", "config_management"]
            },
            "data_processing": {
                "layers": ["ingestion", "processing", "storage", "analytics", "visualization"],
                "patterns": ["ETL", "stream_processing", "batch_processing", "lambda_architecture"],
                "components": ["data_validation", "transformation", "aggregation", "monitoring"]
            },
            "ai_system": {
                "layers": ["data_layer", "model_layer", "inference_layer", "api_layer", "monitoring"],
                "patterns": ["ML_pipeline", "model_serving", "feature_store", "experiment_tracking"],
                "components": ["data_preprocessing", "model_training", "model_deployment", "monitoring"]
            }
        }
        
        logger.info(f"🏗️ {self.metadata.name} initialized with OBELISK architecture capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for code architect agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires architecture planning
        architecture_keywords = [
            "architecture", "design", "structure", "system", "plan", "architect",
            "component", "module", "framework", "pattern", "blueprint", "schema"
        ]
        
        return any(keyword in content for keyword in architecture_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute architecture design task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"arch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"🏗️ Starting architecture design: {task_id}")
            
            # Extract task parameters
            project_name = task.get("project_name", "Unknown Project")
            requirements = task.get("content", "")
            project_type = task.get("project_type", "web_application")
            constraints = task.get("constraints", {})
            context = task.get("context", {})
            
            # Generate architecture plan
            architecture_plan = await self._generate_architecture_plan(
                project_name=project_name,
                requirements=requirements,
                project_type=project_type,
                constraints=constraints,
                context=context
            )
            
            # Store results in memory
            await self._store_architecture_results(
                task_id=task_id,
                project_name=project_name,
                architecture_plan=architecture_plan,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "architecture_plan": architecture_plan,
                "project_name": project_name,
                "project_type": project_type,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"arch_{task_id}",
                "tokens_used": architecture_plan.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Architecture design completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Architecture design failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_architecture_plan(
        self, 
        project_name: str,
        requirements: str,
        project_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive architecture plan"""
        
        # Get architecture template
        template = self.architecture_templates.get(project_type, self.architecture_templates["web_application"])
        
        # Prepare architecture prompt
        architecture_prompt = self._create_architecture_prompt(
            project_name=project_name,
            requirements=requirements,
            template=template,
            constraints=constraints,
            context=context
        )
        
        # Generate architecture using best available model
        try:
            response = await self.orchestrator.generate_response(
                prompt=architecture_prompt,
                model_preference=["claude-3.5-sonnet", "gpt-4", "gpt-3.5-turbo"],
                temperature=0.1,  # Low temperature for consistent architecture
                max_tokens=4000
            )
            
            # Parse and structure architecture response
            architecture_plan = await self._parse_architecture_response(
                response=response,
                project_name=project_name,
                template=template
            )
            
            return architecture_plan
            
        except Exception as e:
            logger.error(f"❌ Architecture generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_plan": self._create_fallback_architecture(project_name, template)
            }
    
    def _create_architecture_prompt(
        self,
        project_name: str,
        requirements: str,
        template: Dict[str, Any],
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed architecture prompt"""
        
        return f"""
You are an expert software architect tasked with designing a comprehensive architecture for a software project.

PROJECT DETAILS:
- Project Name: {project_name}
- Requirements: {requirements}
- Project Type: {template}
- Constraints: {constraints}
- Context: {context}

ARCHITECTURE REQUIREMENTS:
1. Design a scalable, maintainable architecture
2. Consider performance, security, and reliability
3. Include detailed component descriptions
4. Specify technology stack recommendations
5. Define data flow and communication patterns
6. Include deployment and monitoring considerations

EXPECTED ARCHITECTURE LAYERS:
{chr(10).join(f"- {layer}" for layer in template.get("layers", []))}

RECOMMENDED PATTERNS:
{chr(10).join(f"- {pattern}" for pattern in template.get("patterns", []))}

CORE COMPONENTS:
{chr(10).join(f"- {component}" for component in template.get("components", []))}

Please provide a comprehensive architecture plan in the following JSON format:
{{
    "project_overview": {{
        "name": "project name",
        "description": "brief description",
        "goals": ["goal1", "goal2"],
        "success_criteria": ["criteria1", "criteria2"]
    }},
    "technology_stack": {{
        "frontend": ["technologies"],
        "backend": ["technologies"],
        "database": ["technologies"],
        "infrastructure": ["technologies"],
        "monitoring": ["technologies"]
    }},
    "system_architecture": {{
        "layers": [
            {{
                "name": "layer name",
                "purpose": "description",
                "components": ["component1", "component2"],
                "technologies": ["tech1", "tech2"]
            }}
        ],
        "data_flow": "description of data flow",
        "communication_patterns": ["pattern1", "pattern2"]
    }},
    "components": [
        {{
            "name": "component name",
            "type": "component type",
            "purpose": "description",
            "interfaces": ["interface1", "interface2"],
            "dependencies": ["dep1", "dep2"],
            "scalability": "scaling strategy"
        }}
    ],
    "deployment": {{
        "strategy": "deployment strategy",
        "environments": ["dev", "staging", "prod"],
        "infrastructure": "infrastructure description",
        "monitoring": "monitoring strategy"
    }},
    "security": {{
        "authentication": "auth strategy",
        "authorization": "authz strategy",
        "data_protection": "data protection measures",
        "network_security": "network security measures"
    }},
    "performance": {{
        "scalability": "scalability approach",
        "caching": "caching strategy",
        "optimization": "optimization techniques",
        "monitoring": "performance monitoring"
    }},
    "risks_and_mitigations": [
        {{
            "risk": "risk description",
            "impact": "high/medium/low",
            "mitigation": "mitigation strategy"
        }}
    ],
    "implementation_phases": [
        {{
            "phase": "phase name",
            "duration": "estimated duration",
            "deliverables": ["deliverable1", "deliverable2"],
            "dependencies": ["dependency1", "dependency2"]
        }}
    ]
}}

Provide a detailed, practical architecture that can be implemented by a development team.
"""
    
    async def _parse_architecture_response(
        self,
        response: str,
        project_name: str,
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse and validate architecture response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            architecture_data = json.loads(json_str)
            
            # Validate and enhance architecture data
            architecture_plan = {
                "success": True,
                "project_name": project_name,
                "architecture_type": template,
                "generated_at": datetime.now().isoformat(),
                "plan": architecture_data,
                "metadata": {
                    "layers_count": len(architecture_data.get("system_architecture", {}).get("layers", [])),
                    "components_count": len(architecture_data.get("components", [])),
                    "phases_count": len(architecture_data.get("implementation_phases", [])),
                    "technology_stack": architecture_data.get("technology_stack", {})
                },
                "tokens_used": len(response.split())
            }
            
            return architecture_plan
            
        except Exception as e:
            logger.error(f"❌ Architecture parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse architecture: {str(e)}",
                "raw_response": response,
                "fallback_plan": self._create_fallback_architecture(project_name, template)
            }
    
    def _create_fallback_architecture(self, project_name: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic fallback architecture"""
        
        return {
            "project_overview": {
                "name": project_name,
                "description": f"Basic architecture for {project_name}",
                "goals": ["Deliver functional software", "Ensure maintainability"],
                "success_criteria": ["Working application", "Documented architecture"]
            },
            "technology_stack": {
                "frontend": ["React", "TypeScript"],
                "backend": ["Python", "FastAPI"],
                "database": ["PostgreSQL"],
                "infrastructure": ["Docker", "AWS"],
                "monitoring": ["Prometheus", "Grafana"]
            },
            "system_architecture": {
                "layers": [
                    {
                        "name": "Presentation Layer",
                        "purpose": "User interface and interaction",
                        "components": ["Web UI", "Mobile App"],
                        "technologies": ["React", "React Native"]
                    },
                    {
                        "name": "Business Logic Layer",
                        "purpose": "Core application logic",
                        "components": ["API Server", "Business Services"],
                        "technologies": ["Python", "FastAPI"]
                    },
                    {
                        "name": "Data Layer",
                        "purpose": "Data storage and persistence",
                        "components": ["Database", "Cache"],
                        "technologies": ["PostgreSQL", "Redis"]
                    }
                ],
                "data_flow": "Frontend → API → Business Logic → Database",
                "communication_patterns": ["REST API", "JSON over HTTP"]
            },
            "components": [
                {
                    "name": "Web API",
                    "type": "REST API",
                    "purpose": "Provide HTTP endpoints for frontend",
                    "interfaces": ["HTTP REST"],
                    "dependencies": ["Database", "Authentication"],
                    "scalability": "Horizontal scaling with load balancer"
                }
            ],
            "deployment": {
                "strategy": "Containerized deployment",
                "environments": ["development", "staging", "production"],
                "infrastructure": "Container orchestration platform",
                "monitoring": "Application and infrastructure monitoring"
            },
            "implementation_phases": [
                {
                    "phase": "Foundation",
                    "duration": "2 weeks",
                    "deliverables": ["Basic structure", "Core components"],
                    "dependencies": []
                },
                {
                    "phase": "Development",
                    "duration": "4 weeks",
                    "deliverables": ["Full implementation", "Testing"],
                    "dependencies": ["Foundation"]
                },
                {
                    "phase": "Deployment",
                    "duration": "1 week",
                    "deliverables": ["Production deployment", "Monitoring"],
                    "dependencies": ["Development"]
                }
            ]
        }
    
    async def _store_architecture_results(
        self,
        task_id: str,
        project_name: str,
        architecture_plan: Dict[str, Any],
        session_id: Optional[str] = None
    ):
        """Store architecture results in memory"""
        
        content = f"""
Architecture Plan Generated for {project_name}

Task ID: {task_id}
Generated: {datetime.now().isoformat()}

Architecture Summary:
- Project: {project_name}
- Success: {architecture_plan.get('success', False)}
- Components: {architecture_plan.get('metadata', {}).get('components_count', 0)}
- Layers: {architecture_plan.get('metadata', {}).get('layers_count', 0)}
- Phases: {architecture_plan.get('metadata', {}).get('phases_count', 0)}

Full Architecture Plan:
{json.dumps(architecture_plan, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.TASK,
            priority=MemoryPriority.HIGH,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "project_name": project_name,
                "architecture_success": architecture_plan.get("success", False),
                "components_count": architecture_plan.get("metadata", {}).get("components_count", 0),
                "layers_count": architecture_plan.get("metadata", {}).get("layers_count", 0)
            },
            tags=["architecture", "planning", "obelisk", "code_architect"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "supported_project_types": list(self.architecture_templates.keys()),
            "architecture_features": [
                "System component design",
                "Technology stack selection",
                "Scalability planning",
                "Security architecture",
                "Performance optimization",
                "Deployment strategy",
                "Risk assessment",
                "Implementation phases"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_code_architect_agent(config: Dict[str, Any]) -> CodeArchitectAgent:
    """Factory function to create Code Architect Agent"""
    return CodeArchitectAgent(config)