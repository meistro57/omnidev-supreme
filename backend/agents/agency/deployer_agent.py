"""
The-Agency Deployer Agent Integration
Migrated from /home/mark/The-Agency/agents/deployer.py
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


class DeployerAgent(BaseAgent):
    """
    Deployer Agent - Handles deployment and DevOps tasks
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="deployer",
            agent_type=AgentType.DEPLOYER,
            description="Handles deployment and DevOps tasks",
            capabilities=[
                "containerization",
                "ci_cd_pipeline",
                "cloud_deployment",
                "infrastructure_as_code",
                "monitoring_setup",
                "scaling_configuration",
                "security_hardening",
                "environment_management"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=6,  # Lower priority as deployment is typically final stage
            max_concurrent_tasks=3,
            timeout_seconds=900  # Longer timeout for deployment tasks
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Deployment platforms and configurations
        self.deployment_platforms = {
            "docker": {
                "files": ["Dockerfile", "docker-compose.yml", ".dockerignore"],
                "commands": ["docker build", "docker run", "docker-compose up"],
                "best_practices": ["Multi-stage builds", "Minimal base images", "Health checks"]
            },
            "kubernetes": {
                "files": ["deployment.yaml", "service.yaml", "ingress.yaml", "configmap.yaml"],
                "commands": ["kubectl apply", "kubectl rollout", "kubectl scale"],
                "best_practices": ["Resource limits", "Liveness probes", "Horizontal scaling"]
            },
            "aws": {
                "files": ["cloudformation.yaml", "terraform.tf", "serverless.yml"],
                "services": ["EC2", "ECS", "Lambda", "S3", "RDS", "CloudWatch"],
                "best_practices": ["IAM roles", "VPC security", "Auto-scaling"]
            },
            "heroku": {
                "files": ["Procfile", "requirements.txt", "runtime.txt"],
                "commands": ["git push heroku", "heroku ps:scale", "heroku logs"],
                "best_practices": ["12-factor app", "Environment variables", "Add-ons"]
            },
            "vercel": {
                "files": ["vercel.json", "package.json"],
                "commands": ["vercel deploy", "vercel promote"],
                "best_practices": ["Serverless functions", "Edge caching", "Environment variables"]
            },
            "github_actions": {
                "files": [".github/workflows/deploy.yml", ".github/workflows/ci.yml"],
                "triggers": ["push", "pull_request", "schedule"],
                "best_practices": ["Matrix builds", "Caching", "Secrets management"]
            }
        }
        
        # Environment types
        self.environment_types = {
            "development": {
                "characteristics": ["Debug mode", "Hot reload", "Local database"],
                "security": "Relaxed",
                "performance": "Not optimized"
            },
            "staging": {
                "characteristics": ["Production-like", "Testing environment", "Shared resources"],
                "security": "Medium",
                "performance": "Similar to production"
            },
            "production": {
                "characteristics": ["Optimized", "High availability", "Monitoring"],
                "security": "Strict",
                "performance": "Optimized"
            }
        }
        
        logger.info("🚀 Deployer Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for deployer agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires deployment
        deployment_keywords = [
            "deploy", "deployment", "devops", "docker", "kubernetes", "aws",
            "heroku", "vercel", "ci/cd", "pipeline", "containerize", "infrastructure"
        ]
        
        return any(keyword in content for keyword in deployment_keywords) or task_type == "deployment"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            platform = task.get("platform", "docker")
            environment = task.get("environment", "development")
            project_code = task.get("project_code", "")
            session_id = task.get("session_id")
            
            # Get project context
            context = await self.get_project_context(session_id)
            if not project_code and context.get("recent_code"):
                project_code = context["recent_code"]
            
            # Analyze deployment requirements
            deployment_analysis = self._analyze_deployment_requirements(
                user_request, platform, environment, project_code
            )
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Deployment task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "deployer",
                    "task_id": task.get("id"),
                    "platform": platform,
                    "environment": environment,
                    "deployment_type": deployment_analysis["type"]
                },
                session_id=session_id
            )
            
            # Create deployment prompt
            deployment_prompt = self._create_deployment_prompt(
                user_request, platform, environment, project_code, deployment_analysis, context
            )
            
            # Use orchestrator to generate deployment configuration
            orchestrator_request = TaskRequest(
                id=f"deployer_{task.get('id', 'unknown')}",
                content=deployment_prompt,
                task_type="code_generation",
                complexity=self._determine_complexity(platform, environment, project_code),
                required_capabilities=[
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.REASONING
                ],
                max_tokens=3500,
                temperature=0.2,  # Low temperature for consistent deployment configs
                priority=6,
                metadata={
                    "agent": "deployer",
                    "platform": platform,
                    "environment": environment,
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Deployment configuration generation failed: {response.error}")
            
            # Parse the deployment response
            deployment_config = self._parse_deployment_response(response.content, platform, environment)
            
            # Validate deployment configuration
            validated_config = await self._validate_deployment_config(
                deployment_config, platform, environment, project_code
            )
            
            # Store deployment configuration in memory
            deployment_memory_id = self.memory_manager.store_memory(
                content=f"Deployment configuration: {json.dumps(validated_config, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "deployer",
                    "task_id": task.get("id"),
                    "platform": platform,
                    "environment": environment,
                    "config_files": len(validated_config.get("files", [])),
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["deployment", platform, environment, "configuration"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "deployment_config": validated_config,
                "platform": platform,
                "environment": environment,
                "deployment_analysis": deployment_analysis,
                "memory_ids": [task_memory_id, deployment_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "deployer",
                "metadata": {
                    "deployment_ready": validated_config.get("ready", False),
                    "configuration_quality": "validated",
                    "deployment_type": deployment_analysis["type"]
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Deployer agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "deployer"
            }
    
    def _analyze_deployment_requirements(self, user_request: str, platform: str, 
                                       environment: str, project_code: str) -> Dict[str, Any]:
        """Analyze deployment requirements and determine configuration needs"""
        request_lower = user_request.lower()
        
        # Determine deployment type
        deployment_type = "simple"
        if any(word in request_lower for word in ["microservice", "distributed", "cluster"]):
            deployment_type = "microservice"
        elif any(word in request_lower for word in ["serverless", "lambda", "function"]):
            deployment_type = "serverless"
        elif any(word in request_lower for word in ["container", "docker", "kubernetes"]):
            deployment_type = "containerized"
        
        # Analyze project characteristics
        project_characteristics = []
        if project_code:
            code_lower = project_code.lower()
            if "database" in code_lower or "db" in code_lower:
                project_characteristics.append("database")
            if "api" in code_lower or "fastapi" in code_lower or "flask" in code_lower:
                project_characteristics.append("web_api")
            if "react" in code_lower or "vue" in code_lower or "angular" in code_lower:
                project_characteristics.append("frontend")
            if "redis" in code_lower or "cache" in code_lower:
                project_characteristics.append("caching")
            if "queue" in code_lower or "celery" in code_lower:
                project_characteristics.append("background_tasks")
        
        # Determine required services
        required_services = []
        if "database" in project_characteristics:
            required_services.append("database")
        if "caching" in project_characteristics:
            required_services.append("redis")
        if "background_tasks" in project_characteristics:
            required_services.append("worker_queue")
        
        # Calculate complexity
        complexity_score = len(project_characteristics) + len(required_services)
        if platform in ["kubernetes", "aws"]:
            complexity_score += 2
        if environment == "production":
            complexity_score += 1
        
        return {
            "type": deployment_type,
            "complexity_score": complexity_score,
            "project_characteristics": project_characteristics,
            "required_services": required_services,
            "platform_features": self.deployment_platforms.get(platform, {}),
            "environment_config": self.environment_types.get(environment, {})
        }
    
    def _create_deployment_prompt(self, user_request: str, platform: str, environment: str,
                                project_code: str, deployment_analysis: Dict[str, Any], 
                                context: Dict[str, Any]) -> str:
        """Create detailed deployment prompt"""
        platform_info = self.deployment_platforms.get(platform, {})
        environment_info = self.environment_types.get(environment, {})
        
        context_str = ""
        if context.get("architecture"):
            context_str = f"\n\nProject Architecture:\n{json.dumps(context['architecture'], indent=2)}"
        
        code_section = ""
        if project_code:
            code_section = f"\n\nProject Code (sample):\n```python\n{project_code[:1000]}\n```"
        
        required_files = platform_info.get("files", [])
        best_practices = platform_info.get("best_practices", [])
        
        return f"""
As an expert DevOps engineer, create a comprehensive deployment configuration for {platform} in {environment} environment.

Request: {user_request}

Deployment Analysis:
- Type: {deployment_analysis["type"]}
- Complexity: {deployment_analysis["complexity_score"]}/10
- Project Characteristics: {", ".join(deployment_analysis["project_characteristics"])}
- Required Services: {", ".join(deployment_analysis["required_services"])}

Platform: {platform}
Environment: {environment}
Environment Characteristics: {environment_info.get("characteristics", [])}
Security Level: {environment_info.get("security", "Standard")}

Required Files: {", ".join(required_files)}
Best Practices: {", ".join(best_practices)}{code_section}{context_str}

Please provide a complete deployment configuration including:

1. **CONFIGURATION FILES**
   - All necessary deployment files for {platform}
   - Environment-specific configurations
   - Security configurations
   - Resource limits and scaling rules

2. **DEPLOYMENT SCRIPTS**
   - Build scripts
   - Deployment commands
   - Rollback procedures
   - Health checks

3. **ENVIRONMENT SETUP**
   - Environment variables
   - Secret management
   - Database configuration
   - External service connections

4. **MONITORING & LOGGING**
   - Health monitoring setup
   - Log aggregation
   - Metrics collection
   - Alerting rules

5. **SECURITY CONFIGURATION**
   - Network security
   - Access controls
   - SSL/TLS setup
   - Secret management

6. **SCALING & PERFORMANCE**
   - Auto-scaling configuration
   - Load balancing
   - Performance optimization
   - Resource allocation

7. **DEPLOYMENT INSTRUCTIONS**
   - Step-by-step deployment guide
   - Prerequisites and dependencies
   - Troubleshooting tips
   - Rollback procedures

Format each configuration file as:
```filename
// filename: filename.ext
[file content]
```

Provide deployment commands as:
```bash
# Deployment commands
[commands here]
```

Ensure the configuration is:
- Production-ready for {environment} environment
- Secure and following best practices
- Scalable and maintainable
- Well-documented with clear instructions
- Optimized for {platform} platform
"""
    
    def _determine_complexity(self, platform: str, environment: str, project_code: str) -> TaskComplexity:
        """Determine deployment complexity"""
        complexity_factors = 0
        
        # Platform complexity
        platform_complexity = {
            "heroku": 1,
            "vercel": 1,
            "docker": 2,
            "github_actions": 2,
            "aws": 3,
            "kubernetes": 4
        }
        complexity_factors += platform_complexity.get(platform, 2)
        
        # Environment complexity
        if environment == "production":
            complexity_factors += 2
        elif environment == "staging":
            complexity_factors += 1
        
        # Project complexity
        if project_code:
            lines = len(project_code.split('\n'))
            if lines > 500:
                complexity_factors += 2
            elif lines > 200:
                complexity_factors += 1
            
            # Check for complex patterns
            if any(pattern in project_code.lower() for pattern in ["database", "redis", "queue", "microservice"]):
                complexity_factors += 1
        
        if complexity_factors >= 6:
            return TaskComplexity.EXPERT
        elif complexity_factors >= 4:
            return TaskComplexity.COMPLEX
        elif complexity_factors >= 2:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _parse_deployment_response(self, response_content: str, platform: str, environment: str) -> Dict[str, Any]:
        """Parse deployment response into structured configuration"""
        try:
            # Extract configuration files
            file_pattern = r'```(\w+)?\s*(?://\s*filename:\s*(.+?)\s*)?\n(.*?)```'
            file_matches = re.findall(file_pattern, response_content, re.DOTALL)
            
            config_files = []
            deployment_commands = []
            
            for file_type, filename, content in file_matches:
                if file_type == "bash" or "command" in filename.lower():
                    deployment_commands.append({
                        "type": "script",
                        "content": content.strip(),
                        "description": f"Deployment commands for {platform}"
                    })
                else:
                    if not filename.strip():
                        # Try to infer filename from content or platform
                        if platform == "docker" and "FROM" in content:
                            filename = "Dockerfile"
                        elif platform == "kubernetes" and "apiVersion" in content:
                            filename = "deployment.yaml"
                        else:
                            filename = f"config.{file_type or 'txt'}"
                    
                    config_files.append({
                        "filename": filename.strip(),
                        "content": content.strip(),
                        "type": file_type or "config"
                    })
            
            # Extract deployment instructions
            instructions = self._extract_deployment_instructions(response_content)
            
            # Extract security configurations
            security_config = self._extract_security_config(response_content)
            
            # Extract monitoring setup
            monitoring_config = self._extract_monitoring_config(response_content)
            
            return {
                "files": config_files,
                "deployment_commands": deployment_commands,
                "instructions": instructions,
                "security_config": security_config,
                "monitoring_config": monitoring_config,
                "platform": platform,
                "environment": environment,
                "timestamp": datetime.now().isoformat(),
                "ready": len(config_files) > 0
            }
            
        except Exception as e:
            logger.warning(f"⚠️  Deployment parsing failed: {e}")
            return {
                "files": [],
                "deployment_commands": [],
                "instructions": response_content,
                "platform": platform,
                "environment": environment,
                "ready": False,
                "parse_error": str(e)
            }
    
    def _extract_deployment_instructions(self, content: str) -> List[str]:
        """Extract deployment instructions from response"""
        instructions = []
        
        # Look for instruction sections
        patterns = [
            r'DEPLOYMENT INSTRUCTIONS[:\s]+(.*?)(?=\n\n|\*\*|$)',
            r'INSTRUCTIONS[:\s]+(.*?)(?=\n\n|\*\*|$)',
            r'STEPS[:\s]+(.*?)(?=\n\n|\*\*|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Split by bullet points or numbers
                steps = re.split(r'[•\-\*]|\d+\.', match)
                for step in steps:
                    step = step.strip()
                    if step and len(step) > 10:
                        instructions.append(step)
        
        return instructions[:10]  # Limit to top 10 instructions
    
    def _extract_security_config(self, content: str) -> Dict[str, Any]:
        """Extract security configuration from response"""
        security_config = {
            "ssl_enabled": "ssl" in content.lower() or "tls" in content.lower(),
            "secrets_management": "secret" in content.lower() or "env" in content.lower(),
            "access_control": "rbac" in content.lower() or "auth" in content.lower(),
            "network_security": "network" in content.lower() or "firewall" in content.lower()
        }
        return security_config
    
    def _extract_monitoring_config(self, content: str) -> Dict[str, Any]:
        """Extract monitoring configuration from response"""
        monitoring_config = {
            "health_checks": "health" in content.lower() or "probe" in content.lower(),
            "logging": "log" in content.lower() or "logging" in content.lower(),
            "metrics": "metric" in content.lower() or "prometheus" in content.lower(),
            "alerting": "alert" in content.lower() or "notification" in content.lower()
        }
        return monitoring_config
    
    async def _validate_deployment_config(self, config: Dict[str, Any], platform: str, 
                                        environment: str, project_code: str) -> Dict[str, Any]:
        """Validate deployment configuration"""
        try:
            validated_config = {
                **config,
                "validation_results": {},
                "ready": False,
                "issues": []
            }
            
            # Basic validation checks
            validation_checks = {
                "has_config_files": len(config.get("files", [])) > 0,
                "has_deployment_commands": len(config.get("deployment_commands", [])) > 0,
                "has_instructions": len(config.get("instructions", [])) > 0,
                "platform_specific": self._validate_platform_specific(config, platform),
                "environment_ready": self._validate_environment_ready(config, environment)
            }
            
            # Platform-specific validation
            if platform == "docker":
                validation_checks["has_dockerfile"] = any(
                    "dockerfile" in f.get("filename", "").lower() 
                    for f in config.get("files", [])
                )
            elif platform == "kubernetes":
                validation_checks["has_k8s_manifests"] = any(
                    f.get("filename", "").endswith(".yaml") 
                    for f in config.get("files", [])
                )
            
            # Calculate validation score
            passed_checks = sum(validation_checks.values())
            total_checks = len(validation_checks)
            
            validated_config["validation_results"] = validation_checks
            validated_config["ready"] = passed_checks >= (total_checks * 0.8)
            validated_config["validation_score"] = passed_checks / total_checks
            
            return validated_config
            
        except Exception as e:
            logger.warning(f"⚠️  Deployment validation failed: {e}")
            return {
                **config,
                "validation_error": str(e),
                "ready": False
            }
    
    def _validate_platform_specific(self, config: Dict[str, Any], platform: str) -> bool:
        """Validate platform-specific requirements"""
        platform_requirements = self.deployment_platforms.get(platform, {})
        required_files = platform_requirements.get("files", [])
        
        config_filenames = [f.get("filename", "").lower() for f in config.get("files", [])]
        
        # Check if at least one required file is present
        return any(req_file.lower() in " ".join(config_filenames) for req_file in required_files)
    
    def _validate_environment_ready(self, config: Dict[str, Any], environment: str) -> bool:
        """Validate environment readiness"""
        if environment == "production":
            # Production should have security and monitoring
            return (config.get("security_config", {}).get("ssl_enabled", False) and
                   config.get("monitoring_config", {}).get("health_checks", False))
        elif environment == "staging":
            # Staging should have monitoring
            return config.get("monitoring_config", {}).get("health_checks", False)
        else:
            # Development is less strict
            return True
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context for deployment"""
        try:
            # Get recent code
            code_items = self.memory_manager.search_memory(
                query="code generated",
                memory_type=MemoryType.CODE,
                use_vector=True,
                limit=3
            )
            
            # Get architecture information
            architecture_items = self.memory_manager.search_memory(
                query="architecture plan",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=2
            )
            
            # Get previous deployments
            deployment_items = self.memory_manager.search_memory(
                query="deployment",
                memory_type=MemoryType.CODE,
                use_vector=True,
                limit=3
            )
            
            context = {
                "recent_code": "",
                "architecture": {},
                "previous_deployments": [],
                "project_type": "web_application"
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
            
            # Extract previous deployments
            for item in deployment_items:
                if "platform" in item.metadata:
                    context["previous_deployments"].append({
                        "platform": item.metadata["platform"],
                        "environment": item.metadata.get("environment", "unknown"),
                        "timestamp": item.created_at.isoformat()
                    })
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get deployer agent statistics"""
        return {
            **self.stats,
            "supported_platforms": list(self.deployment_platforms.keys()),
            "supported_environments": list(self.environment_types.keys()),
            "deployments_created": len(self.memory_manager.search_memory(
                query="deployer",
                memory_type=MemoryType.CODE,
                limit=1000
            )),
            "deployment_capabilities": [
                "containerization",
                "ci_cd_pipeline_setup",
                "cloud_deployment",
                "infrastructure_as_code",
                "monitoring_configuration",
                "security_hardening"
            ]
        }


def create_deployer_agent(config: Dict[str, Any]) -> DeployerAgent:
    """Factory function to create deployer agent"""
    return DeployerAgent(config)