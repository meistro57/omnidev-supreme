"""
The-Agency Tester Agent Integration
Migrated from /home/mark/The-Agency/agents/tester.py
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class TesterAgent(BaseAgent):
    """
    Tester Agent - Creates comprehensive tests for generated code
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="tester",
            agent_type=AgentType.TESTER,
            description="Creates comprehensive tests for generated code",
            capabilities=[
                "unit_testing",
                "integration_testing",
                "test_generation",
                "test_automation",
                "coverage_analysis",
                "performance_testing",
                "edge_case_testing"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=7,  # High priority for quality assurance
            max_concurrent_tasks=4,
            timeout_seconds=480  # Longer timeout for comprehensive testing
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Testing frameworks by language
        self.test_frameworks = {
            "python": {
                "frameworks": ["pytest", "unittest", "nose2"],
                "default": "pytest",
                "imports": ["import pytest", "from unittest.mock import Mock, patch"],
                "extensions": [".py"]
            },
            "javascript": {
                "frameworks": ["jest", "mocha", "jasmine"],
                "default": "jest",
                "imports": ["const { test, expect } = require('@jest/globals');"],
                "extensions": [".js", ".ts"]
            },
            "java": {
                "frameworks": ["junit5", "junit4", "testng"],
                "default": "junit5",
                "imports": ["import org.junit.jupiter.api.Test;", "import static org.junit.jupiter.api.Assertions.*;"],
                "extensions": [".java"]
            },
            "csharp": {
                "frameworks": ["nunit", "xunit", "mstest"],
                "default": "nunit",
                "imports": ["using NUnit.Framework;"],
                "extensions": [".cs"]
            },
            "go": {
                "frameworks": ["testing", "ginkgo", "testify"],
                "default": "testing",
                "imports": ["import \"testing\""],
                "extensions": [".go"]
            },
            "rust": {
                "frameworks": ["built-in", "proptest"],
                "default": "built-in",
                "imports": ["#[cfg(test)]", "use super::*;"],
                "extensions": [".rs"]
            }
        }
        
        logger.info("🧪 Tester Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for tester agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires testing
        testing_keywords = [
            "test", "testing", "unit test", "integration test", "coverage",
            "validate", "verify", "check", "assert", "mock", "stub"
        ]
        
        return any(keyword in content for keyword in testing_keywords) or task_type == "testing"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute test generation task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            language = task.get("language", "python")
            code_to_test = task.get("code_to_test", "")
            session_id = task.get("session_id")
            
            # Get project context and existing code
            context = await self.get_project_context(session_id)
            if not code_to_test and context.get("recent_code"):
                code_to_test = context["recent_code"]
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Testing task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "tester",
                    "task_id": task.get("id"),
                    "language": language,
                    "code_to_test": code_to_test[:500] if code_to_test else None
                },
                session_id=session_id
            )
            
            # Create testing prompt
            testing_prompt = self._create_testing_prompt(user_request, language, code_to_test, context)
            
            # Use orchestrator to generate tests
            orchestrator_request = TaskRequest(
                id=f"tester_{task.get('id', 'unknown')}",
                content=testing_prompt,
                task_type="code_generation",
                complexity=self._determine_complexity(user_request, code_to_test),
                required_capabilities=[
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.REASONING
                ],
                max_tokens=2500,
                temperature=0.1,  # Very low temperature for consistent, reliable tests
                priority=7,
                metadata={
                    "agent": "tester",
                    "language": language,
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Test generation failed: {response.error}")
            
            # Parse the generated tests
            test_files = self._parse_test_response(response.content, language)
            
            # Validate and enhance tests
            validated_tests = await self._validate_and_enhance_tests(test_files, language, code_to_test)
            
            # Store tests in memory
            test_memory_id = self.memory_manager.store_memory(
                content=f"Generated tests: {json.dumps(validated_tests, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "tester",
                    "task_id": task.get("id"),
                    "language": language,
                    "test_count": len(validated_tests),
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["tests", language, "generated", "quality_assurance"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "test_files": validated_tests,
                "language": language,
                "test_framework": self.test_frameworks.get(language, {}).get("default", "default"),
                "memory_ids": [task_memory_id, test_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "tester",
                "metadata": {
                    "test_quality": "comprehensive",
                    "coverage_target": "high",
                    "test_types": ["unit", "integration", "edge_cases"],
                    "test_count": len(validated_tests)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Tester agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "tester"
            }
    
    def _create_testing_prompt(self, user_request: str, language: str, code_to_test: str, context: Dict[str, Any]) -> str:
        """Create detailed testing prompt"""
        framework_info = self.test_frameworks.get(language, {})
        framework = framework_info.get("default", "default")
        imports = "\n".join(framework_info.get("imports", []))
        
        context_str = ""
        if context.get("architecture"):
            context_str = f"\n\nProject Architecture:\n{json.dumps(context['architecture'], indent=2)}"
        
        code_section = ""
        if code_to_test:
            code_section = f"\n\nCode to Test:\n```{language}\n{code_to_test}\n```"
        
        return f"""
As an expert {language} testing engineer, create comprehensive tests for the following request using {framework}.

Request: {user_request}

Language: {language}
Testing Framework: {framework}
Required Imports: {imports}{code_section}{context_str}

Please create comprehensive tests that include:

1. **UNIT TESTS**
   - Test individual functions/methods
   - Test normal cases with valid inputs
   - Test edge cases and boundary conditions
   - Test error conditions and exceptions
   - Mock external dependencies

2. **INTEGRATION TESTS**
   - Test component interactions
   - Test API endpoints (if applicable)
   - Test database operations (if applicable)
   - Test file I/O operations (if applicable)

3. **EDGE CASE TESTS**
   - Empty inputs
   - Null/None values
   - Very large inputs
   - Invalid data types
   - Concurrent access scenarios

4. **PERFORMANCE TESTS** (if applicable)
   - Test response times
   - Test memory usage
   - Test scalability limits

5. **SETUP AND TEARDOWN**
   - Proper test fixtures
   - Clean test environment
   - Mock configurations

Requirements:
- Use {framework} syntax and best practices
- Include descriptive test names
- Add comments explaining test purpose
- Use appropriate assertions
- Include setup/teardown where needed
- Test both success and failure scenarios
- Aim for high code coverage

Format your response as:
```{language}
// filename: test_filename.{framework_info.get('extensions', ['.py'])[0]}
[test code here]
```

Provide separate test files if needed for different test types.
"""
    
    def _determine_complexity(self, user_request: str, code_to_test: str) -> TaskComplexity:
        """Determine task complexity based on request and code"""
        complexity_factors = 0
        
        # Check request complexity
        request_lower = user_request.lower()
        if any(keyword in request_lower for keyword in ["comprehensive", "extensive", "complex", "integration"]):
            complexity_factors += 2
        if any(keyword in request_lower for keyword in ["performance", "load", "stress", "concurrent"]):
            complexity_factors += 2
        
        # Check code complexity
        if code_to_test:
            lines = len(code_to_test.split('\n'))
            if lines > 100:
                complexity_factors += 2
            elif lines > 50:
                complexity_factors += 1
            
            # Check for complex patterns
            if any(pattern in code_to_test for pattern in ["async", "await", "threading", "multiprocessing"]):
                complexity_factors += 1
            if any(pattern in code_to_test for pattern in ["database", "api", "network", "file"]):
                complexity_factors += 1
        
        if complexity_factors >= 4:
            return TaskComplexity.EXPERT
        elif complexity_factors >= 2:
            return TaskComplexity.COMPLEX
        elif complexity_factors >= 1:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _parse_test_response(self, response_content: str, language: str) -> List[Dict[str, Any]]:
        """Parse the generated test response into structured files"""
        test_files = []
        
        try:
            # Look for test code blocks with filename headers
            pattern = r'```(?:\w+)?\s*(?://\s*filename:\s*(.+?)\s*)??\n(.*?)```'
            matches = re.findall(pattern, response_content, re.DOTALL)
            
            if matches:
                for filename, test_content in matches:
                    if not filename.strip():
                        filename = f"test_main.{self._get_test_extension(language)}"
                    else:
                        filename = filename.strip()
                    
                    test_files.append({
                        "filename": filename,
                        "content": test_content.strip(),
                        "language": language,
                        "type": "test",
                        "test_framework": self.test_frameworks.get(language, {}).get("default", "default")
                    })
            else:
                # If no structured format found, treat entire response as single test file
                test_files.append({
                    "filename": f"test_main.{self._get_test_extension(language)}",
                    "content": response_content.strip(),
                    "language": language,
                    "type": "test",
                    "test_framework": self.test_frameworks.get(language, {}).get("default", "default")
                })
        
        except Exception as e:
            logger.warning(f"⚠️  Test parsing failed: {e}")
            test_files.append({
                "filename": f"test_main.{self._get_test_extension(language)}",
                "content": response_content,
                "language": language,
                "type": "test",
                "parse_error": str(e)
            })
        
        return test_files
    
    def _get_test_extension(self, language: str) -> str:
        """Get appropriate test file extension for language"""
        framework_info = self.test_frameworks.get(language, {})
        extensions = framework_info.get("extensions", [".py"])
        return extensions[0].lstrip('.')
    
    async def _validate_and_enhance_tests(self, test_files: List[Dict[str, Any]], language: str, code_to_test: str) -> List[Dict[str, Any]]:
        """Validate and enhance the generated tests"""
        enhanced_tests = []
        
        for test_info in test_files:
            try:
                # Basic validation
                validated_test = {
                    **test_info,
                    "validated": True,
                    "test_stats": {},
                    "quality_checks": []
                }
                
                # Language-specific validation
                if language == "python":
                    validated_test = self._validate_python_tests(validated_test)
                elif language in ["javascript", "typescript"]:
                    validated_test = self._validate_javascript_tests(validated_test)
                elif language == "java":
                    validated_test = self._validate_java_tests(validated_test)
                
                # Common test quality checks
                test_content = validated_test["content"]
                validated_test["test_stats"] = {
                    "line_count": len(test_content.split('\n')),
                    "test_functions": len(re.findall(r'def test_|function test|@Test', test_content)),
                    "assertions": len(re.findall(r'assert|expect|Assert', test_content, re.IGNORECASE)),
                    "mocks": len(re.findall(r'mock|Mock|stub|Stub', test_content, re.IGNORECASE))
                }
                
                enhanced_tests.append(validated_test)
                
            except Exception as e:
                logger.warning(f"⚠️  Test validation failed for {test_info.get('filename', 'unknown')}: {e}")
                enhanced_tests.append({
                    **test_info,
                    "validated": False,
                    "validation_error": str(e)
                })
        
        return enhanced_tests
    
    def _validate_python_tests(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Python test code"""
        content = test_info["content"]
        quality_checks = []
        
        # Check for pytest patterns
        if "pytest" in content:
            quality_checks.append("pytest_framework")
        if "def test_" in content:
            quality_checks.append("test_functions")
        if "assert " in content:
            quality_checks.append("assertions")
        if "mock" in content.lower():
            quality_checks.append("mocking")
        if "fixture" in content:
            quality_checks.append("fixtures")
        if "parametrize" in content:
            quality_checks.append("parameterized_tests")
        
        test_info["quality_checks"] = quality_checks
        return test_info
    
    def _validate_javascript_tests(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JavaScript test code"""
        content = test_info["content"]
        quality_checks = []
        
        # Check for Jest patterns
        if "test(" in content or "it(" in content:
            quality_checks.append("test_functions")
        if "expect(" in content:
            quality_checks.append("assertions")
        if "describe(" in content:
            quality_checks.append("test_suites")
        if "beforeEach" in content or "afterEach" in content:
            quality_checks.append("setup_teardown")
        if "mock" in content.lower():
            quality_checks.append("mocking")
        
        test_info["quality_checks"] = quality_checks
        return test_info
    
    def _validate_java_tests(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Java test code"""
        content = test_info["content"]
        quality_checks = []
        
        # Check for JUnit patterns
        if "@Test" in content:
            quality_checks.append("test_annotations")
        if "Assert" in content:
            quality_checks.append("assertions")
        if "@Before" in content or "@After" in content:
            quality_checks.append("setup_teardown")
        if "Mock" in content:
            quality_checks.append("mocking")
        if "@ParameterizedTest" in content:
            quality_checks.append("parameterized_tests")
        
        test_info["quality_checks"] = quality_checks
        return test_info
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context and recent code from memory"""
        try:
            # Get recent code for testing
            code_items = self.memory_manager.search_memory(
                query="code generated",
                memory_type=MemoryType.CODE,
                use_vector=True,
                limit=5
            )
            
            # Get architecture information
            architecture_items = self.memory_manager.search_memory(
                query="architecture plan",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=3
            )
            
            context = {
                "recent_code": "",
                "architecture": {},
                "functions": [],
                "classes": []
            }
            
            # Extract recent code
            if code_items:
                recent_code = code_items[0].content
                if "Generated code:" in recent_code:
                    try:
                        code_data = json.loads(recent_code.split("Generated code:")[1].strip())
                        if isinstance(code_data, list) and code_data:
                            context["recent_code"] = code_data[0].get("content", "")
                    except:
                        pass
            
            # Extract architecture
            for item in architecture_items:
                if "plan_structure" in item.metadata:
                    context["architecture"] = item.metadata["plan_structure"]
                    break
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get tester agent statistics"""
        return {
            **self.stats,
            "supported_languages": list(self.test_frameworks.keys()),
            "test_frameworks": {
                lang: info["frameworks"] for lang, info in self.test_frameworks.items()
            },
            "test_files_generated": len(self.memory_manager.search_memory(
                query="tester",
                memory_type=MemoryType.CODE,
                limit=1000
            )),
            "quality_features": [
                "unit_testing",
                "integration_testing",
                "edge_case_testing",
                "mocking",
                "performance_testing",
                "coverage_analysis"
            ]
        }


def create_tester_agent(config: Dict[str, Any]) -> TesterAgent:
    """Factory function to create tester agent"""
    return TesterAgent(config)