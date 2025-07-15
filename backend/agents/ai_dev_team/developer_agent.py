"""
AI-Development-Team Developer Agent
Handles code development, implementation, and feature building
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


class DeveloperAgent(BaseAgent):
    """
    AI-Development-Team Developer Agent
    
    Responsibilities:
    - Code development and implementation
    - Feature building and enhancement
    - Bug fixes and refactoring
    - API development
    - Database integration
    - Third-party integrations
    - Code optimization
    - Documentation writing
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="ai_dev_team_developer",
            agent_type=AgentType.CODER,
            description="Code development and implementation agent",
            capabilities=[
                "code_development",
                "feature_implementation",
                "bug_fixing",
                "refactoring",
                "api_development",
                "database_integration",
                "third_party_integration",
                "code_optimization",
                "documentation_writing",
                "unit_testing",
                "debugging",
                "version_control"
            ],
            model_requirements=["gpt-4", "claude-3.5-sonnet"],
            priority=8,
            max_concurrent_tasks=3,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Programming languages and frameworks
        self.supported_languages = [
            "python", "javascript", "typescript", "java", "golang", "rust",
            "c++", "c#", "php", "ruby", "swift", "kotlin", "dart", "scala"
        ]
        
        self.frameworks = {
            "web": ["react", "vue", "angular", "svelte", "nextjs", "nuxt"],
            "backend": ["fastapi", "django", "flask", "express", "spring", "gin"],
            "mobile": ["react_native", "flutter", "ionic", "xamarin"],
            "desktop": ["electron", "tauri", "qt", "gtk"]
        }
        
        logger.info("👨‍💻 AI-Development-Team Developer Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for development"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # Development keywords
        development_keywords = [
            "code", "develop", "implement", "build", "create", "program",
            "function", "class", "method", "api", "endpoint", "feature",
            "bug", "fix", "debug", "refactor", "optimize", "database",
            "integration", "service", "component", "module", "library",
            "framework", "algorithm", "data", "structure", "logic"
        ]
        
        # Check task type
        if task_type in ["development", "coding", "implementation", "feature"]:
            return True
        
        # Check content for development keywords
        return any(keyword in content for keyword in development_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute development task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            language = task.get("language", "python")
            session_id = task.get("session_id")
            
            logger.info(f"👨‍💻 Developer executing task: {task_id}")
            
            # Determine development action
            action = self._determine_action(content)
            
            result = {}
            
            if action == "feature_implementation":
                result = await self._implement_feature(content, language, task_id, session_id)
            elif action == "bug_fixing":
                result = await self._fix_bug(content, language, task_id, session_id)
            elif action == "api_development":
                result = await self._develop_api(content, language, task_id, session_id)
            elif action == "database_integration":
                result = await self._integrate_database(content, language, task_id, session_id)
            elif action == "refactoring":
                result = await self._refactor_code(content, language, task_id, session_id)
            elif action == "optimization":
                result = await self._optimize_code(content, language, task_id, session_id)
            elif action == "testing":
                result = await self._write_tests(content, language, task_id, session_id)
            else:
                result = await self._general_development(content, language, task_id, session_id)
            
            # Store result in memory
            await self._store_development_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Developer completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "language": language,
                "development_result": result,
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Developer failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_action(self, content: str) -> str:
        """Determine the specific development action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["feature", "implement", "build", "create"]):
            return "feature_implementation"
        elif any(word in content_lower for word in ["bug", "fix", "debug", "error", "issue"]):
            return "bug_fixing"
        elif any(word in content_lower for word in ["api", "endpoint", "service", "rest", "graphql"]):
            return "api_development"
        elif any(word in content_lower for word in ["database", "db", "sql", "query", "orm"]):
            return "database_integration"
        elif any(word in content_lower for word in ["refactor", "restructure", "reorganize", "clean"]):
            return "refactoring"
        elif any(word in content_lower for word in ["optimize", "performance", "speed", "efficiency"]):
            return "optimization"
        elif any(word in content_lower for word in ["test", "testing", "unit", "integration"]):
            return "testing"
        else:
            return "general_development"
    
    async def _implement_feature(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Implement new feature"""
        try:
            request = TaskRequest(
                id=f"{task_id}_feature",
                content=f"""
                Implement a complete feature in {language}: {content}
                
                Provide:
                1. Complete implementation with all necessary components
                2. Proper error handling and validation
                3. Unit tests for the feature
                4. Documentation and comments
                5. Example usage
                6. Configuration and setup instructions
                
                Follow best practices for {language} development including:
                - Clean code principles
                - Proper naming conventions
                - Error handling
                - Performance considerations
                - Security best practices
                """,
                task_type="feature_implementation",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                feature_code = self._parse_feature_implementation(response.content, language)
                
                return {
                    "action": "feature_implementation",
                    "language": language,
                    "feature_code": feature_code,
                    "main_implementation": feature_code.get("main_implementation", ""),
                    "test_code": feature_code.get("test_code", ""),
                    "documentation": feature_code.get("documentation", ""),
                    "dependencies": feature_code.get("dependencies", []),
                    "setup_instructions": feature_code.get("setup_instructions", ""),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "feature_implementation",
                    "error": "Failed to implement feature",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Feature implementation failed: {e}")
            return {
                "action": "feature_implementation",
                "error": str(e)
            }
    
    async def _fix_bug(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Fix bug in existing code"""
        try:
            request = TaskRequest(
                id=f"{task_id}_bugfix",
                content=f"""
                Fix the bug in {language}: {content}
                
                Provide:
                1. Bug analysis and root cause identification
                2. Fixed code with corrections
                3. Explanation of the fix
                4. Test cases to verify the fix
                5. Regression test suggestions
                6. Prevention recommendations
                
                Ensure the fix:
                - Addresses the root cause
                - Doesn't introduce new bugs
                - Maintains existing functionality
                - Follows coding standards
                - Includes proper testing
                """,
                task_type="bug_fixing",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                bug_fix = self._parse_bug_fix(response.content, language)
                
                return {
                    "action": "bug_fixing",
                    "language": language,
                    "bug_fix": bug_fix,
                    "root_cause": bug_fix.get("root_cause", ""),
                    "fixed_code": bug_fix.get("fixed_code", ""),
                    "fix_explanation": bug_fix.get("fix_explanation", ""),
                    "test_cases": bug_fix.get("test_cases", []),
                    "prevention_recommendations": bug_fix.get("prevention_recommendations", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "bug_fixing",
                    "error": "Failed to fix bug",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Bug fixing failed: {e}")
            return {
                "action": "bug_fixing",
                "error": str(e)
            }
    
    async def _develop_api(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Develop API endpoints"""
        try:
            request = TaskRequest(
                id=f"{task_id}_api",
                content=f"""
                Develop API endpoints in {language}: {content}
                
                Provide:
                1. Complete API implementation
                2. Request/response schemas
                3. Authentication and authorization
                4. Error handling and validation
                5. API documentation
                6. Test cases for each endpoint
                7. Rate limiting and security measures
                
                Follow REST/GraphQL best practices:
                - Proper HTTP methods and status codes
                - Consistent response formats
                - Input validation
                - Error handling
                - Security considerations
                - Performance optimization
                """,
                task_type="api_development",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                api_code = self._parse_api_development(response.content, language)
                
                return {
                    "action": "api_development",
                    "language": language,
                    "api_code": api_code,
                    "endpoints": api_code.get("endpoints", []),
                    "schemas": api_code.get("schemas", []),
                    "authentication": api_code.get("authentication", ""),
                    "documentation": api_code.get("documentation", ""),
                    "test_cases": api_code.get("test_cases", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "api_development",
                    "error": "Failed to develop API",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ API development failed: {e}")
            return {
                "action": "api_development",
                "error": str(e)
            }
    
    async def _integrate_database(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Integrate database functionality"""
        try:
            request = TaskRequest(
                id=f"{task_id}_database",
                content=f"""
                Integrate database functionality in {language}: {content}
                
                Provide:
                1. Database schema design
                2. ORM/ODM models
                3. Database connection setup
                4. CRUD operations
                5. Query optimization
                6. Migration scripts
                7. Database testing
                
                Include:
                - Proper indexing strategies
                - Data validation
                - Transaction handling
                - Error handling
                - Performance optimization
                - Security considerations
                """,
                task_type="database_integration",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                db_integration = self._parse_database_integration(response.content, language)
                
                return {
                    "action": "database_integration",
                    "language": language,
                    "db_integration": db_integration,
                    "schema": db_integration.get("schema", ""),
                    "models": db_integration.get("models", []),
                    "crud_operations": db_integration.get("crud_operations", []),
                    "migrations": db_integration.get("migrations", []),
                    "test_cases": db_integration.get("test_cases", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "database_integration",
                    "error": "Failed to integrate database",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Database integration failed: {e}")
            return {
                "action": "database_integration",
                "error": str(e)
            }
    
    async def _refactor_code(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Refactor existing code"""
        try:
            request = TaskRequest(
                id=f"{task_id}_refactor",
                content=f"""
                Refactor the {language} code: {content}
                
                Provide:
                1. Refactored code with improvements
                2. Explanation of changes made
                3. Benefits of the refactoring
                4. Impact analysis
                5. Test cases to verify functionality
                6. Migration guide if needed
                
                Focus on:
                - Code readability and maintainability
                - Performance improvements
                - Design pattern implementation
                - Removing code smells
                - Following best practices
                - Reducing complexity
                """,
                task_type="refactoring",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                refactored_code = self._parse_refactoring(response.content, language)
                
                return {
                    "action": "refactoring",
                    "language": language,
                    "refactored_code": refactored_code,
                    "improvements": refactored_code.get("improvements", []),
                    "impact_analysis": refactored_code.get("impact_analysis", ""),
                    "test_cases": refactored_code.get("test_cases", []),
                    "migration_guide": refactored_code.get("migration_guide", ""),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "refactoring",
                    "error": "Failed to refactor code",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Code refactoring failed: {e}")
            return {
                "action": "refactoring",
                "error": str(e)
            }
    
    async def _optimize_code(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Optimize code for performance"""
        try:
            request = TaskRequest(
                id=f"{task_id}_optimize",
                content=f"""
                Optimize the {language} code for performance: {content}
                
                Provide:
                1. Optimized code with performance improvements
                2. Performance analysis and benchmarks
                3. Optimization techniques applied
                4. Memory usage improvements
                5. Algorithm optimizations
                6. Performance testing code
                
                Focus on:
                - Time complexity improvements
                - Memory efficiency
                - Algorithm optimization
                - Database query optimization
                - Caching strategies
                - Parallel processing opportunities
                """,
                task_type="optimization",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                optimized_code = self._parse_optimization(response.content, language)
                
                return {
                    "action": "optimization",
                    "language": language,
                    "optimized_code": optimized_code,
                    "performance_improvements": optimized_code.get("performance_improvements", []),
                    "benchmarks": optimized_code.get("benchmarks", {}),
                    "optimization_techniques": optimized_code.get("optimization_techniques", []),
                    "test_cases": optimized_code.get("test_cases", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "optimization",
                    "error": "Failed to optimize code",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Code optimization failed: {e}")
            return {
                "action": "optimization",
                "error": str(e)
            }
    
    async def _write_tests(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Write comprehensive tests"""
        try:
            request = TaskRequest(
                id=f"{task_id}_tests",
                content=f"""
                Write comprehensive tests in {language}: {content}
                
                Provide:
                1. Unit tests for all functions/methods
                2. Integration tests for components
                3. Edge case testing
                4. Error handling tests
                5. Performance tests
                6. Test setup and teardown
                7. Test coverage analysis
                
                Include:
                - Positive and negative test cases
                - Boundary value testing
                - Mock and stub implementations
                - Test data generation
                - Assertion strategies
                - Test documentation
                """,
                task_type="testing",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                test_code = self._parse_test_writing(response.content, language)
                
                return {
                    "action": "testing",
                    "language": language,
                    "test_code": test_code,
                    "unit_tests": test_code.get("unit_tests", []),
                    "integration_tests": test_code.get("integration_tests", []),
                    "edge_cases": test_code.get("edge_cases", []),
                    "test_coverage": test_code.get("test_coverage", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "testing",
                    "error": "Failed to write tests",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Test writing failed: {e}")
            return {
                "action": "testing",
                "error": str(e)
            }
    
    async def _general_development(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general development tasks"""
        try:
            request = TaskRequest(
                id=f"{task_id}_general",
                content=f"""
                Handle general development task in {language}: {content}
                
                Provide:
                1. Complete implementation
                2. Code documentation
                3. Error handling
                4. Best practices implementation
                5. Testing recommendations
                6. Usage examples
                
                Follow {language} best practices and conventions.
                """,
                task_type="general_development",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_development",
                    "language": language,
                    "implementation": self._parse_general_development(response.content, language),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_development",
                    "error": "Failed to handle general development",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General development failed: {e}")
            return {
                "action": "general_development",
                "error": str(e)
            }
    
    # Parsing methods (simplified for example)
    def _parse_feature_implementation(self, content: str, language: str) -> Dict[str, Any]:
        """Parse feature implementation"""
        return {
            "main_implementation": "Feature implementation code",
            "test_code": "Test code for feature",
            "documentation": "Feature documentation",
            "dependencies": ["dependency1", "dependency2"],
            "setup_instructions": "Setup instructions",
            "full_content": content
        }
    
    def _parse_bug_fix(self, content: str, language: str) -> Dict[str, Any]:
        """Parse bug fix"""
        return {
            "root_cause": "Bug root cause analysis",
            "fixed_code": "Fixed code implementation",
            "fix_explanation": "Explanation of the fix",
            "test_cases": ["Test case 1", "Test case 2"],
            "prevention_recommendations": ["Prevention 1", "Prevention 2"],
            "full_content": content
        }
    
    def _parse_api_development(self, content: str, language: str) -> Dict[str, Any]:
        """Parse API development"""
        return {
            "endpoints": ["GET /api/users", "POST /api/users"],
            "schemas": ["UserSchema", "ResponseSchema"],
            "authentication": "JWT authentication",
            "documentation": "API documentation",
            "test_cases": ["Test case 1", "Test case 2"],
            "full_content": content
        }
    
    def _parse_database_integration(self, content: str, language: str) -> Dict[str, Any]:
        """Parse database integration"""
        return {
            "schema": "Database schema",
            "models": ["UserModel", "OrderModel"],
            "crud_operations": ["Create", "Read", "Update", "Delete"],
            "migrations": ["Migration 1", "Migration 2"],
            "test_cases": ["Test case 1", "Test case 2"],
            "full_content": content
        }
    
    def _parse_refactoring(self, content: str, language: str) -> Dict[str, Any]:
        """Parse refactoring"""
        return {
            "improvements": ["Improvement 1", "Improvement 2"],
            "impact_analysis": "Impact analysis",
            "test_cases": ["Test case 1", "Test case 2"],
            "migration_guide": "Migration guide",
            "full_content": content
        }
    
    def _parse_optimization(self, content: str, language: str) -> Dict[str, Any]:
        """Parse optimization"""
        return {
            "performance_improvements": ["Improvement 1", "Improvement 2"],
            "benchmarks": {"before": "100ms", "after": "50ms"},
            "optimization_techniques": ["Technique 1", "Technique 2"],
            "test_cases": ["Test case 1", "Test case 2"],
            "full_content": content
        }
    
    def _parse_test_writing(self, content: str, language: str) -> Dict[str, Any]:
        """Parse test writing"""
        return {
            "unit_tests": ["Unit test 1", "Unit test 2"],
            "integration_tests": ["Integration test 1", "Integration test 2"],
            "edge_cases": ["Edge case 1", "Edge case 2"],
            "test_coverage": {"percentage": 95, "lines": 950},
            "full_content": content
        }
    
    def _parse_general_development(self, content: str, language: str) -> Dict[str, Any]:
        """Parse general development"""
        return {
            "implementation": "General implementation",
            "documentation": "Documentation",
            "examples": ["Example 1", "Example 2"],
            "full_content": content
        }
    
    async def _store_development_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store development result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"Development result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "language": result.get("language"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["development", "ai_dev_team", "coding"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store development result: {e}")


def create_developer_agent(config: Dict[str, Any]) -> DeveloperAgent:
    """Factory function to create Developer Agent"""
    return DeveloperAgent(config)