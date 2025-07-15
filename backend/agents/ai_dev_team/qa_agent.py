"""
AI-Development-Team QA Agent
Handles quality assurance, testing, and validation
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ..memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ..orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class QAAgent(BaseAgent):
    """
    AI-Development-Team QA Agent
    
    Responsibilities:
    - Test planning and strategy
    - Test case design and execution
    - Quality assurance processes
    - Bug detection and reporting
    - Performance testing
    - Security testing
    - User acceptance testing
    - Test automation
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="ai_dev_team_qa",
            agent_type=AgentType.TESTER,
            description="Quality assurance and testing agent",
            capabilities=[
                "test_planning",
                "test_case_design",
                "quality_assurance",
                "bug_detection",
                "performance_testing",
                "security_testing",
                "user_acceptance_testing",
                "test_automation",
                "regression_testing",
                "integration_testing",
                "load_testing",
                "usability_testing"
            ],
            model_requirements=["gpt-4", "claude-3.5-sonnet"],
            priority=8,
            max_concurrent_tasks=2,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Testing frameworks and tools
        self.testing_frameworks = {
            "unit": ["pytest", "unittest", "jest", "junit", "mocha"],
            "integration": ["testcontainers", "newman", "postman", "rest-assured"],
            "performance": ["locust", "jmeter", "k6", "artillery"],
            "security": ["owasp-zap", "bandit", "semgrep", "sonarqube"],
            "automation": ["selenium", "playwright", "cypress", "puppeteer"]
        }
        
        logger.info("🧪 AI-Development-Team QA Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for QA"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # QA keywords
        qa_keywords = [
            "test", "testing", "qa", "quality", "assurance", "bug", "defect",
            "validation", "verification", "automation", "regression", "integration",
            "performance", "security", "usability", "acceptance", "functional",
            "non-functional", "load", "stress", "scenario", "case", "coverage"
        ]
        
        # Check task type
        if task_type in ["testing", "qa", "quality", "validation"]:
            return True
        
        # Check content for QA keywords
        return any(keyword in content for keyword in qa_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute QA task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            session_id = task.get("session_id")
            
            logger.info(f"🧪 QA executing task: {task_id}")
            
            # Determine QA action
            action = self._determine_action(content)
            
            result = {}
            
            if action == "test_planning":
                result = await self._create_test_plan(content, task_id, session_id)
            elif action == "test_case_design":
                result = await self._design_test_cases(content, task_id, session_id)
            elif action == "bug_detection":
                result = await self._detect_bugs(content, task_id, session_id)
            elif action == "performance_testing":
                result = await self._performance_testing(content, task_id, session_id)
            elif action == "security_testing":
                result = await self._security_testing(content, task_id, session_id)
            elif action == "automation_testing":
                result = await self._automation_testing(content, task_id, session_id)
            else:
                result = await self._general_qa(content, task_id, session_id)
            
            # Store result in memory
            await self._store_qa_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ QA completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "qa_result": result,
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ QA failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_action(self, content: str) -> str:
        """Determine the specific QA action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["plan", "strategy", "approach"]):
            return "test_planning"
        elif any(word in content_lower for word in ["case", "scenario", "design"]):
            return "test_case_design"
        elif any(word in content_lower for word in ["bug", "defect", "issue", "error"]):
            return "bug_detection"
        elif any(word in content_lower for word in ["performance", "load", "stress", "benchmark"]):
            return "performance_testing"
        elif any(word in content_lower for word in ["security", "vulnerability", "penetration"]):
            return "security_testing"
        elif any(word in content_lower for word in ["automation", "automated", "script"]):
            return "automation_testing"
        else:
            return "general_qa"
    
    async def _create_test_plan(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Create comprehensive test plan"""
        try:
            request = TaskRequest(
                id=f"{task_id}_test_plan",
                content=f"""
                Create a comprehensive test plan for: {content}
                
                Include:
                1. Test objectives and scope
                2. Test strategy and approach
                3. Test types and levels
                4. Test environment requirements
                5. Test data requirements
                6. Test schedule and milestones
                7. Risk assessment and mitigation
                8. Entry and exit criteria
                9. Test deliverables
                10. Resource allocation
                
                Provide detailed testing strategy with specific test cases.
                """,
                task_type="test_planning",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                test_plan = self._parse_test_plan(response.content)
                
                return {
                    "action": "test_planning",
                    "test_plan": test_plan,
                    "test_objectives": test_plan.get("test_objectives", []),
                    "test_strategy": test_plan.get("test_strategy", {}),
                    "test_types": test_plan.get("test_types", []),
                    "test_schedule": test_plan.get("test_schedule", {}),
                    "risk_assessment": test_plan.get("risk_assessment", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "test_planning",
                    "error": "Failed to create test plan",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Test planning failed: {e}")
            return {
                "action": "test_planning",
                "error": str(e)
            }
    
    async def _design_test_cases(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Design detailed test cases"""
        try:
            request = TaskRequest(
                id=f"{task_id}_test_cases",
                content=f"""
                Design comprehensive test cases for: {content}
                
                Create:
                1. Functional test cases
                2. Non-functional test cases
                3. Edge cases and boundary conditions
                4. Negative test cases
                5. Integration test cases
                6. User acceptance test cases
                
                For each test case include:
                - Test case ID
                - Test description
                - Preconditions
                - Test steps
                - Expected results
                - Test data
                - Priority level
                """,
                task_type="test_case_design",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                test_cases = self._parse_test_cases(response.content)
                
                return {
                    "action": "test_case_design",
                    "test_cases": test_cases,
                    "functional_tests": test_cases.get("functional_tests", []),
                    "non_functional_tests": test_cases.get("non_functional_tests", []),
                    "edge_cases": test_cases.get("edge_cases", []),
                    "integration_tests": test_cases.get("integration_tests", []),
                    "total_test_cases": len(test_cases.get("all_tests", [])),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "test_case_design",
                    "error": "Failed to design test cases",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Test case design failed: {e}")
            return {
                "action": "test_case_design",
                "error": str(e)
            }
    
    async def _detect_bugs(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Detect and analyze bugs"""
        try:
            request = TaskRequest(
                id=f"{task_id}_bug_detection",
                content=f"""
                Analyze for bugs and issues: {content}
                
                Identify:
                1. Functional bugs and defects
                2. Performance issues
                3. Security vulnerabilities
                4. Usability problems
                5. Compatibility issues
                6. Error handling problems
                
                For each bug provide:
                - Bug description
                - Severity level
                - Steps to reproduce
                - Expected vs actual behavior
                - Impact assessment
                - Suggested fix
                """,
                task_type="bug_detection",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                bug_analysis = self._parse_bug_detection(response.content)
                
                return {
                    "action": "bug_detection",
                    "bug_analysis": bug_analysis,
                    "critical_bugs": bug_analysis.get("critical_bugs", []),
                    "high_priority_bugs": bug_analysis.get("high_priority_bugs", []),
                    "medium_priority_bugs": bug_analysis.get("medium_priority_bugs", []),
                    "total_bugs": bug_analysis.get("total_bugs", 0),
                    "suggested_fixes": bug_analysis.get("suggested_fixes", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "bug_detection",
                    "error": "Failed to detect bugs",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Bug detection failed: {e}")
            return {
                "action": "bug_detection",
                "error": str(e)
            }
    
    async def _performance_testing(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Create performance testing strategy"""
        try:
            request = TaskRequest(
                id=f"{task_id}_performance",
                content=f"""
                Create performance testing strategy for: {content}
                
                Include:
                1. Load testing scenarios
                2. Stress testing approaches
                3. Performance benchmarks
                4. Scalability testing
                5. Resource utilization monitoring
                6. Performance test automation
                
                Provide:
                - Test scenarios and scripts
                - Performance metrics to monitor
                - Expected performance thresholds
                - Load generation strategies
                - Monitoring and reporting setup
                """,
                task_type="performance_testing",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                performance_tests = self._parse_performance_testing(response.content)
                
                return {
                    "action": "performance_testing",
                    "performance_tests": performance_tests,
                    "load_tests": performance_tests.get("load_tests", []),
                    "stress_tests": performance_tests.get("stress_tests", []),
                    "benchmarks": performance_tests.get("benchmarks", {}),
                    "monitoring_setup": performance_tests.get("monitoring_setup", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "performance_testing",
                    "error": "Failed to create performance tests",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Performance testing failed: {e}")
            return {
                "action": "performance_testing",
                "error": str(e)
            }
    
    async def _security_testing(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Create security testing strategy"""
        try:
            request = TaskRequest(
                id=f"{task_id}_security",
                content=f"""
                Create security testing strategy for: {content}
                
                Include:
                1. Vulnerability assessment
                2. Penetration testing approach
                3. Security test cases
                4. Authentication and authorization testing
                5. Data protection testing
                6. API security testing
                
                Provide:
                - Security test scenarios
                - Vulnerability scanning approach
                - Security testing tools and techniques
                - Risk assessment and mitigation
                - Compliance testing requirements
                """,
                task_type="security_testing",
                complexity=TaskComplexity.EXPERT,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                security_tests = self._parse_security_testing(response.content)
                
                return {
                    "action": "security_testing",
                    "security_tests": security_tests,
                    "vulnerability_tests": security_tests.get("vulnerability_tests", []),
                    "penetration_tests": security_tests.get("penetration_tests", []),
                    "security_tools": security_tests.get("security_tools", []),
                    "risk_assessment": security_tests.get("risk_assessment", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "security_testing",
                    "error": "Failed to create security tests",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Security testing failed: {e}")
            return {
                "action": "security_testing",
                "error": str(e)
            }
    
    async def _automation_testing(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Create test automation strategy"""
        try:
            request = TaskRequest(
                id=f"{task_id}_automation",
                content=f"""
                Create test automation strategy for: {content}
                
                Include:
                1. Automation framework selection
                2. Automated test scripts
                3. CI/CD integration
                4. Test data management
                5. Reporting and monitoring
                6. Maintenance strategy
                
                Provide:
                - Test automation scripts
                - Framework configuration
                - CI/CD pipeline integration
                - Test execution scheduling
                - Result reporting setup
                """,
                task_type="automation_testing",
                complexity=TaskComplexity.COMPLEX,
                required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.REASONING],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                automation_tests = self._parse_automation_testing(response.content)
                
                return {
                    "action": "automation_testing",
                    "automation_tests": automation_tests,
                    "test_scripts": automation_tests.get("test_scripts", []),
                    "framework_config": automation_tests.get("framework_config", {}),
                    "ci_cd_integration": automation_tests.get("ci_cd_integration", {}),
                    "reporting_setup": automation_tests.get("reporting_setup", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "automation_testing",
                    "error": "Failed to create automation tests",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Automation testing failed: {e}")
            return {
                "action": "automation_testing",
                "error": str(e)
            }
    
    async def _general_qa(self, content: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general QA tasks"""
        try:
            request = TaskRequest(
                id=f"{task_id}_general_qa",
                content=f"""
                Provide comprehensive QA guidance for: {content}
                
                Include:
                1. Quality assurance best practices
                2. Testing recommendations
                3. Quality metrics and KPIs
                4. Process improvements
                5. Tool recommendations
                6. Quality gates and checkpoints
                
                Provide actionable QA recommendations.
                """,
                task_type="general_qa",
                complexity=TaskComplexity.MEDIUM,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=6
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_qa",
                    "qa_recommendations": self._parse_general_qa(response.content),
                    "best_practices": self._extract_best_practices(response.content),
                    "quality_metrics": self._extract_quality_metrics(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_qa",
                    "error": "Failed to provide QA guidance",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General QA failed: {e}")
            return {
                "action": "general_qa",
                "error": str(e)
            }
    
    # Parsing methods (simplified)
    def _parse_test_plan(self, content: str) -> Dict[str, Any]:
        """Parse test plan"""
        return {
            "test_objectives": ["Objective 1", "Objective 2"],
            "test_strategy": {"approach": "Risk-based testing"},
            "test_types": ["Unit", "Integration", "System"],
            "test_schedule": {"start": "2024-01-01", "end": "2024-03-01"},
            "risk_assessment": ["Risk 1", "Risk 2"],
            "full_content": content
        }
    
    def _parse_test_cases(self, content: str) -> Dict[str, Any]:
        """Parse test cases"""
        return {
            "functional_tests": ["Test case 1", "Test case 2"],
            "non_functional_tests": ["Performance test", "Security test"],
            "edge_cases": ["Edge case 1", "Edge case 2"],
            "integration_tests": ["Integration test 1", "Integration test 2"],
            "all_tests": ["Test 1", "Test 2", "Test 3", "Test 4"],
            "full_content": content
        }
    
    def _parse_bug_detection(self, content: str) -> Dict[str, Any]:
        """Parse bug detection"""
        return {
            "critical_bugs": ["Critical bug 1"],
            "high_priority_bugs": ["High bug 1", "High bug 2"],
            "medium_priority_bugs": ["Medium bug 1"],
            "total_bugs": 4,
            "suggested_fixes": ["Fix 1", "Fix 2"],
            "full_content": content
        }
    
    def _parse_performance_testing(self, content: str) -> Dict[str, Any]:
        """Parse performance testing"""
        return {
            "load_tests": ["Load test 1", "Load test 2"],
            "stress_tests": ["Stress test 1"],
            "benchmarks": {"response_time": "200ms", "throughput": "1000 req/s"},
            "monitoring_setup": {"tools": ["Prometheus", "Grafana"]},
            "full_content": content
        }
    
    def _parse_security_testing(self, content: str) -> Dict[str, Any]:
        """Parse security testing"""
        return {
            "vulnerability_tests": ["SQL injection test", "XSS test"],
            "penetration_tests": ["Network pen test", "Application pen test"],
            "security_tools": ["OWASP ZAP", "Nessus"],
            "risk_assessment": {"high_risk": 2, "medium_risk": 5},
            "full_content": content
        }
    
    def _parse_automation_testing(self, content: str) -> Dict[str, Any]:
        """Parse automation testing"""
        return {
            "test_scripts": ["Script 1", "Script 2"],
            "framework_config": {"framework": "Selenium", "language": "Python"},
            "ci_cd_integration": {"pipeline": "Jenkins", "triggers": "On commit"},
            "reporting_setup": {"tool": "Allure", "format": "HTML"},
            "full_content": content
        }
    
    def _parse_general_qa(self, content: str) -> List[str]:
        """Parse general QA recommendations"""
        return ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices"""
        return ["Best practice 1", "Best practice 2"]
    
    def _extract_quality_metrics(self, content: str) -> List[str]:
        """Extract quality metrics"""
        return ["Test coverage", "Defect density", "Pass rate"]
    
    async def _store_qa_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store QA result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"QA result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["qa", "testing", "ai_dev_team"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store QA result: {e}")


def create_qa_agent(config: Dict[str, Any]) -> QAAgent:
    """Factory function to create QA Agent"""
    return QAAgent(config)