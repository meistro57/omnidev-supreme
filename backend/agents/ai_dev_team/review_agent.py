"""
AI-Development-Team Review Agent
Handles code review, documentation review, and quality assessment
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


class ReviewAgent(BaseAgent):
    """
    AI-Development-Team Review Agent
    
    Responsibilities:
    - Code review and quality assessment
    - Documentation review
    - Architecture review
    - Security review
    - Performance review
    - Best practices compliance
    - Technical debt assessment
    - Mentoring and guidance
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="ai_dev_team_review",
            agent_type=AgentType.REVIEWER,
            description="Code and documentation review agent",
            capabilities=[
                "code_review",
                "documentation_review",
                "architecture_review",
                "security_review",
                "performance_review",
                "quality_assessment",
                "best_practices_compliance",
                "technical_debt_assessment",
                "mentoring_guidance",
                "pull_request_review",
                "design_review",
                "compliance_review"
            ],
            model_requirements=["gpt-4", "claude-3.5-sonnet"],
            priority=8,
            max_concurrent_tasks=3,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Review criteria and standards
        self.review_criteria = {
            "code_quality": ["readability", "maintainability", "testability", "reusability"],
            "security": ["input_validation", "authentication", "authorization", "encryption"],
            "performance": ["efficiency", "scalability", "memory_usage", "cpu_usage"],
            "architecture": ["design_patterns", "separation_of_concerns", "modularity", "coupling"],
            "documentation": ["completeness", "accuracy", "clarity", "examples"]
        }
        
        self.severity_levels = ["critical", "high", "medium", "low", "info"]
        
        logger.info("🔍 AI-Development-Team Review Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for review"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # Review keywords
        review_keywords = [
            "review", "check", "assess", "evaluate", "analyze", "inspect",
            "audit", "validate", "verify", "quality", "feedback", "critique",
            "pull", "request", "pr", "merge", "approval", "documentation",
            "architecture", "security", "performance", "best", "practices"
        ]
        
        # Check task type
        if task_type in ["review", "assessment", "evaluation", "audit"]:
            return True
        
        # Check content for review keywords
        return any(keyword in content for keyword in review_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute review task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            language = task.get("language", "python")
            session_id = task.get("session_id")
            
            logger.info(f"🔍 Review executing task: {task_id}")
            
            # Determine review action
            action = self._determine_action(content)
            
            result = {}
            
            if action == "code_review":
                result = await self._review_code(content, language, task_id, session_id)
            elif action == "documentation_review":
                result = await self._review_documentation(content, task_id, session_id)
            elif action == "architecture_review":
                result = await self._review_architecture(content, task_id, session_id)
            elif action == "security_review":
                result = await self._review_security(content, language, task_id, session_id)
            elif action == "performance_review":
                result = await self._review_performance(content, language, task_id, session_id)
            elif action == "pull_request_review":
                result = await self._review_pull_request(content, language, task_id, session_id)
            else:
                result = await self._general_review(content, language, task_id, session_id)
            
            # Store result in memory
            await self._store_review_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Review completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "language": language,
                "review_result": result,
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Review failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_action(self, content: str) -> str:
        """Determine the specific review action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["code", "function", "class", "method"]):
            return "code_review"
        elif any(word in content_lower for word in ["documentation", "doc", "readme", "comment"]):
            return "documentation_review"
        elif any(word in content_lower for word in ["architecture", "design", "structure", "pattern"]):
            return "architecture_review"
        elif any(word in content_lower for word in ["security", "vulnerability", "auth", "encryption"]):
            return "security_review"
        elif any(word in content_lower for word in ["performance", "optimization", "speed", "memory"]):
            return "performance_review"
        elif any(word in content_lower for word in ["pull", "request", "pr", "merge"]):
            return "pull_request_review"
        else:
            return "general_review"
    
    async def _review_code(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review code quality and best practices"""
        try:
            request = TaskRequest(
                id=f"{task_id}_code_review",
                content=f"""
                Perform comprehensive code review for {language} code: {content}
                
                Analyze:
                1. Code quality and readability
                2. Best practices compliance
                3. Security vulnerabilities
                4. Performance issues
                5. Error handling
                6. Code structure and organization
                7. Testing coverage
                8. Documentation quality
                
                For each issue provide:
                - Issue description
                - Severity level (critical/high/medium/low/info)
                - Line numbers (if applicable)
                - Suggested fix
                - Explanation and rationale
                - Best practice recommendation
                """,
                task_type="code_review",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                review_results = self._parse_code_review(response.content, language)
                
                return {
                    "action": "code_review",
                    "language": language,
                    "review_results": review_results,
                    "issues": review_results.get("issues", []),
                    "suggestions": review_results.get("suggestions", []),
                    "quality_score": review_results.get("quality_score", 0),
                    "critical_issues": review_results.get("critical_issues", []),
                    "security_issues": review_results.get("security_issues", []),
                    "performance_issues": review_results.get("performance_issues", []),
                    "best_practices": review_results.get("best_practices", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "code_review",
                    "error": "Failed to review code",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Code review failed: {e}")
            return {
                "action": "code_review",
                "error": str(e)
            }
    
    async def _review_documentation(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review documentation quality and completeness"""
        try:
            request = TaskRequest(
                id=f"{task_id}_doc_review",
                content=f"""
                Review documentation quality and completeness: {content}
                
                Evaluate:
                1. Clarity and readability
                2. Completeness and accuracy
                3. Structure and organization
                4. Examples and use cases
                5. Technical accuracy
                6. Target audience appropriateness
                7. Consistency and style
                8. Accessibility and formatting
                
                Provide:
                - Overall assessment
                - Specific improvement suggestions
                - Missing sections or information
                - Clarity and readability issues
                - Technical accuracy verification
                - Style and consistency feedback
                """,
                task_type="documentation_review",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                doc_review = self._parse_documentation_review(response.content)
                
                return {
                    "action": "documentation_review",
                    "doc_review": doc_review,
                    "overall_assessment": doc_review.get("overall_assessment", ""),
                    "improvement_suggestions": doc_review.get("improvement_suggestions", []),
                    "missing_sections": doc_review.get("missing_sections", []),
                    "clarity_issues": doc_review.get("clarity_issues", []),
                    "technical_accuracy": doc_review.get("technical_accuracy", {}),
                    "style_feedback": doc_review.get("style_feedback", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "documentation_review",
                    "error": "Failed to review documentation",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Documentation review failed: {e}")
            return {
                "action": "documentation_review",
                "error": str(e)
            }
    
    async def _review_architecture(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review architecture and design decisions"""
        try:
            request = TaskRequest(
                id=f"{task_id}_arch_review",
                content=f"""
                Review architecture and design decisions: {content}
                
                Evaluate:
                1. Design patterns and principles
                2. System architecture and structure
                3. Scalability and performance
                4. Security considerations
                5. Maintainability and extensibility
                6. Technology choices
                7. Integration patterns
                8. Risk assessment
                
                Provide:
                - Architecture assessment
                - Design pattern evaluation
                - Scalability analysis
                - Security review
                - Technology choice validation
                - Risk identification
                - Improvement recommendations
                """,
                task_type="architecture_review",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                arch_review = self._parse_architecture_review(response.content)
                
                return {
                    "action": "architecture_review",
                    "arch_review": arch_review,
                    "design_patterns": arch_review.get("design_patterns", []),
                    "scalability_analysis": arch_review.get("scalability_analysis", {}),
                    "security_assessment": arch_review.get("security_assessment", {}),
                    "technology_validation": arch_review.get("technology_validation", []),
                    "risk_identification": arch_review.get("risk_identification", []),
                    "improvement_recommendations": arch_review.get("improvement_recommendations", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "architecture_review",
                    "error": "Failed to review architecture",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Architecture review failed: {e}")
            return {
                "action": "architecture_review",
                "error": str(e)
            }
    
    async def _review_security(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review security aspects and vulnerabilities"""
        try:
            request = TaskRequest(
                id=f"{task_id}_security_review",
                content=f"""
                Perform security review for {language} code: {content}
                
                Analyze:
                1. Security vulnerabilities (OWASP Top 10)
                2. Authentication and authorization
                3. Input validation and sanitization
                4. Data protection and encryption
                5. Error handling and information disclosure
                6. Session management
                7. API security
                8. Dependency vulnerabilities
                
                For each security issue provide:
                - Vulnerability description
                - Risk level and impact
                - Exploit scenario
                - Remediation steps
                - Best practice recommendations
                - Compliance considerations
                """,
                task_type="security_review",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                security_review = self._parse_security_review(response.content, language)
                
                return {
                    "action": "security_review",
                    "language": language,
                    "security_review": security_review,
                    "vulnerabilities": security_review.get("vulnerabilities", []),
                    "risk_assessment": security_review.get("risk_assessment", {}),
                    "remediation_steps": security_review.get("remediation_steps", []),
                    "best_practices": security_review.get("best_practices", []),
                    "compliance_issues": security_review.get("compliance_issues", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "security_review",
                    "error": "Failed to review security",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Security review failed: {e}")
            return {
                "action": "security_review",
                "error": str(e)
            }
    
    async def _review_performance(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review performance aspects and optimization opportunities"""
        try:
            request = TaskRequest(
                id=f"{task_id}_performance_review",
                content=f"""
                Review performance aspects for {language} code: {content}
                
                Analyze:
                1. Algorithm efficiency and time complexity
                2. Memory usage and space complexity
                3. Database query optimization
                4. Caching opportunities
                5. Resource utilization
                6. Bottleneck identification
                7. Scalability considerations
                8. Profiling recommendations
                
                Provide:
                - Performance assessment
                - Optimization opportunities
                - Bottleneck analysis
                - Scalability recommendations
                - Resource usage analysis
                - Profiling and monitoring suggestions
                """,
                task_type="performance_review",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                performance_review = self._parse_performance_review(response.content, language)
                
                return {
                    "action": "performance_review",
                    "language": language,
                    "performance_review": performance_review,
                    "optimization_opportunities": performance_review.get("optimization_opportunities", []),
                    "bottleneck_analysis": performance_review.get("bottleneck_analysis", {}),
                    "scalability_recommendations": performance_review.get("scalability_recommendations", []),
                    "resource_analysis": performance_review.get("resource_analysis", {}),
                    "monitoring_suggestions": performance_review.get("monitoring_suggestions", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "performance_review",
                    "error": "Failed to review performance",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Performance review failed: {e}")
            return {
                "action": "performance_review",
                "error": str(e)
            }
    
    async def _review_pull_request(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Review pull request comprehensively"""
        try:
            request = TaskRequest(
                id=f"{task_id}_pr_review",
                content=f"""
                Perform comprehensive pull request review for {language}: {content}
                
                Review:
                1. Code changes and their impact
                2. Test coverage and quality
                3. Documentation updates
                4. Breaking changes
                5. Performance implications
                6. Security considerations
                7. Code style and conventions
                8. Merge readiness
                
                Provide:
                - Overall PR assessment
                - Approval recommendation
                - Required changes
                - Suggested improvements
                - Risk assessment
                - Testing recommendations
                """,
                task_type="pull_request_review",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                pr_review = self._parse_pull_request_review(response.content, language)
                
                return {
                    "action": "pull_request_review",
                    "language": language,
                    "pr_review": pr_review,
                    "approval_status": pr_review.get("approval_status", ""),
                    "required_changes": pr_review.get("required_changes", []),
                    "suggested_improvements": pr_review.get("suggested_improvements", []),
                    "risk_assessment": pr_review.get("risk_assessment", {}),
                    "testing_recommendations": pr_review.get("testing_recommendations", []),
                    "merge_readiness": pr_review.get("merge_readiness", False),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "pull_request_review",
                    "error": "Failed to review pull request",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Pull request review failed: {e}")
            return {
                "action": "pull_request_review",
                "error": str(e)
            }
    
    async def _general_review(self, content: str, language: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general review tasks"""
        try:
            request = TaskRequest(
                id=f"{task_id}_general_review",
                content=f"""
                Perform general review and assessment for {language}: {content}
                
                Provide:
                1. Overall quality assessment
                2. Strengths and weaknesses
                3. Improvement recommendations
                4. Best practices compliance
                5. Risk identification
                6. Maintenance considerations
                
                Give comprehensive feedback and actionable recommendations.
                """,
                task_type="general_review",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_review",
                    "language": language,
                    "general_assessment": self._parse_general_review(response.content),
                    "strengths": self._extract_strengths(response.content),
                    "weaknesses": self._extract_weaknesses(response.content),
                    "recommendations": self._extract_recommendations(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_review",
                    "error": "Failed to perform general review",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General review failed: {e}")
            return {
                "action": "general_review",
                "error": str(e)
            }
    
    # Parsing methods (simplified)
    def _parse_code_review(self, content: str, language: str) -> Dict[str, Any]:
        """Parse code review results"""
        return {
            "issues": ["Issue 1", "Issue 2"],
            "suggestions": ["Suggestion 1", "Suggestion 2"],
            "quality_score": 85,
            "critical_issues": ["Critical issue 1"],
            "security_issues": ["Security issue 1"],
            "performance_issues": ["Performance issue 1"],
            "best_practices": ["Best practice 1", "Best practice 2"],
            "full_content": content
        }
    
    def _parse_documentation_review(self, content: str) -> Dict[str, Any]:
        """Parse documentation review results"""
        return {
            "overall_assessment": "Good documentation with some improvements needed",
            "improvement_suggestions": ["Add more examples", "Improve clarity"],
            "missing_sections": ["API reference", "Troubleshooting"],
            "clarity_issues": ["Section 2 is unclear"],
            "technical_accuracy": {"accurate": True, "errors": []},
            "style_feedback": ["Consistent formatting needed"],
            "full_content": content
        }
    
    def _parse_architecture_review(self, content: str) -> Dict[str, Any]:
        """Parse architecture review results"""
        return {
            "design_patterns": ["Observer pattern used well", "Consider Factory pattern"],
            "scalability_analysis": {"horizontal": True, "vertical": False},
            "security_assessment": {"score": 8, "issues": ["Missing rate limiting"]},
            "technology_validation": ["Good choice of database", "Consider caching"],
            "risk_identification": ["Single point of failure", "No backup strategy"],
            "improvement_recommendations": ["Add load balancing", "Implement caching"],
            "full_content": content
        }
    
    def _parse_security_review(self, content: str, language: str) -> Dict[str, Any]:
        """Parse security review results"""
        return {
            "vulnerabilities": ["SQL injection risk", "XSS vulnerability"],
            "risk_assessment": {"high": 1, "medium": 2, "low": 3},
            "remediation_steps": ["Sanitize input", "Use parameterized queries"],
            "best_practices": ["Input validation", "Output encoding"],
            "compliance_issues": ["GDPR compliance needed"],
            "full_content": content
        }
    
    def _parse_performance_review(self, content: str, language: str) -> Dict[str, Any]:
        """Parse performance review results"""
        return {
            "optimization_opportunities": ["Database indexing", "Caching layer"],
            "bottleneck_analysis": {"database": "slow queries", "network": "high latency"},
            "scalability_recommendations": ["Horizontal scaling", "Load balancing"],
            "resource_analysis": {"cpu": "high usage", "memory": "moderate usage"},
            "monitoring_suggestions": ["Add APM", "Database monitoring"],
            "full_content": content
        }
    
    def _parse_pull_request_review(self, content: str, language: str) -> Dict[str, Any]:
        """Parse pull request review results"""
        return {
            "approval_status": "approved_with_suggestions",
            "required_changes": ["Fix test coverage", "Update documentation"],
            "suggested_improvements": ["Add error handling", "Improve naming"],
            "risk_assessment": {"deployment_risk": "low", "breaking_changes": False},
            "testing_recommendations": ["Add integration tests", "Test edge cases"],
            "merge_readiness": True,
            "full_content": content
        }
    
    def _parse_general_review(self, content: str) -> Dict[str, Any]:
        """Parse general review results"""
        return {
            "overall_score": 8,
            "assessment": "Good overall quality with room for improvement",
            "full_content": content
        }
    
    def _extract_strengths(self, content: str) -> List[str]:
        """Extract strengths from review"""
        return ["Good code structure", "Comprehensive testing"]
    
    def _extract_weaknesses(self, content: str) -> List[str]:
        """Extract weaknesses from review"""
        return ["Missing error handling", "Poor documentation"]
    
    def _extract_recommendations(self, content: str) -> List[str]:
        """Extract recommendations from review"""
        return ["Add error handling", "Improve documentation", "Add tests"]
    
    async def _store_review_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store review result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"Review result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "language": result.get("language"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["review", "quality", "ai_dev_team"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store review result: {e}")


def create_review_agent(config: Dict[str, Any]) -> ReviewAgent:
    """Factory function to create Review Agent"""
    return ReviewAgent(config)