"""
OBELISK Code Generator Agent
Generates code based on architecture plans and specifications
"""

import asyncio
import json
import os
import tempfile
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class CodeGeneratorAgent(BaseAgent):
    """
    OBELISK Code Generator Agent
    
    Specializes in:
    - Code generation from specifications
    - File structure creation
    - Implementation from architectural plans
    - Code scaffolding and boilerplate
    - Multi-language code generation
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="code_generator",
            agent_type=AgentType.CODER,
            description="OBELISK Code Generator - Generates code from architecture plans and specifications",
            capabilities=[
                "code_generation_from_specs",
                "file_structure_creation",
                "architecture_based_implementation",
                "code_scaffolding",
                "multi_language_support",
                "boilerplate_generation",
                "project_setup",
                "dependency_management"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=8,
            max_concurrent_tasks=3,
            timeout_seconds=900,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Supported languages and frameworks
        self.supported_languages = {
            "python": {
                "frameworks": ["fastapi", "flask", "django", "pydantic", "sqlalchemy"],
                "file_extensions": [".py"],
                "package_manager": "pip",
                "config_files": ["requirements.txt", "pyproject.toml", "setup.py"]
            },
            "javascript": {
                "frameworks": ["react", "vue", "angular", "express", "nodejs"],
                "file_extensions": [".js", ".jsx"],
                "package_manager": "npm",
                "config_files": ["package.json", "webpack.config.js"]
            },
            "typescript": {
                "frameworks": ["react", "vue", "angular", "express", "nestjs"],
                "file_extensions": [".ts", ".tsx"],
                "package_manager": "npm",
                "config_files": ["package.json", "tsconfig.json"]
            },
            "java": {
                "frameworks": ["spring", "springboot", "maven", "gradle"],
                "file_extensions": [".java"],
                "package_manager": "maven",
                "config_files": ["pom.xml", "build.gradle"]
            },
            "go": {
                "frameworks": ["gin", "echo", "fiber", "gorilla"],
                "file_extensions": [".go"],
                "package_manager": "go mod",
                "config_files": ["go.mod", "go.sum"]
            }
        }
        
        # Code generation templates
        self.code_templates = {
            "api_server": {
                "python": "fastapi_server_template",
                "javascript": "express_server_template",
                "typescript": "nestjs_server_template",
                "java": "springboot_server_template",
                "go": "gin_server_template"
            },
            "web_app": {
                "javascript": "react_app_template",
                "typescript": "react_ts_app_template",
                "python": "flask_web_template"
            },
            "microservice": {
                "python": "fastapi_microservice_template",
                "java": "springboot_microservice_template",
                "go": "go_microservice_template"
            },
            "data_processing": {
                "python": "pandas_processing_template",
                "java": "spark_processing_template"
            }
        }
        
        logger.info(f"🔧 {self.metadata.name} initialized with multi-language code generation capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for code generator agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires code generation
        code_keywords = [
            "code", "generate", "implement", "write", "create", "build",
            "program", "script", "function", "class", "module", "library"
        ]
        
        return any(keyword in content for keyword in code_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code generation task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"codegen_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"🔧 Starting code generation: {task_id}")
            
            # Extract task parameters
            requirements = task.get("content", "")
            language = task.get("language", "python")
            framework = task.get("framework", "")
            architecture_plan = task.get("architecture_plan", {})
            context = task.get("context", {})
            
            # Generate code based on requirements
            generation_result = await self._generate_code_from_specs(
                requirements=requirements,
                language=language,
                framework=framework,
                architecture_plan=architecture_plan,
                context=context
            )
            
            # Store results in memory
            await self._store_generation_results(
                task_id=task_id,
                generation_result=generation_result,
                language=language,
                framework=framework,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "code_generation": generation_result,
                "language": language,
                "framework": framework,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"codegen_{task_id}",
                "tokens_used": generation_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Code generation completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Code generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_code_from_specs(
        self,
        requirements: str,
        language: str,
        framework: str,
        architecture_plan: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate code based on specifications"""
        
        # Validate language support
        if language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {language}")
        
        lang_config = self.supported_languages[language]
        
        # Determine project type from architecture or requirements
        project_type = self._determine_project_type(requirements, architecture_plan)
        
        # Create code generation prompt
        code_prompt = self._create_code_generation_prompt(
            requirements=requirements,
            language=language,
            framework=framework,
            project_type=project_type,
            architecture_plan=architecture_plan,
            lang_config=lang_config,
            context=context
        )
        
        # Generate code using best available model
        try:
            response = await self.orchestrator.generate_response(
                prompt=code_prompt,
                model_preference=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
                temperature=0.2,  # Low temperature for consistent code
                max_tokens=6000
            )
            
            # Parse and structure code response
            code_result = await self._parse_code_response(
                response=response,
                language=language,
                framework=framework,
                project_type=project_type
            )
            
            return code_result
            
        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_code": self._create_fallback_code(language, framework, project_type)
            }
    
    def _determine_project_type(self, requirements: str, architecture_plan: Dict[str, Any]) -> str:
        """Determine project type from requirements and architecture"""
        
        # Check architecture plan first
        if architecture_plan:
            plan_data = architecture_plan.get("plan", {})
            if "api" in str(plan_data).lower() or "rest" in str(plan_data).lower():
                return "api_server"
            elif "web" in str(plan_data).lower() or "frontend" in str(plan_data).lower():
                return "web_app"
            elif "microservice" in str(plan_data).lower():
                return "microservice"
            elif "data" in str(plan_data).lower() or "processing" in str(plan_data).lower():
                return "data_processing"
        
        # Analyze requirements
        req_lower = requirements.lower()
        if any(word in req_lower for word in ["api", "rest", "endpoint", "server"]):
            return "api_server"
        elif any(word in req_lower for word in ["web", "frontend", "ui", "interface"]):
            return "web_app"
        elif any(word in req_lower for word in ["microservice", "service", "distributed"]):
            return "microservice"
        elif any(word in req_lower for word in ["data", "processing", "etl", "pipeline"]):
            return "data_processing"
        
        # Default to API server
        return "api_server"
    
    def _create_code_generation_prompt(
        self,
        requirements: str,
        language: str,
        framework: str,
        project_type: str,
        architecture_plan: Dict[str, Any],
        lang_config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed code generation prompt"""
        
        architecture_context = ""
        if architecture_plan and architecture_plan.get("plan"):
            plan_data = architecture_plan["plan"]
            architecture_context = f"""
ARCHITECTURE CONTEXT:
- Technology Stack: {plan_data.get('technology_stack', {})}
- System Components: {[comp.get('name', '') for comp in plan_data.get('components', [])]}
- Data Flow: {plan_data.get('system_architecture', {}).get('data_flow', 'Not specified')}
- Security Requirements: {plan_data.get('security', {})}
"""
        
        return f"""
You are an expert software developer tasked with generating high-quality, production-ready code.

PROJECT REQUIREMENTS:
{requirements}

TECHNICAL SPECIFICATIONS:
- Language: {language}
- Framework: {framework if framework else 'Standard library'}
- Project Type: {project_type}
- Supported Frameworks: {lang_config.get('frameworks', [])}
- Package Manager: {lang_config.get('package_manager', 'N/A')}

{architecture_context}

CONTEXT:
{context}

CODE GENERATION REQUIREMENTS:
1. Generate complete, working code that follows best practices
2. Include proper error handling and validation
3. Add comprehensive documentation and comments
4. Follow language-specific conventions and style guides
5. Include necessary imports and dependencies
6. Structure code in a logical, maintainable way
7. Add configuration files and setup instructions
8. Include basic tests where appropriate

DELIVERABLES:
Please provide the code generation results in the following JSON format:
{{
    "project_structure": {{
        "root_directory": "project_name",
        "directories": ["dir1", "dir2", "dir3"],
        "files": [
            {{
                "path": "relative/path/to/file.ext",
                "type": "source|config|test|doc",
                "purpose": "description of file purpose"
            }}
        ]
    }},
    "code_files": [
        {{
            "filename": "filename.ext",
            "path": "relative/path/",
            "content": "complete file content",
            "type": "source|config|test|doc",
            "purpose": "description",
            "dependencies": ["dependency1", "dependency2"]
        }}
    ],
    "configuration": {{
        "dependencies": [
            {{
                "name": "dependency_name",
                "version": "version_spec",
                "purpose": "what this dependency does"
            }}
        ],
        "environment_variables": [
            {{
                "name": "VAR_NAME",
                "description": "variable description",
                "required": true,
                "example": "example_value"
            }}
        ],
        "config_files": [
            {{
                "filename": "config_file.ext",
                "content": "complete config file content",
                "purpose": "configuration purpose"
            }}
        ]
    }},
    "setup_instructions": [
        "Step 1: Install dependencies",
        "Step 2: Set up environment",
        "Step 3: Run the application"
    ],
    "usage_examples": [
        {{
            "title": "Basic Usage",
            "description": "How to use the basic functionality",
            "code": "example code snippet"
        }}
    ],
    "testing": {{
        "test_framework": "framework_name",
        "test_files": [
            {{
                "filename": "test_file.ext",
                "content": "test file content",
                "purpose": "what this test covers"
            }}
        ],
        "run_command": "command to run tests"
    }}
}}

Focus on creating clean, maintainable, and well-documented code that solves the specified requirements.
"""
    
    async def _parse_code_response(
        self,
        response: str,
        language: str,
        framework: str,
        project_type: str
    ) -> Dict[str, Any]:
        """Parse and validate code generation response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            code_data = json.loads(json_str)
            
            # Validate and enhance code data
            generation_result = {
                "success": True,
                "language": language,
                "framework": framework,
                "project_type": project_type,
                "generated_at": datetime.now().isoformat(),
                "code_generation": code_data,
                "metadata": {
                    "files_count": len(code_data.get("code_files", [])),
                    "dependencies_count": len(code_data.get("configuration", {}).get("dependencies", [])),
                    "test_files_count": len(code_data.get("testing", {}).get("test_files", [])),
                    "config_files_count": len(code_data.get("configuration", {}).get("config_files", []))
                },
                "tokens_used": len(response.split())
            }
            
            return generation_result
            
        except Exception as e:
            logger.error(f"❌ Code parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse code: {str(e)}",
                "raw_response": response,
                "fallback_code": self._create_fallback_code(language, framework, project_type)
            }
    
    def _create_fallback_code(self, language: str, framework: str, project_type: str) -> Dict[str, Any]:
        """Create basic fallback code structure"""
        
        if language == "python":
            return {
                "project_structure": {
                    "root_directory": "generated_project",
                    "directories": ["src", "tests", "config"],
                    "files": [
                        {"path": "src/main.py", "type": "source", "purpose": "Main application entry point"},
                        {"path": "requirements.txt", "type": "config", "purpose": "Python dependencies"},
                        {"path": "README.md", "type": "doc", "purpose": "Project documentation"}
                    ]
                },
                "code_files": [
                    {
                        "filename": "main.py",
                        "path": "src/",
                        "content": '#!/usr/bin/env python3\n"""Main application module"""\n\ndef main():\n    """Main entry point"""\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
                        "type": "source",
                        "purpose": "Main application entry point",
                        "dependencies": []
                    }
                ],
                "configuration": {
                    "dependencies": [],
                    "environment_variables": [],
                    "config_files": [
                        {
                            "filename": "requirements.txt",
                            "content": "# Add your dependencies here\n",
                            "purpose": "Python package dependencies"
                        }
                    ]
                },
                "setup_instructions": [
                    "1. Install Python 3.8+",
                    "2. Create virtual environment: python -m venv venv",
                    "3. Activate virtual environment: source venv/bin/activate",
                    "4. Install dependencies: pip install -r requirements.txt",
                    "5. Run application: python src/main.py"
                ],
                "usage_examples": [
                    {
                        "title": "Basic Usage",
                        "description": "Run the main application",
                        "code": "python src/main.py"
                    }
                ],
                "testing": {
                    "test_framework": "pytest",
                    "test_files": [],
                    "run_command": "pytest tests/"
                }
            }
        else:
            # Generic fallback for other languages
            return {
                "project_structure": {
                    "root_directory": "generated_project",
                    "directories": ["src", "tests"],
                    "files": [
                        {"path": "src/main", "type": "source", "purpose": "Main application file"},
                        {"path": "README.md", "type": "doc", "purpose": "Project documentation"}
                    ]
                },
                "code_files": [
                    {
                        "filename": f"main.{self.supported_languages.get(language, {}).get('file_extensions', ['.txt'])[0][1:]}",
                        "path": "src/",
                        "content": f"// {language} application\n// TODO: Implement your code here\n",
                        "type": "source",
                        "purpose": "Main application file",
                        "dependencies": []
                    }
                ],
                "configuration": {
                    "dependencies": [],
                    "environment_variables": [],
                    "config_files": []
                },
                "setup_instructions": [
                    f"1. Set up {language} development environment",
                    "2. Install dependencies",
                    "3. Build and run the application"
                ],
                "usage_examples": [],
                "testing": {
                    "test_framework": "standard",
                    "test_files": [],
                    "run_command": "Run your test command"
                }
            }
    
    async def _store_generation_results(
        self,
        task_id: str,
        generation_result: Dict[str, Any],
        language: str,
        framework: str,
        session_id: Optional[str] = None
    ):
        """Store code generation results in memory"""
        
        content = f"""
Code Generation Results

Task ID: {task_id}
Language: {language}
Framework: {framework}
Generated: {datetime.now().isoformat()}

Generation Summary:
- Success: {generation_result.get('success', False)}
- Files Generated: {generation_result.get('metadata', {}).get('files_count', 0)}
- Dependencies: {generation_result.get('metadata', {}).get('dependencies_count', 0)}
- Test Files: {generation_result.get('metadata', {}).get('test_files_count', 0)}

Full Generation Result:
{json.dumps(generation_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.CODE,
            priority=MemoryPriority.HIGH,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "language": language,
                "framework": framework,
                "generation_success": generation_result.get("success", False),
                "files_count": generation_result.get("metadata", {}).get("files_count", 0)
            },
            tags=["code_generation", "implementation", "obelisk", "code_generator"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "supported_languages": list(self.supported_languages.keys()),
            "supported_frameworks": {
                lang: config["frameworks"] 
                for lang, config in self.supported_languages.items()
            },
            "project_types": list(self.code_templates.keys()),
            "generation_features": [
                "Complete project structure",
                "Multi-file code generation",
                "Dependency management",
                "Configuration files",
                "Setup instructions",
                "Usage examples",
                "Test scaffolding"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_code_generator_agent(config: Dict[str, Any]) -> CodeGeneratorAgent:
    """Factory function to create Code Generator Agent"""
    return CodeGeneratorAgent(config)