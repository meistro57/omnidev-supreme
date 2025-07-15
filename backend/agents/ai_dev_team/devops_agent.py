"""
AI-Development-Team DevOps Agent
Handles infrastructure, deployment, and operations
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


class DevOpsAgent(BaseAgent):
    """
    AI-Development-Team DevOps Agent
    
    Responsibilities:
    - Infrastructure as Code (IaC)
    - CI/CD pipeline design and implementation
    - Container orchestration
    - Cloud platform management
    - Monitoring and alerting
    - Security and compliance
    - Automation and scripting
    - Performance optimization
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="ai_dev_team_devops",
            agent_type=AgentType.DEPLOYER,
            description="Infrastructure and deployment operations agent",
            capabilities=[
                "infrastructure_as_code",
                "ci_cd_pipeline",
                "container_orchestration",
                "cloud_management",
                "monitoring_alerting",
                "security_compliance",
                "automation_scripting",
                "performance_optimization",
                "disaster_recovery",
                "backup_restore",
                "scaling_management",
                "cost_optimization"
            ],
            model_requirements=["gpt-4", "claude-3.5-sonnet"],
            priority=8,
            max_concurrent_tasks=2,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # DevOps tools and platforms
        self.devops_tools = {
            "iac": ["terraform", "ansible", "cloudformation", "pulumi"],
            "ci_cd": ["jenkins", "github_actions", "gitlab_ci", "azure_devops"],
            "containers": ["docker", "kubernetes", "openshift", "nomad"],
            "cloud": ["aws", "azure", "gcp", "digitalocean"],
            "monitoring": ["prometheus", "grafana", "datadog", "newrelic"],
            "security": ["vault", "consul", "cert-manager", "falco"]
        }
        
        logger.info("🔧 AI-Development-Team DevOps Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for DevOps"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # DevOps keywords
        devops_keywords = [
            "deploy", "deployment", "infrastructure", "devops", "cicd", "pipeline",
            "docker", "kubernetes", "container", "cloud", "aws", "azure", "gcp",
            "terraform", "ansible", "jenkins", "monitoring", "alerting", "scaling",
            "automation", "orchestration", "provisioning", "configuration",
            "server", "service", "microservice", "cluster", "network", "security"
        ]
        
        # Check task type
        if task_type in ["deployment", "devops", "infrastructure", "cicd"]:
            return True
        
        # Check content for DevOps keywords
        return any(keyword in content for keyword in devops_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DevOps task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            platform = task.get("platform", "docker")
            session_id = task.get("session_id")
            
            logger.info(f"🔧 DevOps executing task: {task_id}")
            
            # Determine DevOps action
            action = self._determine_action(content)
            
            result = {}
            
            if action == "infrastructure_setup":
                result = await self._setup_infrastructure(content, platform, task_id, session_id)
            elif action == "ci_cd_pipeline":
                result = await self._setup_ci_cd(content, platform, task_id, session_id)
            elif action == "container_orchestration":
                result = await self._setup_containers(content, platform, task_id, session_id)
            elif action == "monitoring_setup":
                result = await self._setup_monitoring(content, platform, task_id, session_id)
            elif action == "security_setup":
                result = await self._setup_security(content, platform, task_id, session_id)
            elif action == "scaling_optimization":
                result = await self._optimize_scaling(content, platform, task_id, session_id)
            else:
                result = await self._general_devops(content, platform, task_id, session_id)
            
            # Store result in memory
            await self._store_devops_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ DevOps completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "platform": platform,
                "devops_result": result,
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ DevOps failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_action(self, content: str) -> str:
        """Determine the specific DevOps action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["infrastructure", "provision", "setup", "iac"]):
            return "infrastructure_setup"
        elif any(word in content_lower for word in ["ci", "cd", "pipeline", "build", "deploy"]):
            return "ci_cd_pipeline"
        elif any(word in content_lower for word in ["container", "docker", "kubernetes", "orchestration"]):
            return "container_orchestration"
        elif any(word in content_lower for word in ["monitor", "alert", "observability", "metrics"]):
            return "monitoring_setup"
        elif any(word in content_lower for word in ["security", "compliance", "vault", "certificate"]):
            return "security_setup"
        elif any(word in content_lower for word in ["scale", "scaling", "performance", "optimization"]):
            return "scaling_optimization"
        else:
            return "general_devops"
    
    async def _setup_infrastructure(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Set up infrastructure as code"""
        try:
            request = TaskRequest(
                id=f"{task_id}_infrastructure",
                content=f"""
                Create infrastructure as code for {platform}: {content}
                
                Provide:
                1. Infrastructure configuration files
                2. Resource definitions and specifications
                3. Network configuration
                4. Security groups and policies
                5. Storage configuration
                6. Monitoring and logging setup
                7. Backup and disaster recovery
                8. Cost optimization recommendations
                
                Include:
                - Terraform/CloudFormation templates
                - Configuration management scripts
                - Environment-specific configurations
                - Security best practices
                - Scalability considerations
                """,
                task_type="infrastructure_setup",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                infrastructure_config = self._parse_infrastructure_setup(response.content, platform)
                
                return {
                    "action": "infrastructure_setup",
                    "platform": platform,
                    "infrastructure_config": infrastructure_config,
                    "resource_definitions": infrastructure_config.get("resource_definitions", []),
                    "network_config": infrastructure_config.get("network_config", {}),
                    "security_policies": infrastructure_config.get("security_policies", []),
                    "monitoring_setup": infrastructure_config.get("monitoring_setup", {}),
                    "cost_optimization": infrastructure_config.get("cost_optimization", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "infrastructure_setup",
                    "error": "Failed to setup infrastructure",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Infrastructure setup failed: {e}")
            return {
                "action": "infrastructure_setup",
                "error": str(e)
            }
    
    async def _setup_ci_cd(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Set up CI/CD pipeline"""
        try:
            request = TaskRequest(
                id=f"{task_id}_ci_cd",
                content=f"""
                Create CI/CD pipeline for {platform}: {content}
                
                Provide:
                1. Pipeline configuration files
                2. Build and test stages
                3. Deployment strategies
                4. Environment management
                5. Security scanning integration
                6. Monitoring and notifications
                7. Rollback procedures
                8. Performance optimization
                
                Include:
                - Pipeline as code (YAML/JSON)
                - Build scripts and configurations
                - Testing automation
                - Deployment automation
                - Security best practices
                - Performance monitoring
                """,
                task_type="ci_cd_pipeline",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                ci_cd_config = self._parse_ci_cd_setup(response.content, platform)
                
                return {
                    "action": "ci_cd_pipeline",
                    "platform": platform,
                    "ci_cd_config": ci_cd_config,
                    "pipeline_stages": ci_cd_config.get("pipeline_stages", []),
                    "build_scripts": ci_cd_config.get("build_scripts", []),
                    "deployment_strategies": ci_cd_config.get("deployment_strategies", []),
                    "security_scanning": ci_cd_config.get("security_scanning", {}),
                    "monitoring_integration": ci_cd_config.get("monitoring_integration", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "ci_cd_pipeline",
                    "error": "Failed to setup CI/CD pipeline",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ CI/CD setup failed: {e}")
            return {
                "action": "ci_cd_pipeline",
                "error": str(e)
            }
    
    async def _setup_containers(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Set up container orchestration"""
        try:
            request = TaskRequest(
                id=f"{task_id}_containers",
                content=f"""
                Create container orchestration for {platform}: {content}
                
                Provide:
                1. Docker configuration files
                2. Kubernetes manifests
                3. Service mesh configuration
                4. Container security policies
                5. Resource management
                6. Networking configuration
                7. Storage management
                8. Monitoring and logging
                
                Include:
                - Dockerfile optimizations
                - Kubernetes deployments and services
                - ConfigMaps and Secrets
                - Ingress and load balancing
                - Auto-scaling configuration
                - Security best practices
                """,
                task_type="container_orchestration",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                container_config = self._parse_container_setup(response.content, platform)
                
                return {
                    "action": "container_orchestration",
                    "platform": platform,
                    "container_config": container_config,
                    "docker_files": container_config.get("docker_files", []),
                    "kubernetes_manifests": container_config.get("kubernetes_manifests", []),
                    "service_mesh": container_config.get("service_mesh", {}),
                    "security_policies": container_config.get("security_policies", []),
                    "auto_scaling": container_config.get("auto_scaling", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "container_orchestration",
                    "error": "Failed to setup containers",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Container setup failed: {e}")
            return {
                "action": "container_orchestration",
                "error": str(e)
            }
    
    async def _setup_monitoring(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Set up monitoring and alerting"""
        try:
            request = TaskRequest(
                id=f"{task_id}_monitoring",
                content=f"""
                Create monitoring and alerting setup for {platform}: {content}
                
                Provide:
                1. Monitoring configuration
                2. Alerting rules and thresholds
                3. Dashboard configurations
                4. Log aggregation setup
                5. Performance metrics
                6. Health checks
                7. Notification systems
                8. Incident response procedures
                
                Include:
                - Prometheus/Grafana configurations
                - Custom metrics and dashboards
                - Alert manager setup
                - Log shipping and analysis
                - SLA monitoring
                - Automated remediation
                """,
                task_type="monitoring_setup",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                monitoring_config = self._parse_monitoring_setup(response.content, platform)
                
                return {
                    "action": "monitoring_setup",
                    "platform": platform,
                    "monitoring_config": monitoring_config,
                    "alert_rules": monitoring_config.get("alert_rules", []),
                    "dashboards": monitoring_config.get("dashboards", []),
                    "log_aggregation": monitoring_config.get("log_aggregation", {}),
                    "health_checks": monitoring_config.get("health_checks", []),
                    "notification_systems": monitoring_config.get("notification_systems", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "monitoring_setup",
                    "error": "Failed to setup monitoring",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Monitoring setup failed: {e}")
            return {
                "action": "monitoring_setup",
                "error": str(e)
            }
    
    async def _setup_security(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Set up security and compliance"""
        try:
            request = TaskRequest(
                id=f"{task_id}_security",
                content=f"""
                Create security and compliance setup for {platform}: {content}
                
                Provide:
                1. Security policies and configurations
                2. Access control and authentication
                3. Network security setup
                4. Secrets management
                5. Compliance monitoring
                6. Security scanning integration
                7. Incident response procedures
                8. Audit logging
                
                Include:
                - Security group configurations
                - IAM policies and roles
                - Certificate management
                - Vulnerability scanning
                - Security monitoring
                - Compliance reporting
                """,
                task_type="security_setup",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                security_config = self._parse_security_setup(response.content, platform)
                
                return {
                    "action": "security_setup",
                    "platform": platform,
                    "security_config": security_config,
                    "access_controls": security_config.get("access_controls", []),
                    "network_security": security_config.get("network_security", {}),
                    "secrets_management": security_config.get("secrets_management", {}),
                    "compliance_monitoring": security_config.get("compliance_monitoring", []),
                    "security_scanning": security_config.get("security_scanning", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "security_setup",
                    "error": "Failed to setup security",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Security setup failed: {e}")
            return {
                "action": "security_setup",
                "error": str(e)
            }
    
    async def _optimize_scaling(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Optimize scaling and performance"""
        try:
            request = TaskRequest(
                id=f"{task_id}_scaling",
                content=f"""
                Create scaling and performance optimization for {platform}: {content}
                
                Provide:
                1. Auto-scaling configurations
                2. Load balancing setup
                3. Performance tuning
                4. Resource optimization
                5. Caching strategies
                6. Database scaling
                7. CDN configuration
                8. Cost optimization
                
                Include:
                - Horizontal and vertical scaling
                - Load balancer configurations
                - Performance monitoring
                - Resource allocation optimization
                - Cost analysis and optimization
                """,
                task_type="scaling_optimization",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                scaling_config = self._parse_scaling_optimization(response.content, platform)
                
                return {
                    "action": "scaling_optimization",
                    "platform": platform,
                    "scaling_config": scaling_config,
                    "auto_scaling": scaling_config.get("auto_scaling", {}),
                    "load_balancing": scaling_config.get("load_balancing", {}),
                    "performance_tuning": scaling_config.get("performance_tuning", []),
                    "resource_optimization": scaling_config.get("resource_optimization", []),
                    "cost_optimization": scaling_config.get("cost_optimization", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "scaling_optimization",
                    "error": "Failed to optimize scaling",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Scaling optimization failed: {e}")
            return {
                "action": "scaling_optimization",
                "error": str(e)
            }
    
    async def _general_devops(self, content: str, platform: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general DevOps tasks"""
        try:
            request = TaskRequest(
                id=f"{task_id}_general_devops",
                content=f"""
                Provide comprehensive DevOps guidance for {platform}: {content}
                
                Include:
                1. Best practices and recommendations
                2. Tool and platform suggestions
                3. Process optimization
                4. Automation opportunities
                5. Security considerations
                6. Performance improvements
                7. Cost optimization
                8. Maintenance procedures
                
                Provide actionable DevOps recommendations.
                """,
                task_type="general_devops",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_devops",
                    "platform": platform,
                    "devops_recommendations": self._parse_general_devops(response.content),
                    "best_practices": self._extract_best_practices(response.content),
                    "tool_suggestions": self._extract_tool_suggestions(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_devops",
                    "error": "Failed to provide DevOps guidance",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General DevOps failed: {e}")
            return {
                "action": "general_devops",
                "error": str(e)
            }
    
    # Parsing methods (simplified)
    def _parse_infrastructure_setup(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse infrastructure setup"""
        return {
            "resource_definitions": ["EC2 instances", "RDS database"],
            "network_config": {"vpc": "10.0.0.0/16", "subnets": ["10.0.1.0/24", "10.0.2.0/24"]},
            "security_policies": ["Security group rules", "IAM policies"],
            "monitoring_setup": {"cloudwatch": True, "alerts": True},
            "cost_optimization": ["Reserved instances", "Spot instances"],
            "full_content": content
        }
    
    def _parse_ci_cd_setup(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse CI/CD setup"""
        return {
            "pipeline_stages": ["Build", "Test", "Deploy"],
            "build_scripts": ["Build script", "Test script"],
            "deployment_strategies": ["Blue-green", "Rolling update"],
            "security_scanning": {"sast": True, "dast": True},
            "monitoring_integration": {"prometheus": True, "grafana": True},
            "full_content": content
        }
    
    def _parse_container_setup(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse container setup"""
        return {
            "docker_files": ["App Dockerfile", "Nginx Dockerfile"],
            "kubernetes_manifests": ["Deployment", "Service", "Ingress"],
            "service_mesh": {"istio": True, "linkerd": False},
            "security_policies": ["Network policies", "Pod security policies"],
            "auto_scaling": {"hpa": True, "vpa": True},
            "full_content": content
        }
    
    def _parse_monitoring_setup(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse monitoring setup"""
        return {
            "alert_rules": ["High CPU", "Memory usage", "Error rate"],
            "dashboards": ["Application dashboard", "Infrastructure dashboard"],
            "log_aggregation": {"fluentd": True, "elasticsearch": True},
            "health_checks": ["Liveness probe", "Readiness probe"],
            "notification_systems": ["Slack", "PagerDuty"],
            "full_content": content
        }
    
    def _parse_security_setup(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse security setup"""
        return {
            "access_controls": ["RBAC", "IAM roles"],
            "network_security": {"firewall": True, "vpn": True},
            "secrets_management": {"vault": True, "kms": True},
            "compliance_monitoring": ["CIS benchmarks", "GDPR compliance"],
            "security_scanning": {"clair": True, "trivy": True},
            "full_content": content
        }
    
    def _parse_scaling_optimization(self, content: str, platform: str) -> Dict[str, Any]:
        """Parse scaling optimization"""
        return {
            "auto_scaling": {"min": 2, "max": 10, "target_cpu": 70},
            "load_balancing": {"alb": True, "nlb": False},
            "performance_tuning": ["JVM tuning", "Database optimization"],
            "resource_optimization": ["Memory limits", "CPU requests"],
            "cost_optimization": ["Reserved instances", "Spot instances"],
            "full_content": content
        }
    
    def _parse_general_devops(self, content: str) -> List[str]:
        """Parse general DevOps recommendations"""
        return ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices"""
        return ["Best practice 1", "Best practice 2"]
    
    def _extract_tool_suggestions(self, content: str) -> List[str]:
        """Extract tool suggestions"""
        return ["Tool 1", "Tool 2", "Tool 3"]
    
    async def _store_devops_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store DevOps result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"DevOps result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "platform": result.get("platform"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["devops", "deployment", "ai_dev_team"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store DevOps result: {e}")


def create_devops_agent(config: Dict[str, Any]) -> DevOpsAgent:
    """Factory function to create DevOps Agent"""
    return DevOpsAgent(config)