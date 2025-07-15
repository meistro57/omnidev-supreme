"""
OBELISK Quality Checker Agent
Performs comprehensive code quality analysis and security review
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


class QualityCheckerAgent(BaseAgent):
    """
    OBELISK Quality Checker Agent
    
    Specializes in:
    - Code quality analysis
    - Security vulnerability detection
    - Performance optimization suggestions
    - Best practices validation
    - Code style and conventions
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="quality_checker",
            agent_type=AgentType.REVIEWER,
            description="OBELISK Quality Checker - Comprehensive code quality analysis and security review",
            capabilities=[
                "code_quality_analysis",
                "security_vulnerability_detection",
                "performance_optimization",
                "best_practices_validation",
                "code_style_checking",
                "bug_detection",
                "maintainability_assessment",
                "complexity_analysis"
            ],
            model_requirements=["analysis", "reasoning", "security"],
            priority=8,
            max_concurrent_tasks=2,
            timeout_seconds=720,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Quality check categories and severity levels
        self.check_categories = {
            "security": {
                "weight": 0.3,
                "checks": [
                    "sql_injection",
                    "xss_vulnerabilities",
                    "authentication_issues",
                    "authorization_flaws",
                    "input_validation",
                    "data_encryption",
                    "sensitive_data_exposure"
                ]
            },
            "performance": {
                "weight": 0.2,
                "checks": [
                    "time_complexity",
                    "memory_usage",
                    "database_queries",
                    "caching_strategy",
                    "resource_management",
                    "algorithm_efficiency"
                ]
            },
            "maintainability": {
                "weight": 0.25,
                "checks": [
                    "code_readability",
                    "documentation_quality",
                    "function_complexity",
                    "code_duplication",
                    "naming_conventions",
                    "separation_of_concerns"
                ]
            },
            "reliability": {
                "weight": 0.15,
                "checks": [
                    "error_handling",
                    "edge_cases",
                    "null_pointer_safety",
                    "resource_cleanup",
                    "exception_handling",
                    "defensive_programming"
                ]
            },
            "standards": {
                "weight": 0.1,
                "checks": [
                    "coding_standards",
                    "style_guidelines",
                    "documentation_standards",
                    "testing_standards",
                    "version_control_practices"
                ]
            }
        }
        
        self.severity_levels = {
            "CRITICAL": {"score": 10, "description": "Critical issues that must be fixed immediately"},
            "HIGH": {"score": 7, "description": "High priority issues that should be fixed soon"},
            "MEDIUM": {"score": 4, "description": "Medium priority issues that should be addressed"},
            "LOW": {"score": 1, "description": "Low priority issues or suggestions"},
            "INFO": {"score": 0, "description": "Informational notes or suggestions"}
        }
        
        # Language-specific quality rules
        self.language_rules = {
            "python": {
                "style_guide": "PEP 8",
                "security_patterns": [
                    r"eval\(",
                    r"exec\(",
                    r"input\(",
                    r"os\.system\(",
                    r"subprocess\.call\("
                ],
                "performance_patterns": [
                    r"for.*in.*range\(len\(",
                    r"\.append\(.*\).*in.*for",
                    r"global\s+\w+"
                ],
                "best_practices": [
                    "Use type hints",
                    "Follow PEP 8 naming conventions",
                    "Use context managers for resources",
                    "Prefer f-strings over .format()",
                    "Use list comprehensions appropriately"
                ]
            },
            "javascript": {
                "style_guide": "ESLint",
                "security_patterns": [
                    r"eval\(",
                    r"innerHTML\s*=",
                    r"document\.write\(",
                    r"setTimeout\([^,]*\)",
                    r"setInterval\([^,]*\)"
                ],
                "performance_patterns": [
                    r"for.*in.*",
                    r"document\.getElementById",
                    r"\.length.*for"
                ],
                "best_practices": [
                    "Use const/let instead of var",
                    "Use arrow functions appropriately",
                    "Avoid global variables",
                    "Use strict mode",
                    "Handle promises with async/await"
                ]
            },
            "java": {
                "style_guide": "Google Java Style",
                "security_patterns": [
                    r"Runtime\.getRuntime\(",
                    r"Class\.forName\(",
                    r"System\.getProperty\(",
                    r"ProcessBuilder\("
                ],
                "performance_patterns": [
                    r"String\s+\w+\s*=.*\+",
                    r"\.equals\(\s*\"\"",
                    r"new.*ArrayList\(\)"
                ],
                "best_practices": [
                    "Use final for immutable variables",
                    "Override equals() and hashCode() together",
                    "Use try-with-resources",
                    "Prefer StringBuilder for string concatenation",
                    "Use generic types"
                ]
            },
            "go": {
                "style_guide": "Go Code Review Comments",
                "security_patterns": [
                    r"os\.Exec\(",
                    r"exec\.Command\(",
                    r"unsafe\.",
                    r"reflect\."
                ],
                "performance_patterns": [
                    r"fmt\.Sprintf\(",
                    r"range.*\[\]byte",
                    r"defer.*in.*for"
                ],
                "best_practices": [
                    "Handle errors explicitly",
                    "Use gofmt for formatting",
                    "Follow Go naming conventions",
                    "Use channels for goroutine communication",
                    "Avoid empty catch blocks"
                ]
            }
        }
        
        logger.info(f"🔍 {self.metadata.name} initialized with comprehensive quality checking capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for quality checker agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires quality checking
        quality_keywords = [
            "quality", "check", "review", "analyze", "audit", "validate",
            "inspect", "examine", "security", "performance", "bug", "error"
        ]
        
        return any(keyword in content for keyword in quality_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute quality check task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"qc_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"🔍 Starting quality check: {task_id}")
            
            # Extract task parameters
            code_to_check = task.get("code_to_check", "")
            language = task.get("language", "python")
            check_types = task.get("check_types", list(self.check_categories.keys()))
            context = task.get("context", {})
            
            # Perform comprehensive quality analysis
            quality_result = await self._perform_quality_analysis(
                code=code_to_check,
                language=language,
                check_types=check_types,
                context=context
            )
            
            # Store results in memory
            await self._store_quality_results(
                task_id=task_id,
                quality_result=quality_result,
                language=language,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "quality_analysis": quality_result,
                "language": language,
                "check_types": check_types,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"qc_{task_id}",
                "tokens_used": quality_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Quality check completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Quality check failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _perform_quality_analysis(
        self,
        code: str,
        language: str,
        check_types: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive quality analysis"""
        
        # Get language-specific rules
        lang_rules = self.language_rules.get(language, self.language_rules["python"])
        
        # Create quality analysis prompt
        quality_prompt = self._create_quality_analysis_prompt(
            code=code,
            language=language,
            check_types=check_types,
            lang_rules=lang_rules,
            context=context
        )
        
        # Perform analysis using best available model
        try:
            response = await self.orchestrator.generate_response(
                prompt=quality_prompt,
                model_preference=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
                temperature=0.0,  # Zero temperature for consistent analysis
                max_tokens=5000
            )
            
            # Parse and structure analysis response
            analysis_result = await self._parse_quality_response(
                response=response,
                code=code,
                language=language,
                check_types=check_types
            )
            
            # Perform additional static analysis
            static_analysis = self._perform_static_analysis(code, language, lang_rules)
            
            # Combine results
            combined_result = self._combine_analysis_results(analysis_result, static_analysis)
            
            return combined_result
            
        except Exception as e:
            logger.error(f"❌ Quality analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": self._create_fallback_analysis(code, language)
            }
    
    def _create_quality_analysis_prompt(
        self,
        code: str,
        language: str,
        check_types: List[str],
        lang_rules: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed quality analysis prompt"""
        
        return f"""
You are an expert code reviewer and security analyst tasked with performing a comprehensive quality analysis of the provided code.

CODE TO ANALYZE:
```{language}
{code}
```

LANGUAGE: {language}
STYLE GUIDE: {lang_rules.get('style_guide', 'Standard conventions')}
ANALYSIS TYPES: {check_types}

CONTEXT:
{context}

QUALITY ANALYSIS REQUIREMENTS:
Analyze the code for the following categories:

1. SECURITY ANALYSIS:
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Authentication and authorization issues
   - Input validation problems
   - Data encryption concerns
   - Sensitive data exposure

2. PERFORMANCE ANALYSIS:
   - Time complexity issues
   - Memory usage problems
   - Database query optimization
   - Caching opportunities
   - Resource management
   - Algorithm efficiency

3. MAINTAINABILITY ANALYSIS:
   - Code readability and clarity
   - Documentation quality
   - Function complexity
   - Code duplication
   - Naming conventions
   - Separation of concerns

4. RELIABILITY ANALYSIS:
   - Error handling adequacy
   - Edge case coverage
   - Null pointer safety
   - Resource cleanup
   - Exception handling
   - Defensive programming

5. STANDARDS COMPLIANCE:
   - Coding standards adherence
   - Style guide compliance
   - Documentation standards
   - Testing standards
   - Version control practices

BEST PRACTICES FOR {language.upper()}:
{chr(10).join(f"- {practice}" for practice in lang_rules.get('best_practices', []))}

Please provide your analysis in the following JSON format:
{{
    "overall_score": 0-100,
    "quality_grade": "A|B|C|D|F",
    "analysis_summary": "Brief summary of code quality",
    "categories": {{
        "security": {{
            "score": 0-100,
            "grade": "A|B|C|D|F",
            "issues": [
                {{
                    "type": "issue_type",
                    "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
                    "description": "detailed description",
                    "line_number": 0,
                    "suggestion": "how to fix",
                    "impact": "potential impact"
                }}
            ]
        }},
        "performance": {{
            "score": 0-100,
            "grade": "A|B|C|D|F",
            "issues": [...]
        }},
        "maintainability": {{
            "score": 0-100,
            "grade": "A|B|C|D|F",
            "issues": [...]
        }},
        "reliability": {{
            "score": 0-100,
            "grade": "A|B|C|D|F",
            "issues": [...]
        }},
        "standards": {{
            "score": 0-100,
            "grade": "A|B|C|D|F",
            "issues": [...]
        }}
    }},
    "improvements": [
        {{
            "priority": "HIGH|MEDIUM|LOW",
            "category": "security|performance|maintainability|reliability|standards",
            "description": "improvement description",
            "effort": "LOW|MEDIUM|HIGH",
            "impact": "LOW|MEDIUM|HIGH"
        }}
    ],
    "metrics": {{
        "lines_of_code": 0,
        "complexity_score": 0-100,
        "duplication_percentage": 0-100,
        "test_coverage_estimate": 0-100,
        "documentation_score": 0-100
    }},
    "recommendations": [
        "specific actionable recommendations"
    ]
}}

Be thorough, specific, and provide actionable feedback with clear explanations.
"""
    
    def _perform_static_analysis(self, code: str, language: str, lang_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Perform basic static analysis using regex patterns"""
        
        static_issues = []
        
        # Check for security patterns
        for pattern in lang_rules.get("security_patterns", []):
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                static_issues.append({
                    "type": "security_pattern",
                    "severity": "HIGH",
                    "description": f"Potentially unsafe pattern detected: {match.group()}",
                    "line_number": line_number,
                    "suggestion": "Review this pattern for security implications",
                    "pattern": pattern
                })
        
        # Check for performance patterns
        for pattern in lang_rules.get("performance_patterns", []):
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                static_issues.append({
                    "type": "performance_pattern",
                    "severity": "MEDIUM",
                    "description": f"Potentially inefficient pattern detected: {match.group()}",
                    "line_number": line_number,
                    "suggestion": "Consider optimizing this pattern",
                    "pattern": pattern
                })
        
        # Basic metrics
        lines = code.split('\n')
        metrics = {
            "lines_of_code": len([line for line in lines if line.strip()]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "average_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0
        }
        
        return {
            "static_issues": static_issues,
            "metrics": metrics,
            "patterns_checked": len(lang_rules.get("security_patterns", [])) + len(lang_rules.get("performance_patterns", []))
        }
    
    async def _parse_quality_response(
        self,
        response: str,
        code: str,
        language: str,
        check_types: List[str]
    ) -> Dict[str, Any]:
        """Parse and validate quality analysis response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            analysis_data = json.loads(json_str)
            
            # Validate and enhance analysis data
            quality_result = {
                "success": True,
                "language": language,
                "check_types": check_types,
                "analyzed_at": datetime.now().isoformat(),
                "analysis": analysis_data,
                "metadata": {
                    "total_issues": sum(
                        len(category.get("issues", []))
                        for category in analysis_data.get("categories", {}).values()
                    ),
                    "critical_issues": sum(
                        len([issue for issue in category.get("issues", []) if issue.get("severity") == "CRITICAL"])
                        for category in analysis_data.get("categories", {}).values()
                    ),
                    "high_issues": sum(
                        len([issue for issue in category.get("issues", []) if issue.get("severity") == "HIGH"])
                        for category in analysis_data.get("categories", {}).values()
                    ),
                    "overall_score": analysis_data.get("overall_score", 0),
                    "quality_grade": analysis_data.get("quality_grade", "F")
                },
                "tokens_used": len(response.split())
            }
            
            return quality_result
            
        except Exception as e:
            logger.error(f"❌ Quality analysis parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse quality analysis: {str(e)}",
                "raw_response": response,
                "fallback_analysis": self._create_fallback_analysis(code, language)
            }
    
    def _combine_analysis_results(self, ai_analysis: Dict[str, Any], static_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Combine AI analysis with static analysis results"""
        
        if not ai_analysis.get("success"):
            return ai_analysis
        
        # Add static analysis issues to appropriate categories
        combined_analysis = ai_analysis.copy()
        
        if "analysis" in combined_analysis and "categories" in combined_analysis["analysis"]:
            for issue in static_analysis.get("static_issues", []):
                if issue["type"] == "security_pattern":
                    if "security" not in combined_analysis["analysis"]["categories"]:
                        combined_analysis["analysis"]["categories"]["security"] = {"issues": []}
                    combined_analysis["analysis"]["categories"]["security"]["issues"].append(issue)
                elif issue["type"] == "performance_pattern":
                    if "performance" not in combined_analysis["analysis"]["categories"]:
                        combined_analysis["analysis"]["categories"]["performance"] = {"issues": []}
                    combined_analysis["analysis"]["categories"]["performance"]["issues"].append(issue)
        
        # Enhance metrics with static analysis data
        if "analysis" in combined_analysis and "metrics" in combined_analysis["analysis"]:
            combined_analysis["analysis"]["metrics"].update(static_analysis.get("metrics", {}))
        
        # Update metadata
        combined_analysis["metadata"]["static_patterns_checked"] = static_analysis.get("patterns_checked", 0)
        combined_analysis["metadata"]["static_issues_found"] = len(static_analysis.get("static_issues", []))
        
        return combined_analysis
    
    def _create_fallback_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Create basic fallback analysis"""
        
        lines = code.split('\n')
        loc = len([line for line in lines if line.strip()])
        
        return {
            "overall_score": 70,
            "quality_grade": "C",
            "analysis_summary": "Basic analysis - unable to perform comprehensive review",
            "categories": {
                "security": {
                    "score": 70,
                    "grade": "C",
                    "issues": [
                        {
                            "type": "unknown",
                            "severity": "INFO",
                            "description": "Unable to perform comprehensive security analysis",
                            "line_number": 0,
                            "suggestion": "Manual security review recommended",
                            "impact": "Unknown"
                        }
                    ]
                },
                "performance": {"score": 70, "grade": "C", "issues": []},
                "maintainability": {"score": 70, "grade": "C", "issues": []},
                "reliability": {"score": 70, "grade": "C", "issues": []},
                "standards": {"score": 70, "grade": "C", "issues": []}
            },
            "improvements": [
                {
                    "priority": "MEDIUM",
                    "category": "general",
                    "description": "Comprehensive code review recommended",
                    "effort": "MEDIUM",
                    "impact": "MEDIUM"
                }
            ],
            "metrics": {
                "lines_of_code": loc,
                "complexity_score": 50,
                "duplication_percentage": 0,
                "test_coverage_estimate": 0,
                "documentation_score": 50
            },
            "recommendations": [
                "Perform manual code review",
                "Add comprehensive tests",
                "Improve documentation",
                "Follow coding standards"
            ]
        }
    
    async def _store_quality_results(
        self,
        task_id: str,
        quality_result: Dict[str, Any],
        language: str,
        session_id: Optional[str] = None
    ):
        """Store quality analysis results in memory"""
        
        content = f"""
Quality Analysis Results

Task ID: {task_id}
Language: {language}
Analyzed: {datetime.now().isoformat()}

Quality Summary:
- Success: {quality_result.get('success', False)}
- Overall Score: {quality_result.get('metadata', {}).get('overall_score', 0)}/100
- Quality Grade: {quality_result.get('metadata', {}).get('quality_grade', 'F')}
- Total Issues: {quality_result.get('metadata', {}).get('total_issues', 0)}
- Critical Issues: {quality_result.get('metadata', {}).get('critical_issues', 0)}
- High Issues: {quality_result.get('metadata', {}).get('high_issues', 0)}

Full Analysis Result:
{json.dumps(quality_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.TASK,
            priority=MemoryPriority.HIGH,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "language": language,
                "quality_success": quality_result.get("success", False),
                "overall_score": quality_result.get("metadata", {}).get("overall_score", 0),
                "quality_grade": quality_result.get("metadata", {}).get("quality_grade", "F"),
                "total_issues": quality_result.get("metadata", {}).get("total_issues", 0),
                "critical_issues": quality_result.get("metadata", {}).get("critical_issues", 0)
            },
            tags=["quality_analysis", "code_review", "obelisk", "quality_checker"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "supported_languages": list(self.language_rules.keys()),
            "check_categories": list(self.check_categories.keys()),
            "severity_levels": list(self.severity_levels.keys()),
            "analysis_features": [
                "Security vulnerability detection",
                "Performance optimization suggestions",
                "Maintainability assessment",
                "Reliability analysis",
                "Standards compliance checking",
                "Static code analysis",
                "Metrics calculation",
                "Actionable recommendations"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_quality_checker_agent(config: Dict[str, Any]) -> QualityCheckerAgent:
    """Factory function to create Quality Checker Agent"""
    return QualityCheckerAgent(config)