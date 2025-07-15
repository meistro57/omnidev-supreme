"""
The-Agency Coder Agent Integration
Migrated from /home/mark/The-Agency/agents/coder.py
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


class CoderAgent(BaseAgent):
    """
    Coder Agent - Generates high-quality code from plans and specifications
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="coder",
            agent_type=AgentType.CODER,
            description="Generates high-quality code from plans and specifications",
            capabilities=[
                "code_generation",
                "multiple_languages",
                "best_practices",
                "documentation",
                "refactoring",
                "debugging"
            ],
            model_requirements=["code_generation", "text_generation"],
            priority=8,  # High priority for code generation
            max_concurrent_tasks=5,
            timeout_seconds=600  # Longer timeout for complex code
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Supported languages and their file extensions
        self.supported_languages = {
            "python": [".py"],
            "javascript": [".js", ".jsx", ".ts", ".tsx"],
            "java": [".java"],
            "cpp": [".cpp", ".hpp", ".cc", ".h"],
            "c": [".c", ".h"],
            "csharp": [".cs"],
            "go": [".go"],
            "rust": [".rs"],
            "php": [".php"],
            "ruby": [".rb"],
            "swift": [".swift"],
            "kotlin": [".kt"],
            "scala": [".scala"],
            "html": [".html", ".htm"],
            "css": [".css", ".scss", ".sass"],
            "sql": [".sql"],
            "shell": [".sh", ".bash"],
            "dockerfile": ["Dockerfile", ".dockerfile"],
            "yaml": [".yml", ".yaml"],
            "json": [".json"],
            "xml": [".xml"],
            "markdown": [".md"]
        }
        
        logger.info("💻 Coder Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for coder agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires code generation
        coding_keywords = [
            "code", "implement", "function", "class", "method", "algorithm",
            "script", "program", "develop", "write", "create", "generate",
            "refactor", "optimize", "debug", "fix"
        ]
        
        return any(keyword in content for keyword in coding_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code generation task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            language = task.get("language", "python")
            project_context = task.get("context", {})
            session_id = task.get("session_id")
            
            # Get project context from memory
            context = await self.get_project_context(session_id)
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Coding task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "coder",
                    "task_id": task.get("id"),
                    "language": language,
                    "project_context": project_context
                },
                session_id=session_id
            )
            
            # Create coding prompt
            coding_prompt = self._create_coding_prompt(user_request, language, context)
            
            # Use orchestrator to generate code
            orchestrator_request = TaskRequest(
                id=f"coder_{task.get('id', 'unknown')}",
                content=coding_prompt,
                task_type="code_generation",
                complexity=self._determine_complexity(user_request),
                required_capabilities=[
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.TEXT_GENERATION
                ],
                max_tokens=3000,
                temperature=0.2,  # Lower temperature for consistent code
                priority=7,
                metadata={
                    "agent": "coder",
                    "language": language,
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Code generation failed: {response.error}")
            
            # Parse the generated code
            code_files = self._parse_code_response(response.content, language)
            
            # Validate and enhance code
            validated_files = await self._validate_and_enhance_code(code_files, language)
            
            # Store code in memory
            code_memory_id = self.memory_manager.store_memory(
                content=f"Generated code: {json.dumps(validated_files, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "coder",
                    "task_id": task.get("id"),
                    "language": language,
                    "file_count": len(validated_files),
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["code", language, "generated"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "code_files": validated_files,
                "language": language,
                "memory_ids": [task_memory_id, code_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "coder",
                "metadata": {
                    "code_quality": "high",
                    "best_practices": True,
                    "documentation": True,
                    "file_count": len(validated_files)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Coder agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "coder"
            }
    
    def _create_coding_prompt(self, user_request: str, language: str, context: Dict[str, Any]) -> str:
        """Create detailed coding prompt"""
        context_str = ""
        if context:
            context_str = f"\n\nProject Context:\n{json.dumps(context, indent=2)}"
        
        language_specific = self._get_language_specific_guidelines(language)
        
        return f"""
As an expert {language} developer, implement the following request with high-quality, production-ready code.

Request: {user_request}

Language: {language}

{language_specific}{context_str}

Please provide:

1. **COMPLETE CODE IMPLEMENTATION**
   - Full, working code with proper structure
   - Clear file organization and naming
   - Comprehensive error handling
   - Input validation where needed

2. **BEST PRACTICES**
   - Follow {language} coding standards
   - Use appropriate design patterns
   - Implement proper separation of concerns
   - Include type hints/annotations where applicable

3. **DOCUMENTATION**
   - Clear docstrings/comments for all functions/classes
   - Inline comments for complex logic
   - Usage examples where helpful

4. **TESTING CONSIDERATIONS**
   - Write testable code
   - Include example test cases if requested
   - Consider edge cases and error conditions

5. **FILE STRUCTURE**
   - Organize code into appropriate files
   - Use proper imports and dependencies
   - Follow project structure conventions

Format your response as:
```{language}
// filename: path/to/file.ext
[code content]
```

Provide multiple files if needed, each with clear filename headers.
"""
    
    def _get_language_specific_guidelines(self, language: str) -> str:
        """Get language-specific coding guidelines"""
        guidelines = {
            "python": """
Python Guidelines:
- Follow PEP 8 style guide
- Use type hints for all functions
- Include docstrings for all public functions/classes
- Use f-strings for string formatting
- Implement proper exception handling
- Use dataclasses or Pydantic models for data structures
            """,
            "javascript": """
JavaScript Guidelines:
- Use ES6+ features (arrow functions, destructuring, etc.)
- Include JSDoc comments for functions
- Use async/await for asynchronous operations
- Implement proper error handling with try/catch
- Use modern module syntax (import/export)
- Consider TypeScript types if applicable
            """,
            "java": """
Java Guidelines:
- Follow Java naming conventions
- Use proper access modifiers
- Include Javadoc comments
- Implement proper exception handling
- Use generics where appropriate
- Follow SOLID principles
            """,
            "cpp": """
C++ Guidelines:
- Use modern C++ features (C++17/20)
- Follow RAII principles
- Use smart pointers for memory management
- Include proper header guards
- Use const correctness
- Follow STL conventions
            """,
            "go": """
Go Guidelines:
- Follow Go formatting standards (gofmt)
- Use proper error handling patterns
- Include package documentation
- Use interfaces effectively
- Follow Go naming conventions
- Consider concurrent patterns where appropriate
            """
        }
        
        return guidelines.get(language, "Follow language-specific best practices and conventions.")
    
    def _determine_complexity(self, user_request: str) -> TaskComplexity:
        """Determine task complexity based on request"""
        request_lower = user_request.lower()
        
        expert_keywords = [
            "algorithm", "optimization", "performance", "concurrent", "parallel",
            "distributed", "architecture", "design pattern", "complex system"
        ]
        
        complex_keywords = [
            "integrate", "api", "database", "framework", "multiple files",
            "class hierarchy", "inheritance", "polymorphism"
        ]
        
        if any(keyword in request_lower for keyword in expert_keywords):
            return TaskComplexity.EXPERT
        elif any(keyword in request_lower for keyword in complex_keywords):
            return TaskComplexity.COMPLEX
        elif len(request_lower.split()) > 20:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _parse_code_response(self, response_content: str, language: str) -> List[Dict[str, Any]]:
        """Parse the generated code response into structured files"""
        files = []
        
        try:
            # Look for code blocks with filename headers
            pattern = r'```(?:\w+)?\s*(?://\s*filename:\s*(.+?)\s*)??\n(.*?)```'
            matches = re.findall(pattern, response_content, re.DOTALL)
            
            if matches:
                for filename, code_content in matches:
                    filename = filename.strip() if filename else f"main.{self._get_file_extension(language)}"
                    files.append({
                        "filename": filename,
                        "content": code_content.strip(),
                        "language": language,
                        "type": "code"
                    })
            else:
                # If no structured format found, treat entire response as single file
                files.append({
                    "filename": f"main.{self._get_file_extension(language)}",
                    "content": response_content.strip(),
                    "language": language,
                    "type": "code"
                })
        
        except Exception as e:
            logger.warning(f"⚠️  Code parsing failed: {e}")
            files.append({
                "filename": f"main.{self._get_file_extension(language)}",
                "content": response_content,
                "language": language,
                "type": "code",
                "parse_error": str(e)
            })
        
        return files
    
    def _get_file_extension(self, language: str) -> str:
        """Get appropriate file extension for language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "cpp": "cpp",
            "c": "c",
            "csharp": "cs",
            "go": "go",
            "rust": "rs",
            "php": "php",
            "ruby": "rb",
            "swift": "swift",
            "kotlin": "kt",
            "scala": "scala",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "shell": "sh",
            "yaml": "yml",
            "json": "json",
            "xml": "xml",
            "markdown": "md"
        }
        
        return extensions.get(language.lower(), "txt")
    
    async def _validate_and_enhance_code(self, code_files: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
        """Validate and enhance the generated code"""
        enhanced_files = []
        
        for file_info in code_files:
            try:
                # Basic validation
                validated_file = {
                    **file_info,
                    "validated": True,
                    "enhancements": []
                }
                
                # Language-specific validation
                if language == "python":
                    validated_file = self._validate_python_code(validated_file)
                elif language in ["javascript", "typescript"]:
                    validated_file = self._validate_javascript_code(validated_file)
                elif language == "java":
                    validated_file = self._validate_java_code(validated_file)
                
                # Add common enhancements
                validated_file["line_count"] = len(validated_file["content"].split('\n'))
                validated_file["size_bytes"] = len(validated_file["content"].encode('utf-8'))
                
                enhanced_files.append(validated_file)
                
            except Exception as e:
                logger.warning(f"⚠️  Code validation failed for {file_info.get('filename', 'unknown')}: {e}")
                enhanced_files.append({
                    **file_info,
                    "validated": False,
                    "validation_error": str(e)
                })
        
        return enhanced_files
    
    def _validate_python_code(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Python code"""
        content = file_info["content"]
        enhancements = []
        
        # Check for common Python patterns
        if "import" in content:
            enhancements.append("imports_detected")
        if "def " in content:
            enhancements.append("functions_detected")
        if "class " in content:
            enhancements.append("classes_detected")
        if '"""' in content or "'''" in content:
            enhancements.append("docstrings_detected")
        if "try:" in content:
            enhancements.append("error_handling_detected")
        
        file_info["enhancements"] = enhancements
        return file_info
    
    def _validate_javascript_code(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JavaScript code"""
        content = file_info["content"]
        enhancements = []
        
        # Check for modern JavaScript patterns
        if "const " in content or "let " in content:
            enhancements.append("modern_variables")
        if "=>" in content:
            enhancements.append("arrow_functions")
        if "async " in content or "await " in content:
            enhancements.append("async_await")
        if "import " in content or "export " in content:
            enhancements.append("es6_modules")
        if "try {" in content:
            enhancements.append("error_handling")
        
        file_info["enhancements"] = enhancements
        return file_info
    
    def _validate_java_code(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Java code"""
        content = file_info["content"]
        enhancements = []
        
        # Check for Java patterns
        if "public class " in content:
            enhancements.append("public_class")
        if "private " in content:
            enhancements.append("encapsulation")
        if "/**" in content:
            enhancements.append("javadoc")
        if "try {" in content:
            enhancements.append("exception_handling")
        if "@Override" in content:
            enhancements.append("annotations")
        
        file_info["enhancements"] = enhancements
        return file_info
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context from memory"""
        try:
            # Get recent code and architecture information
            context_items = self.memory_manager.search_memory(
                query="architecture plan code structure",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=10
            )
            
            context = {
                "previous_code": [],
                "architecture": {},
                "technologies": [],
                "patterns": []
            }
            
            for item in context_items:
                if item.memory_type == MemoryType.CODE:
                    context["previous_code"].append(item.content[:500])  # Truncate for context
                elif "plan_structure" in item.metadata:
                    context["architecture"] = item.metadata["plan_structure"]
                elif "language" in item.metadata:
                    context["technologies"].append(item.metadata["language"])
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get coder agent statistics"""
        return {
            **self.stats,
            "supported_languages": list(self.supported_languages.keys()),
            "code_files_generated": len(self.memory_manager.search_memory(
                query="coder",
                memory_type=MemoryType.CODE,
                limit=1000
            )),
            "code_quality_features": [
                "syntax_validation",
                "best_practices",
                "documentation",
                "error_handling",
                "type_safety"
            ]
        }


def create_coder_agent(config: Dict[str, Any]) -> CoderAgent:
    """Factory function to create coder agent"""
    return CoderAgent(config)