"""
The-Agency Reviewer Agent Integration
Migrated from /home/mark/The-Agency/agents/reviewer.py
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


class ReviewerAgent(BaseAgent):
    """
    Reviewer Agent - Analyzes code quality and provides improvement suggestions
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="reviewer",
            agent_type=AgentType.REVIEWER,
            description="Analyzes code quality and provides improvement suggestions",
            capabilities=[
                "code_review",
                "quality_analysis",
                "security_review",
                "performance_analysis",
                "best_practices",
                "documentation_review",
                "style_checking",
                "refactoring_suggestions"
            ],
            model_requirements=["analysis", "reasoning", "text_generation"],
            priority=8,  # High priority for quality assurance
            max_concurrent_tasks=3,
            timeout_seconds=360  # Longer timeout for thorough analysis
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Code review criteria by language
        self.review_criteria = {
            "python": {
                "style_guide": "PEP 8",
                "key_checks": [
                    "naming_conventions",
                    "docstrings",
                    "type_hints",
                    "error_handling",
                    "imports",
                    "complexity"
                ],
                "tools": ["pylint", "flake8", "black", "mypy"]
            },
            "javascript": {
                "style_guide": "ESLint",
                "key_checks": [
                    "es6_features",
                    "async_await",
                    "error_handling",
                    "performance",
                    "security",
                    "testing"
                ],
                "tools": ["eslint", "prettier", "jshint"]
            },
            "java": {
                "style_guide": "Google Java Style",
                "key_checks": [
                    "naming_conventions",
                    "javadoc",
                    "exception_handling",
                    "generics",
                    "performance",
                    "security"
                ],
                "tools": ["checkstyle", "spotbugs", "pmd"]
            },
            "cpp": {
                "style_guide": "Google C++ Style",
                "key_checks": [
                    "memory_management",
                    "const_correctness",
                    "raii",
                    "performance",
                    "security",
                    "modern_cpp"
                ],
                "tools": ["clang-tidy", "cppcheck", "valgrind"]
            }
        }
        
        # Review severity levels
        self.severity_levels = {
            "CRITICAL": "Security vulnerabilities, memory leaks, or major bugs",
            "HIGH": "Performance issues, bad practices, or maintainability concerns",
            "MEDIUM": "Style violations, minor optimizations, or documentation issues",
            "LOW": "Suggestions for improvement or alternative approaches"
        }
        
        logger.info("🔍 Reviewer Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for reviewer agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires code review
        review_keywords = [
            "review", "analyze", "check", "quality", "improve", "optimize",
            "refactor", "security", "performance", "best practices", "critique"
        ]
        
        return any(keyword in content for keyword in review_keywords) or task_type == "review"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code review task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            language = task.get("language", "python")
            code_to_review = task.get("code_to_review", "")
            session_id = task.get("session_id")
            
            # Get project context and code to review
            context = await self.get_project_context(session_id)
            if not code_to_review and context.get("recent_code"):
                code_to_review = context["recent_code"]
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Review task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "reviewer",
                    "task_id": task.get("id"),
                    "language": language,
                    "code_length": len(code_to_review) if code_to_review else 0
                },
                session_id=session_id
            )
            
            # Create review prompt
            review_prompt = self._create_review_prompt(user_request, language, code_to_review, context)
            
            # Use orchestrator to generate review
            orchestrator_request = TaskRequest(
                id=f"reviewer_{task.get('id', 'unknown')}",
                content=review_prompt,
                task_type="analysis",
                complexity=self._determine_complexity(code_to_review),
                required_capabilities=[
                    ModelCapability.ANALYSIS,
                    ModelCapability.REASONING,
                    ModelCapability.TEXT_GENERATION
                ],
                max_tokens=3000,
                temperature=0.2,  # Low temperature for consistent, thorough analysis
                priority=8,
                metadata={
                    "agent": "reviewer",
                    "language": language,
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Code review failed: {response.error}")
            
            # Parse the review response
            review_results = self._parse_review_response(response.content, language)
            
            # Store review in memory
            review_memory_id = self.memory_manager.store_memory(
                content=f"Code review results: {json.dumps(review_results, indent=2)}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "reviewer",
                    "task_id": task.get("id"),
                    "language": language,
                    "review_score": review_results.get("overall_score", 0),
                    "issue_count": len(review_results.get("issues", [])),
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["review", "quality_assurance", language],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "review_results": review_results,
                "language": language,
                "memory_ids": [task_memory_id, review_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "reviewer",
                "metadata": {
                    "review_quality": "comprehensive",
                    "analysis_depth": "thorough",
                    "recommendations": "actionable"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Reviewer agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "reviewer"
            }
    
    def _create_review_prompt(self, user_request: str, language: str, code_to_review: str, context: Dict[str, Any]) -> str:
        """Create detailed review prompt"""
        criteria = self.review_criteria.get(language, {})
        style_guide = criteria.get("style_guide", "Standard conventions")
        key_checks = criteria.get("key_checks", [])
        tools = criteria.get("tools", [])
        
        context_str = ""
        if context.get("architecture"):
            context_str = f"\n\nProject Architecture:\n{json.dumps(context['architecture'], indent=2)}"
        
        code_section = ""
        if code_to_review:
            code_section = f"\n\nCode to Review:\n```{language}\n{code_to_review}\n```"
        
        return f"""
As an expert {language} code reviewer, conduct a comprehensive analysis of the following code.

Request: {user_request}

Language: {language}
Style Guide: {style_guide}
Key Areas to Check: {', '.join(key_checks)}
Recommended Tools: {', '.join(tools)}{code_section}{context_str}

Please provide a detailed code review covering:

1. **OVERALL ASSESSMENT**
   - Code quality score (1-10)
   - Overall readability and maintainability
   - Adherence to best practices

2. **SECURITY ANALYSIS**
   - Potential security vulnerabilities
   - Input validation issues
   - Authentication/authorization concerns
   - Data exposure risks

3. **PERFORMANCE ANALYSIS**
   - Algorithm efficiency
   - Memory usage patterns
   - Database query optimization
   - Caching opportunities

4. **CODE QUALITY ISSUES**
   - Naming conventions
   - Code structure and organization
   - Error handling
   - Documentation quality

5. **STYLE AND CONVENTIONS**
   - Adherence to {style_guide}
   - Consistency with project standards
   - Code formatting issues

6. **SPECIFIC RECOMMENDATIONS**
   - Priority fixes (Critical/High/Medium/Low)
   - Refactoring suggestions
   - Performance improvements
   - Security enhancements

7. **POSITIVE ASPECTS**
   - Well-implemented features
   - Good practices observed
   - Strengths to maintain

Format your response as a structured review with:
- Clear severity levels for each issue
- Specific line references where applicable
- Actionable recommendations
- Code examples for improvements where helpful

Review Criteria:
- CRITICAL: Security vulnerabilities, major bugs
- HIGH: Performance issues, bad practices
- MEDIUM: Style violations, minor optimizations
- LOW: Suggestions for improvement

Please be thorough but constructive in your analysis.
"""
    
    def _determine_complexity(self, code_to_review: str) -> TaskComplexity:
        """Determine review complexity based on code"""
        if not code_to_review:
            return TaskComplexity.SIMPLE
        
        lines = len(code_to_review.split('\n'))
        complexity_indicators = 0
        
        # Check code size
        if lines > 200:
            complexity_indicators += 3
        elif lines > 100:
            complexity_indicators += 2
        elif lines > 50:
            complexity_indicators += 1
        
        # Check for complex patterns
        complex_patterns = [
            "async", "await", "threading", "multiprocessing", "concurrent",
            "database", "sql", "api", "network", "security", "crypto",
            "performance", "optimization", "algorithm", "data structure"
        ]
        
        code_lower = code_to_review.lower()
        for pattern in complex_patterns:
            if pattern in code_lower:
                complexity_indicators += 1
        
        # Check for multiple classes/functions
        class_count = len(re.findall(r'class\s+\w+', code_to_review))
        function_count = len(re.findall(r'def\s+\w+|function\s+\w+', code_to_review))
        
        if class_count > 5 or function_count > 10:
            complexity_indicators += 2
        elif class_count > 2 or function_count > 5:
            complexity_indicators += 1
        
        if complexity_indicators >= 5:
            return TaskComplexity.EXPERT
        elif complexity_indicators >= 3:
            return TaskComplexity.COMPLEX
        elif complexity_indicators >= 1:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _parse_review_response(self, response_content: str, language: str) -> Dict[str, Any]:
        """Parse the review response into structured format"""
        try:
            # Extract overall score
            score_match = re.search(r'score[:\s]+(\d+(?:\.\d+)?)', response_content, re.IGNORECASE)
            overall_score = float(score_match.group(1)) if score_match else 0
            
            # Extract issues by severity
            issues = []
            severity_patterns = {
                "CRITICAL": r'CRITICAL[:\s]+(.*?)(?=HIGH|MEDIUM|LOW|$)',
                "HIGH": r'HIGH[:\s]+(.*?)(?=CRITICAL|MEDIUM|LOW|$)',
                "MEDIUM": r'MEDIUM[:\s]+(.*?)(?=CRITICAL|HIGH|LOW|$)',
                "LOW": r'LOW[:\s]+(.*?)(?=CRITICAL|HIGH|MEDIUM|$)'
            }
            
            for severity, pattern in severity_patterns.items():
                matches = re.findall(pattern, response_content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    issues.append({
                        "severity": severity,
                        "description": match.strip(),
                        "category": self._categorize_issue(match.strip())
                    })
            
            # Extract recommendations
            recommendations = self._extract_recommendations(response_content)
            
            # Extract positive aspects
            positive_aspects = self._extract_positive_aspects(response_content)
            
            # Calculate quality metrics
            quality_metrics = {
                "overall_score": overall_score,
                "issue_count": len(issues),
                "critical_issues": len([i for i in issues if i["severity"] == "CRITICAL"]),
                "high_issues": len([i for i in issues if i["severity"] == "HIGH"]),
                "medium_issues": len([i for i in issues if i["severity"] == "MEDIUM"]),
                "low_issues": len([i for i in issues if i["severity"] == "LOW"]),
                "maintainability_score": self._calculate_maintainability_score(issues),
                "security_score": self._calculate_security_score(issues),
                "performance_score": self._calculate_performance_score(issues)
            }
            
            return {
                "overall_score": overall_score,
                "quality_metrics": quality_metrics,
                "issues": issues,
                "recommendations": recommendations,
                "positive_aspects": positive_aspects,
                "language": language,
                "review_timestamp": datetime.now().isoformat(),
                "raw_review": response_content
            }
            
        except Exception as e:
            logger.warning(f"⚠️  Review parsing failed: {e}")
            return {
                "overall_score": 0,
                "quality_metrics": {},
                "issues": [],
                "recommendations": [],
                "positive_aspects": [],
                "language": language,
                "raw_review": response_content,
                "parse_error": str(e)
            }
    
    def _categorize_issue(self, issue_description: str) -> str:
        """Categorize issue based on description"""
        description_lower = issue_description.lower()
        
        if any(word in description_lower for word in ["security", "vulnerability", "authentication", "authorization"]):
            return "security"
        elif any(word in description_lower for word in ["performance", "efficiency", "slow", "memory"]):
            return "performance"
        elif any(word in description_lower for word in ["style", "formatting", "convention", "naming"]):
            return "style"
        elif any(word in description_lower for word in ["error", "exception", "handling", "validation"]):
            return "error_handling"
        elif any(word in description_lower for word in ["documentation", "comment", "docstring"]):
            return "documentation"
        else:
            return "general"
    
    def _extract_recommendations(self, response_content: str) -> List[str]:
        """Extract specific recommendations from the review"""
        recommendations = []
        
        # Look for recommendation sections
        rec_pattern = r'RECOMMENDATIONS?[:\s]+(.*?)(?=\n\n|\Z)'
        matches = re.findall(rec_pattern, response_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            # Split by bullet points or numbers
            items = re.split(r'[•\-\*]|\d+\.', match)
            for item in items:
                item = item.strip()
                if item and len(item) > 10:
                    recommendations.append(item)
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _extract_positive_aspects(self, response_content: str) -> List[str]:
        """Extract positive aspects from the review"""
        positive = []
        
        # Look for positive sections
        pos_pattern = r'POSITIVE[:\s]+(.*?)(?=\n\n|\Z)'
        matches = re.findall(pos_pattern, response_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            # Split by bullet points or numbers
            items = re.split(r'[•\-\*]|\d+\.', match)
            for item in items:
                item = item.strip()
                if item and len(item) > 10:
                    positive.append(item)
        
        return positive[:5]  # Limit to top 5 positive aspects
    
    def _calculate_maintainability_score(self, issues: List[Dict[str, Any]]) -> float:
        """Calculate maintainability score based on issues"""
        score = 10.0
        
        for issue in issues:
            if issue["severity"] == "CRITICAL":
                score -= 2.0
            elif issue["severity"] == "HIGH":
                score -= 1.0
            elif issue["severity"] == "MEDIUM":
                score -= 0.5
            elif issue["severity"] == "LOW":
                score -= 0.2
        
        return max(0.0, min(10.0, score))
    
    def _calculate_security_score(self, issues: List[Dict[str, Any]]) -> float:
        """Calculate security score based on security-related issues"""
        score = 10.0
        
        for issue in issues:
            if issue.get("category") == "security":
                if issue["severity"] == "CRITICAL":
                    score -= 3.0
                elif issue["severity"] == "HIGH":
                    score -= 2.0
                elif issue["severity"] == "MEDIUM":
                    score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def _calculate_performance_score(self, issues: List[Dict[str, Any]]) -> float:
        """Calculate performance score based on performance-related issues"""
        score = 10.0
        
        for issue in issues:
            if issue.get("category") == "performance":
                if issue["severity"] == "CRITICAL":
                    score -= 2.5
                elif issue["severity"] == "HIGH":
                    score -= 1.5
                elif issue["severity"] == "MEDIUM":
                    score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context and recent code from memory"""
        try:
            # Get recent code for review
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
            
            context = {
                "recent_code": "",
                "architecture": {},
                "previous_reviews": []
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
            
            # Get previous reviews
            review_items = self.memory_manager.search_memory(
                query="reviewer",
                memory_type=MemoryType.TASK,
                use_vector=True,
                limit=2
            )
            
            for item in review_items:
                if "review_score" in item.metadata:
                    context["previous_reviews"].append({
                        "score": item.metadata["review_score"],
                        "date": item.created_at.isoformat()
                    })
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get reviewer agent statistics"""
        return {
            **self.stats,
            "supported_languages": list(self.review_criteria.keys()),
            "review_criteria": self.review_criteria,
            "severity_levels": self.severity_levels,
            "reviews_completed": len(self.memory_manager.search_memory(
                query="reviewer",
                memory_type=MemoryType.TASK,
                limit=1000
            )),
            "review_capabilities": [
                "security_analysis",
                "performance_review",
                "code_quality_assessment",
                "style_checking",
                "best_practices_validation"
            ]
        }


def create_reviewer_agent(config: Dict[str, Any]) -> ReviewerAgent:
    """Factory function to create reviewer agent"""
    return ReviewerAgent(config)