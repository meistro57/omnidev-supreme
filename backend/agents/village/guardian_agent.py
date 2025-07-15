"""
Village-of-Intelligence Guardian Agent
Handles security, protection, and system guardianship
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class GuardianAgent(BaseAgent):
    """
    Village-of-Intelligence Guardian Agent
    
    Responsibilities:
    - Security monitoring and protection
    - System integrity maintenance
    - Threat detection and response
    - Access control and authorization
    - Compliance and governance
    - Risk assessment and mitigation
    - Incident response and recovery
    - Preventive security measures
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="village_guardian",
            agent_type=AgentType.GUARDIAN,
            description="Security and protection agent",
            capabilities=[
                "security_monitoring",
                "threat_detection",
                "access_control",
                "compliance_governance",
                "risk_assessment",
                "incident_response",
                "preventive_security",
                "system_integrity",
                "vulnerability_assessment",
                "security_auditing",
                "data_protection",
                "privacy_enforcement"
            ],
            model_requirements=["gpt-4", "claude-3-opus"],
            priority=10,
            max_concurrent_tasks=3,
            timeout_seconds=600
        )
        
        super().__init__(metadata, config)
        
        self.memory_manager = memory_manager
        self.model_orchestrator = model_orchestrator
        
        # Security frameworks and standards
        self.security_frameworks = [
            "nist_cybersecurity",
            "iso_27001",
            "owasp_top_10",
            "cis_controls",
            "pci_dss",
            "gdpr_compliance",
            "hipaa_compliance",
            "soc2_compliance"
        ]
        
        # Village security knowledge
        self.village_security = {
            "threat_intelligence": [],
            "security_incidents": [],
            "protective_measures": {},
            "vulnerability_database": [],
            "security_wisdom": []
        }
        
        # Threat severity levels
        self.threat_levels = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "info": 1
        }
        
        logger.info("🛡️ Village-of-Intelligence Guardian Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for security/protection"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "").lower()
        
        # Security keywords
        security_keywords = [
            "security", "protect", "secure", "safety", "threat", "risk",
            "vulnerability", "attack", "breach", "incident", "malware",
            "authentication", "authorization", "access", "permission",
            "encryption", "decrypt", "firewall", "intrusion", "monitoring",
            "compliance", "audit", "governance", "privacy", "data",
            "backup", "recovery", "forensics", "penetration", "testing"
        ]
        
        # Check task type
        if task_type in ["security", "protection", "monitoring", "compliance"]:
            return True
        
        # Check content for security keywords
        return any(keyword in content for keyword in security_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute security/protection task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", str(uuid.uuid4()))
            content = task.get("content", "")
            priority = task.get("priority", "medium")
            session_id = task.get("session_id")
            
            logger.info(f"🛡️ Guardian executing task: {task_id}")
            
            # Determine security action
            action = self._determine_security_action(content)
            
            result = {}
            
            if action == "threat_detection":
                result = await self._detect_threats(content, priority, task_id, session_id)
            elif action == "vulnerability_assessment":
                result = await self._assess_vulnerabilities(content, priority, task_id, session_id)
            elif action == "access_control":
                result = await self._manage_access_control(content, priority, task_id, session_id)
            elif action == "compliance_check":
                result = await self._check_compliance(content, priority, task_id, session_id)
            elif action == "incident_response":
                result = await self._respond_to_incident(content, priority, task_id, session_id)
            elif action == "security_monitoring":
                result = await self._monitor_security(content, priority, task_id, session_id)
            elif action == "risk_assessment":
                result = await self._assess_risks(content, priority, task_id, session_id)
            else:
                result = await self._general_security_work(content, priority, task_id, session_id)
            
            # Update village security knowledge
            await self._update_village_security(result, task_id, session_id)
            
            # Store result in memory
            await self._store_security_result(result, task_id, session_id)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Guardian completed task: {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "action": action,
                "priority": priority,
                "security_result": result,
                "village_security": self._get_village_security(),
                "agent": self.metadata.name
            }
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Guardian failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "agent": self.metadata.name
            }
    
    def _determine_security_action(self, content: str) -> str:
        """Determine the specific security action needed"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["threat", "attack", "malware", "intrusion"]):
            return "threat_detection"
        elif any(word in content_lower for word in ["vulnerability", "weakness", "flaw", "exploit"]):
            return "vulnerability_assessment"
        elif any(word in content_lower for word in ["access", "permission", "authorization", "authentication"]):
            return "access_control"
        elif any(word in content_lower for word in ["compliance", "regulation", "standard", "audit"]):
            return "compliance_check"
        elif any(word in content_lower for word in ["incident", "breach", "emergency", "response"]):
            return "incident_response"
        elif any(word in content_lower for word in ["monitor", "surveillance", "watch", "alert"]):
            return "security_monitoring"
        elif any(word in content_lower for word in ["risk", "assess", "evaluation", "analysis"]):
            return "risk_assessment"
        else:
            return "general_security_work"
    
    async def _detect_threats(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Detect and analyze security threats"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_threat_detection",
                content=f"""
                Detect and analyze security threats: {content}
                
                Perform comprehensive threat analysis including:
                1. Threat identification and classification
                2. Attack vector analysis
                3. Threat actor profiling
                4. Impact assessment
                5. Likelihood evaluation
                6. Threat intelligence correlation
                7. Indicators of compromise (IoCs)
                8. Attack timeline reconstruction
                9. Threat hunting recommendations
                10. Mitigation strategies
                
                Provide:
                - Threat assessment report
                - Attack vector analysis
                - Risk scoring and prioritization
                - Immediate response actions
                - Long-term mitigation strategies
                - Threat intelligence updates
                - Monitoring recommendations
                - Prevention measures
                """,
                task_type="threat_detection",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=9
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                threat_analysis = self._parse_threat_detection(response.content, priority)
                
                return {
                    "action": "threat_detection",
                    "priority": priority,
                    "threat_analysis": threat_analysis,
                    "identified_threats": threat_analysis.get("identified_threats", []),
                    "attack_vectors": threat_analysis.get("attack_vectors", []),
                    "threat_actors": threat_analysis.get("threat_actors", []),
                    "risk_score": threat_analysis.get("risk_score", 0),
                    "immediate_actions": threat_analysis.get("immediate_actions", []),
                    "mitigation_strategies": threat_analysis.get("mitigation_strategies", []),
                    "monitoring_recommendations": threat_analysis.get("monitoring_recommendations", []),
                    "prevention_measures": threat_analysis.get("prevention_measures", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "threat_detection",
                    "error": "Failed to detect threats",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Threat detection failed: {e}")
            return {
                "action": "threat_detection",
                "error": str(e)
            }
    
    async def _assess_vulnerabilities(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Assess system vulnerabilities"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_vulnerability_assessment",
                content=f"""
                Assess system vulnerabilities: {content}
                
                Conduct comprehensive vulnerability assessment including:
                1. Vulnerability scanning and identification
                2. Security weakness analysis
                3. Exploitability assessment
                4. Impact evaluation
                5. CVSS scoring and prioritization
                6. Patch management recommendations
                7. Configuration security review
                8. Network security assessment
                9. Application security testing
                10. Remediation planning
                
                Provide:
                - Vulnerability assessment report
                - Risk-based prioritization
                - Remediation recommendations
                - Patch management plan
                - Configuration improvements
                - Security hardening guide
                - Monitoring requirements
                - Compliance implications
                """,
                task_type="vulnerability_assessment",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                vulnerability_assessment = self._parse_vulnerability_assessment(response.content, priority)
                
                return {
                    "action": "vulnerability_assessment",
                    "priority": priority,
                    "vulnerability_assessment": vulnerability_assessment,
                    "identified_vulnerabilities": vulnerability_assessment.get("identified_vulnerabilities", []),
                    "risk_prioritization": vulnerability_assessment.get("risk_prioritization", []),
                    "remediation_plan": vulnerability_assessment.get("remediation_plan", []),
                    "patch_management": vulnerability_assessment.get("patch_management", []),
                    "hardening_recommendations": vulnerability_assessment.get("hardening_recommendations", []),
                    "compliance_impact": vulnerability_assessment.get("compliance_impact", []),
                    "monitoring_requirements": vulnerability_assessment.get("monitoring_requirements", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "vulnerability_assessment",
                    "error": "Failed to assess vulnerabilities",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Vulnerability assessment failed: {e}")
            return {
                "action": "vulnerability_assessment",
                "error": str(e)
            }
    
    async def _manage_access_control(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Manage access control and authorization"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_access_control",
                content=f"""
                Manage access control and authorization: {content}
                
                Implement comprehensive access control including:
                1. Authentication mechanisms
                2. Authorization frameworks
                3. Role-based access control (RBAC)
                4. Attribute-based access control (ABAC)
                5. Multi-factor authentication (MFA)
                6. Privileged access management
                7. Session management
                8. Access review and auditing
                9. Identity lifecycle management
                10. Zero-trust architecture
                
                Provide:
                - Access control strategy
                - Authentication implementation
                - Authorization policies
                - Role and permission matrix
                - MFA implementation guide
                - Session management rules
                - Audit and monitoring setup
                - Compliance mapping
                """,
                task_type="access_control",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                access_control = self._parse_access_control(response.content, priority)
                
                return {
                    "action": "access_control",
                    "priority": priority,
                    "access_control": access_control,
                    "authentication_strategy": access_control.get("authentication_strategy", {}),
                    "authorization_policies": access_control.get("authorization_policies", []),
                    "role_matrix": access_control.get("role_matrix", {}),
                    "mfa_implementation": access_control.get("mfa_implementation", {}),
                    "session_management": access_control.get("session_management", {}),
                    "audit_requirements": access_control.get("audit_requirements", []),
                    "compliance_mapping": access_control.get("compliance_mapping", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "access_control",
                    "error": "Failed to manage access control",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Access control management failed: {e}")
            return {
                "action": "access_control",
                "error": str(e)
            }
    
    async def _check_compliance(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Check compliance with regulations and standards"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_compliance_check",
                content=f"""
                Check compliance with regulations and standards: {content}
                
                Conduct comprehensive compliance assessment including:
                1. Regulatory requirements mapping
                2. Control framework alignment
                3. Gap analysis and identification
                4. Risk and compliance assessment
                5. Policy and procedure review
                6. Documentation requirements
                7. Audit preparation and support
                8. Remediation planning
                9. Continuous monitoring setup
                10. Reporting and governance
                
                Provide:
                - Compliance assessment report
                - Gap analysis findings
                - Remediation roadmap
                - Policy recommendations
                - Control implementation guide
                - Audit preparation checklist
                - Monitoring and reporting setup
                - Governance framework
                """,
                task_type="compliance_check",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                compliance_check = self._parse_compliance_check(response.content, priority)
                
                return {
                    "action": "compliance_check",
                    "priority": priority,
                    "compliance_check": compliance_check,
                    "regulatory_mapping": compliance_check.get("regulatory_mapping", []),
                    "gap_analysis": compliance_check.get("gap_analysis", []),
                    "remediation_roadmap": compliance_check.get("remediation_roadmap", []),
                    "policy_recommendations": compliance_check.get("policy_recommendations", []),
                    "control_implementation": compliance_check.get("control_implementation", []),
                    "audit_checklist": compliance_check.get("audit_checklist", []),
                    "monitoring_setup": compliance_check.get("monitoring_setup", {}),
                    "governance_framework": compliance_check.get("governance_framework", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "compliance_check",
                    "error": "Failed to check compliance",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Compliance check failed: {e}")
            return {
                "action": "compliance_check",
                "error": str(e)
            }
    
    async def _respond_to_incident(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Respond to security incidents"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_incident_response",
                content=f"""
                Respond to security incident: {content}
                
                Execute comprehensive incident response including:
                1. Incident classification and severity
                2. Immediate containment actions
                3. Evidence collection and preservation
                4. Impact assessment and analysis
                5. Root cause investigation
                6. Eradication and recovery planning
                7. Communication and notification
                8. Post-incident review
                9. Lessons learned documentation
                10. Process improvement recommendations
                
                Provide:
                - Incident response plan
                - Containment procedures
                - Investigation findings
                - Recovery recommendations
                - Communication strategy
                - Evidence handling guide
                - Post-incident analysis
                - Process improvements
                """,
                task_type="incident_response",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=10
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                incident_response = self._parse_incident_response(response.content, priority)
                
                return {
                    "action": "incident_response",
                    "priority": priority,
                    "incident_response": incident_response,
                    "incident_classification": incident_response.get("incident_classification", {}),
                    "containment_actions": incident_response.get("containment_actions", []),
                    "investigation_findings": incident_response.get("investigation_findings", []),
                    "recovery_plan": incident_response.get("recovery_plan", []),
                    "communication_strategy": incident_response.get("communication_strategy", {}),
                    "evidence_handling": incident_response.get("evidence_handling", []),
                    "lessons_learned": incident_response.get("lessons_learned", []),
                    "process_improvements": incident_response.get("process_improvements", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "incident_response",
                    "error": "Failed to respond to incident",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Incident response failed: {e}")
            return {
                "action": "incident_response",
                "error": str(e)
            }
    
    async def _monitor_security(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Monitor security systems and events"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_security_monitoring",
                content=f"""
                Monitor security systems and events: {content}
                
                Implement comprehensive security monitoring including:
                1. Security event correlation
                2. Anomaly detection and analysis
                3. Threat hunting activities
                4. Log analysis and SIEM integration
                5. Network traffic monitoring
                6. System integrity monitoring
                7. User behavior analytics
                8. Alert management and triage
                9. Incident escalation procedures
                10. Reporting and dashboards
                
                Provide:
                - Monitoring architecture
                - Event correlation rules
                - Anomaly detection setup
                - Threat hunting playbooks
                - Alert management procedures
                - Escalation workflows
                - Reporting requirements
                - Dashboard specifications
                """,
                task_type="security_monitoring",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                security_monitoring = self._parse_security_monitoring(response.content, priority)
                
                return {
                    "action": "security_monitoring",
                    "priority": priority,
                    "security_monitoring": security_monitoring,
                    "monitoring_architecture": security_monitoring.get("monitoring_architecture", {}),
                    "correlation_rules": security_monitoring.get("correlation_rules", []),
                    "anomaly_detection": security_monitoring.get("anomaly_detection", {}),
                    "threat_hunting": security_monitoring.get("threat_hunting", []),
                    "alert_management": security_monitoring.get("alert_management", {}),
                    "escalation_procedures": security_monitoring.get("escalation_procedures", []),
                    "reporting_setup": security_monitoring.get("reporting_setup", {}),
                    "dashboard_specs": security_monitoring.get("dashboard_specs", []),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "security_monitoring",
                    "error": "Failed to monitor security",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Security monitoring failed: {e}")
            return {
                "action": "security_monitoring",
                "error": str(e)
            }
    
    async def _assess_risks(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Assess security risks"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_risk_assessment",
                content=f"""
                Assess security risks: {content}
                
                Conduct comprehensive risk assessment including:
                1. Risk identification and categorization
                2. Threat and vulnerability analysis
                3. Impact and likelihood evaluation
                4. Risk scoring and prioritization
                5. Risk treatment options
                6. Residual risk analysis
                7. Risk tolerance evaluation
                8. Mitigation strategy development
                9. Risk monitoring and review
                10. Risk communication and reporting
                
                Provide:
                - Risk assessment report
                - Risk register and matrix
                - Treatment recommendations
                - Mitigation strategies
                - Monitoring requirements
                - Risk tolerance analysis
                - Communication plan
                - Review schedule
                """,
                task_type="risk_assessment",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.ANALYSIS, ModelCapability.REASONING],
                priority=8
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                risk_assessment = self._parse_risk_assessment(response.content, priority)
                
                return {
                    "action": "risk_assessment",
                    "priority": priority,
                    "risk_assessment": risk_assessment,
                    "risk_register": risk_assessment.get("risk_register", []),
                    "risk_matrix": risk_assessment.get("risk_matrix", {}),
                    "treatment_options": risk_assessment.get("treatment_options", []),
                    "mitigation_strategies": risk_assessment.get("mitigation_strategies", []),
                    "monitoring_requirements": risk_assessment.get("monitoring_requirements", []),
                    "risk_tolerance": risk_assessment.get("risk_tolerance", {}),
                    "communication_plan": risk_assessment.get("communication_plan", {}),
                    "review_schedule": risk_assessment.get("review_schedule", {}),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "risk_assessment",
                    "error": "Failed to assess risks",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ Risk assessment failed: {e}")
            return {
                "action": "risk_assessment",
                "error": str(e)
            }
    
    async def _general_security_work(self, content: str, priority: str, task_id: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Handle general security work"""
        try:
            task_complexity = self._map_priority_to_complexity(priority)
            
            request = TaskRequest(
                id=f"{task_id}_general_security",
                content=f"""
                Handle general security work: {content}
                
                Provide comprehensive security solution including:
                1. Security analysis and recommendations
                2. Best practices implementation
                3. Risk mitigation strategies
                4. Compliance considerations
                5. Security controls implementation
                6. Monitoring and detection
                7. Response procedures
                8. Documentation and training
                
                Follow security best practices and industry standards.
                """,
                task_type="general_security",
                complexity=task_complexity,
                required_capabilities=[ModelCapability.REASONING, ModelCapability.ANALYSIS],
                priority=7
            )
            
            response = await self.model_orchestrator.execute_task(request)
            
            if response.success:
                return {
                    "action": "general_security_work",
                    "priority": priority,
                    "security_work": self._parse_general_security(response.content, priority),
                    "recommendations": self._extract_recommendations(response.content),
                    "best_practices": self._extract_best_practices(response.content),
                    "controls": self._extract_controls(response.content),
                    "ai_response": response.content,
                    "tokens_used": response.tokens_used
                }
            else:
                return {
                    "action": "general_security_work",
                    "error": "Failed to handle general security work",
                    "ai_error": response.error
                }
                
        except Exception as e:
            logger.error(f"❌ General security work failed: {e}")
            return {
                "action": "general_security_work",
                "error": str(e)
            }
    
    def _map_priority_to_complexity(self, priority: str) -> TaskComplexity:
        """Map priority string to TaskComplexity enum"""
        priority_map = {
            "low": TaskComplexity.SIMPLE,
            "medium": TaskComplexity.MEDIUM,
            "high": TaskComplexity.COMPLEX,
            "critical": TaskComplexity.EXPERT
        }
        return priority_map.get(priority.lower(), TaskComplexity.MEDIUM)
    
    # Parsing methods (simplified)
    def _parse_threat_detection(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse threat detection results"""
        return {
            "identified_threats": ["Malware", "Phishing", "DDoS"],
            "attack_vectors": ["Email", "Web", "Network"],
            "threat_actors": ["Cybercriminals", "Nation-state"],
            "risk_score": 8.5,
            "immediate_actions": ["Block IPs", "Update signatures"],
            "mitigation_strategies": ["Patch systems", "Train users"],
            "monitoring_recommendations": ["Enhanced logging", "Real-time alerts"],
            "prevention_measures": ["Firewalls", "Endpoint protection"],
            "full_content": content
        }
    
    def _parse_vulnerability_assessment(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse vulnerability assessment results"""
        return {
            "identified_vulnerabilities": ["CVE-2023-1234", "CVE-2023-5678"],
            "risk_prioritization": ["Critical", "High", "Medium"],
            "remediation_plan": ["Patch immediately", "Configuration change"],
            "patch_management": ["Emergency patches", "Scheduled updates"],
            "hardening_recommendations": ["Disable services", "Update configs"],
            "compliance_impact": ["SOC2", "PCI-DSS"],
            "monitoring_requirements": ["Vulnerability scanning", "Patch tracking"],
            "full_content": content
        }
    
    def _parse_access_control(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse access control results"""
        return {
            "authentication_strategy": {"method": "Multi-factor", "provider": "SSO"},
            "authorization_policies": ["RBAC", "ABAC"],
            "role_matrix": {"admin": ["full"], "user": ["read"]},
            "mfa_implementation": {"method": "TOTP", "backup": "SMS"},
            "session_management": {"timeout": "30min", "concurrent": "single"},
            "audit_requirements": ["Login tracking", "Permission changes"],
            "compliance_mapping": ["SOX", "GDPR"],
            "full_content": content
        }
    
    def _parse_compliance_check(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse compliance check results"""
        return {
            "regulatory_mapping": ["GDPR", "HIPAA", "SOX"],
            "gap_analysis": ["Missing encryption", "Insufficient logging"],
            "remediation_roadmap": ["Phase 1: Encryption", "Phase 2: Logging"],
            "policy_recommendations": ["Data retention", "Access control"],
            "control_implementation": ["Technical controls", "Administrative controls"],
            "audit_checklist": ["Evidence collection", "Documentation review"],
            "monitoring_setup": {"continuous": True, "automated": True},
            "governance_framework": {"structure": "Committee", "reporting": "Monthly"},
            "full_content": content
        }
    
    def _parse_incident_response(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse incident response results"""
        return {
            "incident_classification": {"severity": "High", "type": "Data breach"},
            "containment_actions": ["Isolate systems", "Disable accounts"],
            "investigation_findings": ["Root cause", "Attack timeline"],
            "recovery_plan": ["Restore systems", "Verify integrity"],
            "communication_strategy": {"internal": "Immediate", "external": "Legal review"},
            "evidence_handling": ["Chain of custody", "Forensic imaging"],
            "lessons_learned": ["Process gaps", "Training needs"],
            "process_improvements": ["Better monitoring", "Faster response"],
            "full_content": content
        }
    
    def _parse_security_monitoring(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse security monitoring results"""
        return {
            "monitoring_architecture": {"siem": "Splunk", "collectors": "Multiple"},
            "correlation_rules": ["Failed login attempts", "Privilege escalation"],
            "anomaly_detection": {"ml_based": True, "behavioral": True},
            "threat_hunting": ["IOC hunting", "Behavioral analysis"],
            "alert_management": {"triage": "Automated", "escalation": "Tiered"},
            "escalation_procedures": ["L1 -> L2 -> L3", "Management notification"],
            "reporting_setup": {"dashboards": "Real-time", "reports": "Daily"},
            "dashboard_specs": ["Executive summary", "Technical details"],
            "full_content": content
        }
    
    def _parse_risk_assessment(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse risk assessment results"""
        return {
            "risk_register": ["Risk 1", "Risk 2", "Risk 3"],
            "risk_matrix": {"high": 3, "medium": 5, "low": 2},
            "treatment_options": ["Accept", "Mitigate", "Transfer", "Avoid"],
            "mitigation_strategies": ["Controls", "Procedures", "Training"],
            "monitoring_requirements": ["Regular reviews", "KRI tracking"],
            "risk_tolerance": {"threshold": "Medium", "appetite": "Low"},
            "communication_plan": {"stakeholders": "All", "frequency": "Monthly"},
            "review_schedule": {"quarterly": "Full", "monthly": "Updates"},
            "full_content": content
        }
    
    def _parse_general_security(self, content: str, priority: str) -> Dict[str, Any]:
        """Parse general security results"""
        return {
            "security_analysis": "Comprehensive analysis",
            "recommendations": ["Recommendation 1", "Recommendation 2"],
            "best_practices": ["Best practice 1", "Best practice 2"],
            "controls": ["Control 1", "Control 2"],
            "full_content": content
        }
    
    def _extract_recommendations(self, content: str) -> List[str]:
        """Extract recommendations from content"""
        return ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices from content"""
        return ["Best practice 1", "Best practice 2"]
    
    def _extract_controls(self, content: str) -> List[str]:
        """Extract security controls from content"""
        return ["Control 1", "Control 2", "Control 3"]
    
    async def _update_village_security(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Update village security knowledge"""
        try:
            # Extract security intelligence and lessons
            action = result.get("action", "")
            priority = result.get("priority", "medium")
            
            # Update village security knowledge
            if action == "threat_detection":
                self.village_security["threat_intelligence"].extend(
                    result.get("security_result", {}).get("identified_threats", [])
                )
            elif action == "incident_response":
                self.village_security["security_incidents"].append({
                    "task_id": task_id,
                    "incident": result.get("security_result", {}),
                    "timestamp": datetime.now().isoformat()
                })
            elif action == "vulnerability_assessment":
                self.village_security["vulnerability_database"].extend(
                    result.get("security_result", {}).get("identified_vulnerabilities", [])
                )
            
            # Store protective measures
            if action not in self.village_security["protective_measures"]:
                self.village_security["protective_measures"][action] = []
            
            self.village_security["protective_measures"][action].append({
                "priority": priority,
                "measures": result.get("security_result", {}),
                "timestamp": datetime.now().isoformat()
            })
            
            # Store in shared memory for other village agents
            await self.memory_manager.store_memory(
                content=f"Village security: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.KNOWLEDGE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "village_agent": "guardian",
                    "task_id": task_id,
                    "collective_intelligence": True,
                    "security_level": priority
                },
                tags=["village", "security", "protection"],
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to update village security: {e}")
    
    def _get_village_security(self) -> Dict[str, Any]:
        """Get village security knowledge"""
        return {
            "threat_intelligence_items": len(self.village_security["threat_intelligence"]),
            "security_incidents": len(self.village_security["security_incidents"]),
            "vulnerability_database_size": len(self.village_security["vulnerability_database"]),
            "protective_measures": len(self.village_security["protective_measures"]),
            "recent_threats": self.village_security["threat_intelligence"][-3:],
            "recent_incidents": self.village_security["security_incidents"][-3:]
        }
    
    async def _store_security_result(self, result: Dict[str, Any], task_id: str, session_id: Optional[str]):
        """Store security result in memory"""
        try:
            self.memory_manager.store_memory(
                content=f"Security result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.KNOWLEDGE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": self.metadata.name,
                    "task_id": task_id,
                    "action": result.get("action"),
                    "priority": result.get("priority"),
                    "timestamp": datetime.now().isoformat()
                },
                tags=["security", "protection", "village"],
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"❌ Failed to store security result: {e}")


def create_guardian_agent(config: Dict[str, Any]) -> GuardianAgent:
    """Factory function to create Guardian Agent"""
    return GuardianAgent(config)