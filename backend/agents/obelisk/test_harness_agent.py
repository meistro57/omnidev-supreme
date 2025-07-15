"""
OBELISK Test Harness Agent
Automatically generates comprehensive test suites
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class TestHarnessAgent(BaseAgent):
    """
    OBELISK Test Harness Agent
    
    Specializes in:
    - Comprehensive test suite generation
    - Unit and integration test creation
    - Edge case testing
    - Test automation setup
    - Performance testing
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="test_harness",
            agent_type=AgentType.TESTER,
            description="OBELISK Test Harness - Automatically generates comprehensive test suites",
            capabilities=[
                "unit_test_generation",
                "integration_test_creation",
                "edge_case_testing",
                "test_automation_setup",
                "performance_testing",
                "test_coverage_analysis",
                "mock_and_stub_generation",
                "test_data_generation"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=7,
            max_concurrent_tasks=2,
            timeout_seconds=900,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Test frameworks by language
        self.test_frameworks = {
            "python": {
                "primary": "pytest",
                "alternatives": ["unittest", "nose2", "doctest"],
                "mocking": "unittest.mock",
                "fixtures": "pytest.fixture",
                "coverage": "pytest-cov",
                "test_file_pattern": "test_*.py",
                "test_directory": "tests/",
                "imports": ["import pytest", "from unittest.mock import Mock, patch"]
            },
            "javascript": {
                "primary": "jest",
                "alternatives": ["mocha", "jasmine", "vitest"],
                "mocking": "jest.mock",
                "fixtures": "beforeEach/afterEach",
                "coverage": "jest --coverage",
                "test_file_pattern": "*.test.js",
                "test_directory": "tests/",
                "imports": ["const { describe, it, expect, beforeEach, afterEach } = require('@jest/globals');"]
            },
            "typescript": {
                "primary": "jest",
                "alternatives": ["mocha", "jasmine", "vitest"],
                "mocking": "jest.mock",
                "fixtures": "beforeEach/afterEach",
                "coverage": "jest --coverage",
                "test_file_pattern": "*.test.ts",
                "test_directory": "tests/",
                "imports": ["import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';"]
            },
            "java": {
                "primary": "junit5",
                "alternatives": ["junit4", "testng"],
                "mocking": "Mockito",
                "fixtures": "@BeforeEach/@AfterEach",
                "coverage": "JaCoCo",
                "test_file_pattern": "*Test.java",
                "test_directory": "src/test/java/",
                "imports": ["import org.junit.jupiter.api.*;", "import static org.junit.jupiter.api.Assertions.*;"]
            },
            "go": {
                "primary": "testing",
                "alternatives": ["ginkgo", "testify"],
                "mocking": "testify/mock",
                "fixtures": "setup/teardown functions",
                "coverage": "go test -cover",
                "test_file_pattern": "*_test.go",
                "test_directory": "./",
                "imports": ["import \"testing\"", "import \"github.com/stretchr/testify/assert\""]
            }
        }
        
        # Test types and patterns
        self.test_types = {
            "unit": {
                "description": "Test individual functions/methods in isolation",
                "scope": "single function or method",
                "dependencies": "mocked",
                "patterns": ["happy_path", "edge_cases", "error_conditions"]
            },
            "integration": {
                "description": "Test interactions between components",
                "scope": "multiple components",
                "dependencies": "real or stubbed",
                "patterns": ["component_interaction", "data_flow", "api_integration"]
            },
            "performance": {
                "description": "Test performance characteristics",
                "scope": "system or component",
                "dependencies": "production-like",
                "patterns": ["load_testing", "stress_testing", "benchmark_testing"]
            },
            "end_to_end": {
                "description": "Test complete user workflows",
                "scope": "entire application",
                "dependencies": "real system",
                "patterns": ["user_journey", "business_scenarios", "workflow_testing"]
            }
        }
        
        logger.info(f"🧪 {self.metadata.name} initialized with comprehensive test generation capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for test harness agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires test generation
        test_keywords = [
            "test", "testing", "unittest", "pytest", "spec", "verify",
            "validation", "coverage", "mock", "fixture", "assertion"
        ]
        
        return any(keyword in content for keyword in test_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute test generation task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"🧪 Starting test generation: {task_id}")
            
            # Extract task parameters
            code_to_test = task.get("code_to_test", "")
            language = task.get("language", "python")
            test_types = task.get("test_types", ["unit"])
            framework = task.get("framework", "")
            context = task.get("context", {})
            
            # Generate comprehensive test suite
            test_result = await self._generate_test_suite(
                code=code_to_test,
                language=language,
                test_types=test_types,
                framework=framework,
                context=context
            )
            
            # Store results in memory
            await self._store_test_results(
                task_id=task_id,
                test_result=test_result,
                language=language,
                test_types=test_types,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "test_generation": test_result,
                "language": language,
                "test_types": test_types,
                "framework": framework,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"test_{task_id}",
                "tokens_used": test_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Test generation completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Test generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_test_suite(
        self,
        code: str,
        language: str,
        test_types: List[str],
        framework: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive test suite"""
        
        # Validate language support
        if language not in self.test_frameworks:
            raise ValueError(f"Unsupported language: {language}")
        
        framework_config = self.test_frameworks[language]
        if not framework:
            framework = framework_config["primary"]
        
        # Analyze code structure
        code_analysis = self._analyze_code_structure(code, language)
        
        # Create test generation prompt
        test_prompt = self._create_test_generation_prompt(
            code=code,
            language=language,
            framework=framework,
            test_types=test_types,
            framework_config=framework_config,
            code_analysis=code_analysis,
            context=context
        )
        
        # Generate tests using best available model
        try:
            response = await self.orchestrator.generate_response(
                prompt=test_prompt,
                model_preference=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
                temperature=0.1,  # Low temperature for consistent test generation
                max_tokens=6000
            )
            
            # Parse and structure test response
            test_result = await self._parse_test_response(
                response=response,
                language=language,
                framework=framework,
                test_types=test_types,
                code_analysis=code_analysis
            )
            
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Test generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_tests": self._create_fallback_tests(language, framework, code_analysis)
            }
    
    def _analyze_code_structure(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code structure to identify testable components"""
        
        analysis = {
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": "medium",
            "test_candidates": []
        }
        
        if language == "python":
            # Extract functions
            func_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):'
            functions = re.findall(func_pattern, code)
            analysis["functions"] = functions
            
            # Extract classes
            class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[(:)]'
            classes = re.findall(class_pattern, code)
            analysis["classes"] = classes
            
            # Extract imports
            import_pattern = r'(?:from\s+[\w.]+\s+)?import\s+[\w.,\s]+'
            imports = re.findall(import_pattern, code)
            analysis["imports"] = imports
            
        elif language in ["javascript", "typescript"]:
            # Extract functions
            func_pattern = r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)\s*[=:]\s*(?:async\s+)?function|([a-zA-Z_][a-zA-Z0-9_]*)\s*[=:]\s*\([^)]*\)\s*=>)'
            functions = re.findall(func_pattern, code)
            analysis["functions"] = [f for match in functions for f in match if f]
            
            # Extract classes
            class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            classes = re.findall(class_pattern, code)
            analysis["classes"] = classes
            
        elif language == "java":
            # Extract methods
            method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*{'
            methods = re.findall(method_pattern, code)
            analysis["functions"] = methods
            
            # Extract classes
            class_pattern = r'(?:public\s+)?class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            classes = re.findall(class_pattern, code)
            analysis["classes"] = classes
            
        elif language == "go":
            # Extract functions
            func_pattern = r'func\s+(?:\([^)]*\)\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)'
            functions = re.findall(func_pattern, code)
            analysis["functions"] = functions
            
            # Extract structs (Go's version of classes)
            struct_pattern = r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+struct'
            structs = re.findall(struct_pattern, code)
            analysis["classes"] = structs
        
        # Determine complexity
        lines = len(code.split('\n'))
        if lines > 100:
            analysis["complexity"] = "high"
        elif lines > 50:
            analysis["complexity"] = "medium"
        else:
            analysis["complexity"] = "low"
        
        # Generate test candidates
        analysis["test_candidates"] = analysis["functions"] + analysis["classes"]
        
        return analysis
    
    def _create_test_generation_prompt(
        self,
        code: str,
        language: str,
        framework: str,
        test_types: List[str],
        framework_config: Dict[str, Any],
        code_analysis: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed test generation prompt"""
        
        return f"""
You are an expert test engineer tasked with generating comprehensive test suites for the provided code.

CODE TO TEST:
```{language}
{code}
```

TESTING SPECIFICATIONS:
- Language: {language}
- Test Framework: {framework}
- Test Types: {test_types}
- Test File Pattern: {framework_config.get('test_file_pattern', '*_test.*')}
- Test Directory: {framework_config.get('test_directory', 'tests/')}

CODE ANALYSIS:
- Functions: {code_analysis.get('functions', [])}
- Classes: {code_analysis.get('classes', [])}
- Complexity: {code_analysis.get('complexity', 'medium')}
- Test Candidates: {code_analysis.get('test_candidates', [])}

CONTEXT:
{context}

REQUIRED IMPORTS:
{chr(10).join(framework_config.get('imports', []))}

TEST GENERATION REQUIREMENTS:
Generate comprehensive tests for each test type requested:

1. UNIT TESTS:
   - Test each function/method in isolation
   - Cover happy path, edge cases, and error conditions
   - Use mocks/stubs for dependencies
   - Test boundary conditions and invalid inputs
   - Verify return values and side effects

2. INTEGRATION TESTS:
   - Test component interactions
   - Test data flow between modules
   - Test API endpoints and database interactions
   - Verify system behavior with real dependencies

3. PERFORMANCE TESTS:
   - Test response times and throughput
   - Test memory usage and resource consumption
   - Test scalability and load handling
   - Benchmark critical operations

4. END-TO-END TESTS:
   - Test complete user workflows
   - Test business scenarios
   - Test system integration
   - Verify user experience

BEST PRACTICES:
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Include setup and teardown when needed
- Test both positive and negative scenarios
- Use appropriate assertions
- Include test documentation
- Mock external dependencies
- Test error handling

Please provide the test suite in the following JSON format:
{{
    "test_suite": {{
        "language": "{language}",
        "framework": "{framework}",
        "total_tests": 0,
        "coverage_estimate": "0-100%",
        "test_files": [
            {{
                "filename": "test_filename.ext",
                "path": "test_directory/",
                "type": "unit|integration|performance|e2e",
                "content": "complete test file content",
                "tests": [
                    {{
                        "name": "test_function_name",
                        "description": "what this test verifies",
                        "type": "unit|integration|performance|e2e",
                        "target": "function/class being tested",
                        "scenario": "test scenario description"
                    }}
                ]
            }}
        ],
        "test_data": [
            {{
                "name": "test_data_name",
                "type": "fixture|mock|stub",
                "content": "test data content",
                "usage": "how this data is used"
            }}
        ],
        "configuration": {{
            "test_runner_config": "test runner configuration",
            "coverage_config": "coverage configuration", 
            "mock_config": "mocking configuration"
        }},
        "setup_instructions": [
            "how to set up test environment",
            "how to install test dependencies",
            "how to run the tests"
        ],
        "run_commands": {{
            "all_tests": "command to run all tests",
            "unit_tests": "command to run unit tests",
            "integration_tests": "command to run integration tests",
            "coverage": "command to run with coverage"
        }}
    }},
    "quality_metrics": {{
        "test_coverage_target": "target coverage percentage",
        "test_complexity": "low|medium|high",
        "maintainability_score": "0-100",
        "automation_level": "0-100%"
    }},
    "recommendations": [
        "specific testing recommendations",
        "areas that need additional testing",
        "test automation suggestions"
    ]
}}

Generate thorough, production-ready tests that comprehensively validate the code functionality.
"""
    
    async def _parse_test_response(
        self,
        response: str,
        language: str,
        framework: str,
        test_types: List[str],
        code_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse and validate test generation response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            test_data = json.loads(json_str)
            
            # Validate and enhance test data
            test_result = {
                "success": True,
                "language": language,
                "framework": framework,
                "test_types": test_types,
                "generated_at": datetime.now().isoformat(),
                "test_suite": test_data.get("test_suite", {}),
                "quality_metrics": test_data.get("quality_metrics", {}),
                "recommendations": test_data.get("recommendations", []),
                "metadata": {
                    "total_test_files": len(test_data.get("test_suite", {}).get("test_files", [])),
                    "total_tests": test_data.get("test_suite", {}).get("total_tests", 0),
                    "coverage_estimate": test_data.get("test_suite", {}).get("coverage_estimate", "0%"),
                    "test_data_count": len(test_data.get("test_suite", {}).get("test_data", [])),
                    "code_functions": len(code_analysis.get("functions", [])),
                    "code_classes": len(code_analysis.get("classes", []))
                },
                "tokens_used": len(response.split())
            }
            
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Test parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse test response: {str(e)}",
                "raw_response": response,
                "fallback_tests": self._create_fallback_tests(language, framework, code_analysis)
            }
    
    def _create_fallback_tests(self, language: str, framework: str, code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic fallback test structure"""
        
        framework_config = self.test_frameworks.get(language, self.test_frameworks["python"])
        
        # Create basic test file content
        if language == "python":
            test_content = f"""
import pytest
from unittest.mock import Mock, patch

# Basic test structure
class TestBasicFunctionality:
    def test_example_function(self):
        # Arrange
        # Act
        # Assert
        assert True  # Replace with actual test
    
    def test_edge_case(self):
        # Test edge cases
        assert True  # Replace with actual test
        
    def test_error_handling(self):
        # Test error conditions
        with pytest.raises(Exception):
            pass  # Replace with actual test
"""
        else:
            test_content = f"// Basic test structure for {language}\n// TODO: Implement comprehensive tests\n"
        
        return {
            "test_suite": {
                "language": language,
                "framework": framework,
                "total_tests": 3,
                "coverage_estimate": "50%",
                "test_files": [
                    {
                        "filename": f"test_basic.{framework_config.get('test_file_pattern', 'test_*.py').split('*')[1]}",
                        "path": framework_config.get('test_directory', 'tests/'),
                        "type": "unit",
                        "content": test_content,
                        "tests": [
                            {
                                "name": "test_example_function",
                                "description": "Basic functionality test",
                                "type": "unit",
                                "target": "main functionality",
                                "scenario": "happy path"
                            }
                        ]
                    }
                ],
                "test_data": [],
                "configuration": {
                    "test_runner_config": f"Basic {framework} configuration",
                    "coverage_config": "Basic coverage configuration",
                    "mock_config": "Basic mocking configuration"
                },
                "setup_instructions": [
                    f"Install {framework} test framework",
                    "Set up test environment",
                    "Run the test suite"
                ],
                "run_commands": {
                    "all_tests": framework_config.get('coverage', f'{framework} test'),
                    "unit_tests": f"{framework} unit tests",
                    "integration_tests": f"{framework} integration tests",
                    "coverage": framework_config.get('coverage', f'{framework} --coverage')
                }
            },
            "quality_metrics": {
                "test_coverage_target": "80%",
                "test_complexity": "medium",
                "maintainability_score": "70",
                "automation_level": "90%"
            },
            "recommendations": [
                "Implement comprehensive unit tests",
                "Add integration tests for component interactions",
                "Include performance tests for critical paths",
                "Set up continuous integration"
            ]
        }
    
    async def _store_test_results(
        self,
        task_id: str,
        test_result: Dict[str, Any],
        language: str,
        test_types: List[str],
        session_id: Optional[str] = None
    ):
        """Store test generation results in memory"""
        
        content = f"""
Test Generation Results

Task ID: {task_id}
Language: {language}
Test Types: {test_types}
Generated: {datetime.now().isoformat()}

Test Summary:
- Success: {test_result.get('success', False)}
- Total Test Files: {test_result.get('metadata', {}).get('total_test_files', 0)}
- Total Tests: {test_result.get('metadata', {}).get('total_tests', 0)}
- Coverage Estimate: {test_result.get('metadata', {}).get('coverage_estimate', '0%')}
- Test Data Count: {test_result.get('metadata', {}).get('test_data_count', 0)}

Full Test Result:
{json.dumps(test_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.CODE,
            priority=MemoryPriority.HIGH,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "language": language,
                "test_types": test_types,
                "test_success": test_result.get("success", False),
                "total_test_files": test_result.get("metadata", {}).get("total_test_files", 0),
                "total_tests": test_result.get("metadata", {}).get("total_tests", 0)
            },
            tags=["test_generation", "testing", "obelisk", "test_harness"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "supported_languages": list(self.test_frameworks.keys()),
            "supported_frameworks": {
                lang: config["primary"] 
                for lang, config in self.test_frameworks.items()
            },
            "test_types": list(self.test_types.keys()),
            "testing_features": [
                "Unit test generation",
                "Integration test creation",
                "Performance test setup",
                "End-to-end test scenarios",
                "Mock and stub generation",
                "Test data creation",
                "Test configuration",
                "Coverage analysis"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_test_harness_agent(config: Dict[str, Any]) -> TestHarnessAgent:
    """Factory function to create Test Harness Agent"""
    return TestHarnessAgent(config)