"""
Village-of-Intelligence Builder Agent
Handles construction, implementation, and systematic building
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class BuilderAgent(BaseAgent):
    """
    Village-of-Intelligence Builder Agent
    
    Responsibilities:
    - System construction and implementation
    - Incremental building and iteration
    - Component integration
    - Process development
    - Infrastructure building
    - Systematic assembly
    - Quality construction
    - Scalable architecture building
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="village_builder",
            agent_type=AgentType.CODER,
            description="Construction and implementation agent",
            capabilities=[
                "system_construction",
                "incremental_building",
                "component_integration",
                "process_development",
                "infrastructure_building",
                "systematic_assembly",
                "quality_construction",
                "scalable_architecture",
                "modular_development",
                "progressive_enhancement",
                "sustainable_building",
                "adaptive_construction"
            ],
            model_requirements=["gpt-4", "claude-3.5-sonnet"],
            priority=9,
            max_concurrent_tasks=3,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Building methodologies and approaches
        self.building_approaches = [
            "incremental_development",
            "iterative_construction",
            "modular_assembly",
            "component_based",
            "layered_building",
            "progressive_enhancement",
            "sustainable_development",
            "adaptive_construction"
        ]
        
        # Village building knowledge
        self.village_constructions = {
            "completed_builds": [],
            "building_patterns": {},
            "construction_wisdom": [],
            "quality_standards": {}
        }
        
        logger.info("🔨 Village-of-Intelligence Builder Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for building/construction"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # Building keywords
        building_keywords = [
            "build", "construct", "create", "develop", "implement", "assemble",
            "integrate", "setup", "deploy", "install", "configure", "establish",
            "framework", "structure", "system", "platform", "infrastructure",
            "component", "module", "service", "application", "solution",
            "process", "workflow", "pipeline", "architecture", "foundation"
        ]
        
        # Check task type
        if task_type in ["building", "construction", "implementation", "development"]:
            return True
        
        # Check content for building keywords
        return any(keyword in content for keyword in building_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute building/construction task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            language = task.get("language", "python")
            approach = task.get("approach", "incremental")
            session_id = task.get("session_id")
            
            logger.info(f"🔨 Builder executing task: {task_id}")
            
            # Determine building action
            action = self._determine_building_action(content)
            
            result = {}
            
            if action == "system_construction":
                result = await self._construct_system(content, language, approach, task_id, session_id)
            elif action == "component_integration":
                result = await self._integrate_components(content, language, approach, task_id, session_id)
            elif action == "process_development":
                result = await self._develop_process(content, language, approach, task_id, session_id)
            elif action == "infrastructure_building":
                result = await self._build_infrastructure(content, language, approach, task_id, session_id)
            elif action == "modular_assembly":
                result = await self._assemble_modular(content, language, approach, task_id, session_id)
            elif action == "progressive_enhancement":
                result = await self._progressive_enhancement(content, language, approach, task_id, session_id)
            else:
                result = await self._general_building(content, language, approach, task_id, session_id)
            
            # Update village building knowledge
            await self._update_village_constructions(result, task_id, session_id)
            
            # Store result in memory
            await self._store_building_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Builder completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "language": language,
                "approach": approach,
                "building_result": result,
                "village_constructions": self._get_village_constructions(),
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Builder failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_building_action(self, content: str) -> str:
        """Determine the specific building action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["system", "platform", "application", "solution"]):
            return "system_construction"
        elif any(word in content_lower for word in ["component", "integrate", "connect", "combine"]):
            return "component_integration"
        elif any(word in content_lower for word in ["process", "workflow", "pipeline", "procedure"]):
            return "process_development"
        elif any(word in content_lower for word in ["infrastructure", "foundation", "framework", "architecture"]):
            return "infrastructure_building"
        elif any(word in content_lower for word in ["modular", "module", "component", "assembly"]):
            return "modular_assembly"
        elif any(word in content_lower for word in ["enhance", "improve", "upgrade", "progressive"]):
            return "progressive_enhancement"
        else:
            return "general_building"
    
    async def _construct_system(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Construct complete system"""
        try:
            request = TaskRequest(
                id=f"{task_id}_system_construction",
                content=f"""
                Construct a complete system using {approach} approach in {language}: {content}
                
                Build comprehensive system including:
                1. Core architecture and structure
                2. Essential components and modules
                3. Data layer and persistence
                4. Business logic implementation
                5. API and interface layer
                6. Security and validation
                7. Error handling and logging
                8. Testing and quality assurance
                9. Documentation and deployment
                10. Monitoring and maintenance
                
                Provide:
                - Complete system implementation
                - Architecture documentation
                - Component specifications
                - Integration guidelines
                - Testing strategy
                - Deployment instructions
                - Maintenance procedures
                """,
                task_type="system_construction",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                system_construction = self._parse_system_construction(response.content, language)
                
                return {
                    "action": "system_construction",
                    "language": language,
                    "approach": approach,
                    "system_construction": system_construction,
                    "architecture": system_construction.get("architecture", {}),
                    "components": system_construction.get("components", []),
                    "implementation": system_construction.get("implementation", ""),
                    "testing_strategy": system_construction.get("testing_strategy", []),
                    "deployment_guide": system_construction.get("deployment_guide", ""),
                    "maintenance_plan": system_construction.get("maintenance_plan", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "system_construction",
                    "error": "Failed to construct system",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ System construction failed: {e}")
            return {
                "action": "system_construction",
                "error": str(e)
            }
    
    async def _integrate_components(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Integrate system components"""
        try:
            request = TaskRequest(
                id=f"{task_id}_component_integration",
                content=f"""
                Integrate system components using {approach} approach in {language}: {content}
                
                Handle component integration including:
                1. Component interface design
                2. Data flow and communication
                3. Event handling and messaging
                4. Error propagation and handling
                5. Configuration management
                6. Dependency injection
                7. Service orchestration
                8. Performance optimization
                9. Testing integration points
                10. Monitoring and observability
                
                Provide complete integration solution with proper error handling and testing.
                """,
                task_type="component_integration",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                component_integration = self._parse_component_integration(response.content, language)
                
                return {
                    "action": "component_integration",
                    "language": language,
                    "approach": approach,
                    "component_integration": component_integration,
                    "integration_points": component_integration.get("integration_points", []),
                    "communication_patterns": component_integration.get("communication_patterns", []),
                    "error_handling": component_integration.get("error_handling", []),
                    "testing_approach": component_integration.get("testing_approach", []),
                    "monitoring_setup": component_integration.get("monitoring_setup", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "component_integration",
                    "error": "Failed to integrate components",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Component integration failed: {e}")
            return {
                "action": "component_integration",
                "error": str(e)
            }
    
    async def _develop_process(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Develop systematic process"""
        try:
            request = TaskRequest(
                id=f"{task_id}_process_development",
                content=f"""
                Develop systematic process using {approach} approach in {language}: {content}
                
                Create comprehensive process including:
                1. Process workflow design
                2. Step-by-step procedures
                3. Decision points and branching
                4. Error handling and recovery
                5. Validation and quality checks
                6. Performance optimization
                7. Automation opportunities
                8. Monitoring and metrics
                9. Documentation and training
                10. Continuous improvement
                
                Provide complete process implementation with automation and monitoring.
                """,
                task_type="process_development",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                process_development = self._parse_process_development(response.content, language)
                
                return {
                    "action": "process_development",
                    "language": language,
                    "approach": approach,
                    "process_development": process_development,
                    "workflow_design": process_development.get("workflow_design", {}),
                    "procedures": process_development.get("procedures", []),
                    "automation": process_development.get("automation", []),
                    "quality_checks": process_development.get("quality_checks", []),
                    "monitoring_metrics": process_development.get("monitoring_metrics", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "process_development",
                    "error": "Failed to develop process",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Process development failed: {e}")
            return {
                "action": "process_development",
                "error": str(e)
            }
    
    async def _build_infrastructure(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Build system infrastructure"""
        try:
            request = TaskRequest(
                id=f"{task_id}_infrastructure_building",
                content=f"""
                Build system infrastructure using {approach} approach in {language}: {content}
                
                Create robust infrastructure including:
                1. Foundation architecture
                2. Core services and utilities
                3. Configuration management
                4. Logging and monitoring
                5. Security framework
                6. Performance optimization
                7. Scalability provisions
                8. Deployment automation
                9. Backup and recovery
                10. Health checks and diagnostics
                
                Provide production-ready infrastructure with comprehensive monitoring.
                """,
                task_type="infrastructure_building",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                infrastructure_building = self._parse_infrastructure_building(response.content, language)
                
                return {
                    "action": "infrastructure_building",
                    "language": language,
                    "approach": approach,
                    "infrastructure_building": infrastructure_building,
                    "foundation": infrastructure_building.get("foundation", {}),
                    "core_services": infrastructure_building.get("core_services", []),
                    "security_framework": infrastructure_building.get("security_framework", {}),
                    "monitoring_setup": infrastructure_building.get("monitoring_setup", {}),
                    "deployment_automation": infrastructure_building.get("deployment_automation", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "infrastructure_building",
                    "error": "Failed to build infrastructure",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Infrastructure building failed: {e}")
            return {
                "action": "infrastructure_building",
                "error": str(e)
            }
    
    async def _assemble_modular(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Assemble modular components"""
        try:
            request = TaskRequest(
                id=f"{task_id}_modular_assembly",
                content=f"""
                Assemble modular components using {approach} approach in {language}: {content}
                
                Create modular assembly including:
                1. Module design and interfaces
                2. Dependency management
                3. Plugin architecture
                4. Configuration system
                5. Module discovery
                6. Dynamic loading
                7. Inter-module communication
                8. Version compatibility
                9. Testing modules
                10. Documentation
                
                Provide flexible modular system with clean interfaces.
                """,
                task_type="modular_assembly",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                modular_assembly = self._parse_modular_assembly(response.content, language)
                
                return {
                    "action": "modular_assembly",
                    "language": language,
                    "approach": approach,
                    "modular_assembly": modular_assembly,
                    "module_design": modular_assembly.get("module_design", {}),
                    "interfaces": modular_assembly.get("interfaces", []),
                    "plugin_architecture": modular_assembly.get("plugin_architecture", {}),
                    "configuration_system": modular_assembly.get("configuration_system", {}),
                    "testing_modules": modular_assembly.get("testing_modules", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "modular_assembly",
                    "error": "Failed to assemble modular components",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Modular assembly failed: {e}")
            return {
                "action": "modular_assembly",
                "error": str(e)
            }
    
    async def _progressive_enhancement(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Progressive enhancement and improvement"""
        try:
            request = TaskRequest(
                id=f"{task_id}_progressive_enhancement",
                content=f"""
                Progressive enhancement using {approach} approach in {language}: {content}
                
                Implement progressive enhancement including:
                1. Baseline functionality
                2. Feature layering
                3. Graceful degradation
                4. Performance optimization
                5. User experience improvements
                6. Accessibility enhancements
                7. Mobile responsiveness
                8. Cross-platform compatibility
                9. Testing enhancements
                10. Continuous improvement
                
                Provide enhanced system with backwards compatibility.
                """,
                task_type="progressive_enhancement",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                progressive_enhancement = self._parse_progressive_enhancement(response.content, language)
                
                return {
                    "action": "progressive_enhancement",
                    "language": language,
                    "approach": approach,
                    "progressive_enhancement": progressive_enhancement,
                    "baseline_functionality": progressive_enhancement.get("baseline_functionality", {}),
                    "feature_layers": progressive_enhancement.get("feature_layers", []),
                    "performance_optimizations": progressive_enhancement.get("performance_optimizations", []),
                    "accessibility_enhancements": progressive_enhancement.get("accessibility_enhancements", []),
                    "compatibility_measures": progressive_enhancement.get("compatibility_measures", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "progressive_enhancement",
                    "error": "Failed to implement progressive enhancement",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Progressive enhancement failed: {e}")
            return {
                "action": "progressive_enhancement",
                "error": str(e)
            }
    
    async def _general_building(self, content: str, language: str, approach: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general building tasks"""
        try:
            request = TaskRequest(
                id=f"{task_id}_general_building",
                content=f"""
                Build solution using {approach} approach in {language}: {content}
                
                Provide comprehensive building solution with:
                1. Clear implementation
                2. Proper structure and organization
                3. Error handling and validation
                4. Testing and quality assurance
                5. Documentation and examples
                6. Performance considerations
                7. Maintenance guidelines
                
                Follow {language} best practices and conventions.
                """,
                task_type="general_building",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_building",
                    "language": language,
                    "approach": approach,
                    "building_solution": self._parse_general_building(response.content, language),
                    "implementation": self._extract_implementation(response.content),
                    "testing_approach": self._extract_testing_approach(response.content),
                    "documentation": self._extract_documentation(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_building",
                    "error": "Failed to build general solution",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General building failed: {e}")
            return {
                "action": "general_building",
                "error": str(e)
            }
    
    # Parsing methods (simplified)
    def _parse_system_construction(self, content: str, language: str) -> Dict[str, Any]:
        """Parse system construction results"""
        return {
            "architecture": {"type": "microservices", "layers": 3},
            "components": ["Component 1", "Component 2", "Component 3"],
            "implementation": "Complete system implementation",
            "testing_strategy": ["Unit tests", "Integration tests", "E2E tests"],
            "deployment_guide": "Deployment instructions",
            "maintenance_plan": ["Regular updates", "Performance monitoring"],
            "full_content": content
        }
    
    def _parse_component_integration(self, content: str, language: str) -> Dict[str, Any]:
        """Parse component integration results"""
        return {
            "integration_points": ["API Gateway", "Message Queue", "Database"],
            "communication_patterns": ["REST API", "Event-driven", "Pub/Sub"],
            "error_handling": ["Circuit breaker", "Retry logic", "Fallback"],
            "testing_approach": ["Contract testing", "Integration testing"],
            "monitoring_setup": {"metrics": True, "logging": True},
            "full_content": content
        }
    
    def _parse_process_development(self, content: str, language: str) -> Dict[str, Any]:
        """Parse process development results"""
        return {
            "workflow_design": {"steps": 5, "decision_points": 3},
            "procedures": ["Step 1", "Step 2", "Step 3"],
            "automation": ["Automated testing", "Automated deployment"],
            "quality_checks": ["Code review", "Security scan", "Performance test"],
            "monitoring_metrics": ["Success rate", "Processing time", "Error count"],
            "full_content": content
        }
    
    def _parse_infrastructure_building(self, content: str, language: str) -> Dict[str, Any]:
        """Parse infrastructure building results"""
        return {
            "foundation": {"framework": "FastAPI", "database": "PostgreSQL"},
            "core_services": ["Authentication", "Logging", "Monitoring"],
            "security_framework": {"auth": "JWT", "encryption": "AES-256"},
            "monitoring_setup": {"prometheus": True, "grafana": True},
            "deployment_automation": ["Docker", "Kubernetes", "CI/CD"],
            "full_content": content
        }
    
    def _parse_modular_assembly(self, content: str, language: str) -> Dict[str, Any]:
        """Parse modular assembly results"""
        return {
            "module_design": {"pattern": "Plugin architecture", "interfaces": "Abstract base"},
            "interfaces": ["IPlugin", "IService", "IHandler"],
            "plugin_architecture": {"discovery": "Dynamic", "loading": "Lazy"},
            "configuration_system": {"format": "YAML", "validation": True},
            "testing_modules": ["Module tests", "Integration tests"],
            "full_content": content
        }
    
    def _parse_progressive_enhancement(self, content: str, language: str) -> Dict[str, Any]:
        """Parse progressive enhancement results"""
        return {
            "baseline_functionality": {"core": "Basic features", "compatibility": "All browsers"},
            "feature_layers": ["Layer 1: Basic", "Layer 2: Enhanced", "Layer 3: Advanced"],
            "performance_optimizations": ["Caching", "Lazy loading", "Compression"],
            "accessibility_enhancements": ["WCAG compliance", "Screen reader support"],
            "compatibility_measures": ["Polyfills", "Feature detection", "Graceful degradation"],
            "full_content": content
        }
    
    def _parse_general_building(self, content: str, language: str) -> Dict[str, Any]:
        """Parse general building results"""
        return {
            "implementation": "General building solution",
            "structure": "Well-organized code structure",
            "testing": "Comprehensive testing approach",
            "documentation": "Clear documentation",
            "full_content": content
        }
    
    def _extract_implementation(self, content: str) -> str:
        """Extract implementation details"""
        return "Implementation details extracted"
    
    def _extract_testing_approach(self, content: str) -> List[str]:
        """Extract testing approach"""
        return ["Unit tests", "Integration tests", "E2E tests"]
    
    def _extract_documentation(self, content: str) -> str:
        """Extract documentation"""
        return "Documentation extracted"
    
    async def _update_village_constructions(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Update village building knowledge"""
        try:
            # Extract building patterns and wisdom
            action = result.get("action", "")
            approach = result.get("approach", "")
            
            # Update village constructions
            self.village_constructions["completed_builds"].append({
                "task_id": task_id,
                "action": action,
                "approach": approach,
                "timestamp": datetime.now().isoformat()
            })
            
            # Store building patterns
            if action not in self.village_constructions["building_patterns"]:
                self.village_constructions["building_patterns"][action] = []
            
            self.village_constructions["building_patterns"][action].append(approach)
            
            # Store in shared memory for other village agents
            await self.memory_manager.store_memory(
                content=f"Village construction: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.KNOWLEDGE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "village_agent": "builder",
                    "task_id": task_id,
                    "collective_intelligence": True
                },
                tags=["village", "building", "construction"],
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to update village constructions: {e}")
    
    def _get_village_constructions(self) -> Dict[str, Any]:
        """Get village construction knowledge"""
        return {
            "total_builds": len(self.village_constructions["completed_builds"]),
            "recent_builds": self.village_constructions["completed_builds"][-3:],
            "building_patterns": self.village_constructions["building_patterns"],
            "construction_wisdom": self.village_constructions["construction_wisdom"]
        }
    
    async def _store_building_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store building result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"Building result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "language": result.get("language"),
                    "approach": result.get("approach"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["building", "construction", "village"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store building result: {e}")


def create_builder_agent(config: Dict[str, Any]) -> BuilderAgent:
    """Factory function to create Builder Agent"""
    return BuilderAgent(config)