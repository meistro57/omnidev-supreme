"""
The-Agency Fixer Agent Integration
Migrated from /home/mark/The-Agency/agents/fixer.py
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


class FixerAgent(BaseAgent):
    """
    Fixer Agent - Resolves issues and bugs in code
    Integrated from The-Agency system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="fixer",
            agent_type=AgentType.FIXER,
            description="Resolves issues and bugs in code",
            capabilities=[
                "bug_fixing",
                "error_resolution",
                "code_repair",
                "performance_optimization",
                "security_fixes",
                "dependency_resolution",
                "refactoring",
                "debugging"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=9,  # Very high priority for critical fixes
            max_concurrent_tasks=2,
            timeout_seconds=600  # Longer timeout for complex fixes
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Fix categories and patterns
        self.fix_categories = {
            "syntax_errors": {
                "patterns": ["SyntaxError", "IndentationError", "TabError", "unexpected EOF"],
                "priority": "CRITICAL",
                "typical_fixes": ["Fix indentation", "Add missing brackets", "Correct syntax"]
            },
            "runtime_errors": {
                "patterns": ["RuntimeError", "ValueError", "TypeError", "AttributeError", "KeyError"],
                "priority": "HIGH",
                "typical_fixes": ["Add error handling", "Type checking", "Null checks"]
            },
            "logic_errors": {
                "patterns": ["incorrect result", "wrong output", "logic bug", "algorithm error"],
                "priority": "HIGH",
                "typical_fixes": ["Fix algorithm", "Correct logic flow", "Update conditions"]
            },
            "performance_issues": {
                "patterns": ["slow performance", "memory leak", "inefficient", "optimization"],
                "priority": "MEDIUM",
                "typical_fixes": ["Optimize algorithms", "Reduce complexity", "Cache results"]
            },
            "security_vulnerabilities": {
                "patterns": ["security", "vulnerability", "injection", "XSS", "CSRF"],
                "priority": "CRITICAL",
                "typical_fixes": ["Input validation", "Sanitization", "Authentication"]
            },
            "dependency_issues": {
                "patterns": ["ImportError", "ModuleNotFoundError", "dependency", "version conflict"],
                "priority": "HIGH",
                "typical_fixes": ["Install dependencies", "Update versions", "Resolve conflicts"]
            }
        }
        
        logger.info("🔧 Fixer Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for fixer agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires fixing
        fixing_keywords = [
            "fix", "debug", "resolve", "repair", "error", "bug", "issue",
            "problem", "broken", "failing", "crash", "exception"
        ]
        
        return any(keyword in content for keyword in fixing_keywords) or task_type == "fixing"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute bug fixing task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            language = task.get("language", "python")
            broken_code = task.get("broken_code", "")
            error_message = task.get("error_message", "")
            session_id = task.get("session_id")
            
            # Get project context and recent issues
            context = await self.get_project_context(session_id)
            if not broken_code and context.get("recent_code"):
                broken_code = context["recent_code"]
            
            # Analyze the issue
            issue_analysis = self._analyze_issue(user_request, error_message, broken_code)
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Fixing task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.CRITICAL,
                metadata={
                    "agent": "fixer",
                    "task_id": task.get("id"),
                    "language": language,
                    "issue_category": issue_analysis["category"],
                    "issue_priority": issue_analysis["priority"],
                    "error_message": error_message
                },
                session_id=session_id
            )
            
            # Create fixing prompt
            fixing_prompt = self._create_fixing_prompt(
                user_request, language, broken_code, error_message, issue_analysis, context
            )
            
            # Use orchestrator to generate fix
            orchestrator_request = TaskRequest(
                id=f"fixer_{task.get('id', 'unknown')}",
                content=fixing_prompt,
                task_type="code_generation",
                complexity=self._determine_complexity(broken_code, error_message),
                required_capabilities=[
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.REASONING
                ],
                max_tokens=3000,
                temperature=0.1,  # Very low temperature for precise fixes
                priority=9,
                metadata={
                    "agent": "fixer",
                    "language": language,
                    "issue_category": issue_analysis["category"],
                    "original_task": task.get("id")
                }
            )
            
            response = await self.orchestrator.execute_task(orchestrator_request)
            
            if not response.success:
                raise Exception(f"Fix generation failed: {response.error}")
            
            # Parse the fix response
            fix_results = self._parse_fix_response(response.content, language, issue_analysis)
            
            # Validate the fix
            validated_fix = await self._validate_fix(fix_results, broken_code, error_message)
            
            # Store fix in memory
            fix_memory_id = self.memory_manager.store_memory(
                content=f"Generated fix: {json.dumps(validated_fix, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "fixer",
                    "task_id": task.get("id"),
                    "language": language,
                    "issue_category": issue_analysis["category"],
                    "fix_confidence": validated_fix.get("confidence", 0),
                    "tokens_used": response.tokens_used,
                    "model_used": response.model_type.value
                },
                tags=["fix", "resolved", language, issue_analysis["category"]],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "fix_results": validated_fix,
                "issue_analysis": issue_analysis,
                "language": language,
                "memory_ids": [task_memory_id, fix_memory_id],
                "tokens_used": response.tokens_used,
                "response_time": execution_time,
                "model_used": response.model_type.value,
                "agent": "fixer",
                "metadata": {
                    "fix_quality": "validated",
                    "issue_resolved": validated_fix.get("likely_resolved", False),
                    "requires_testing": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Fixer agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0,
                "response_time": 0,
                "agent": "fixer"
            }
    
    def _analyze_issue(self, user_request: str, error_message: str, broken_code: str) -> Dict[str, Any]:
        """Analyze the issue to determine category and priority"""
        issue_text = f"{user_request} {error_message}".lower()
        
        # Determine category
        category = "unknown"
        priority = "MEDIUM"
        
        for cat, info in self.fix_categories.items():
            if any(pattern.lower() in issue_text for pattern in info["patterns"]):
                category = cat
                priority = info["priority"]
                break
        
        # Analyze complexity
        complexity_factors = []
        if len(broken_code) > 500:
            complexity_factors.append("large_codebase")
        if any(word in issue_text for word in ["async", "threading", "concurrent"]):
            complexity_factors.append("concurrency")
        if any(word in issue_text for word in ["database", "sql", "orm"]):
            complexity_factors.append("database")
        if any(word in issue_text for word in ["network", "api", "http"]):
            complexity_factors.append("network")
        
        return {
            "category": category,
            "priority": priority,
            "complexity_factors": complexity_factors,
            "estimated_difficulty": len(complexity_factors),
            "typical_fixes": self.fix_categories.get(category, {}).get("typical_fixes", [])
        }
    
    def _create_fixing_prompt(self, user_request: str, language: str, broken_code: str, 
                            error_message: str, issue_analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create detailed fixing prompt"""
        context_str = ""
        if context.get("architecture"):
            context_str = f"\n\nProject Architecture:\n{json.dumps(context['architecture'], indent=2)}"
        
        error_section = ""
        if error_message:
            error_section = f"\n\nError Message:\n{error_message}"
        
        broken_code_section = ""
        if broken_code:
            broken_code_section = f"\n\nBroken Code:\n```{language}\n{broken_code}\n```"
        
        typical_fixes = issue_analysis.get("typical_fixes", [])
        typical_fixes_str = "\n".join(f"- {fix}" for fix in typical_fixes)
        
        return f"""
As an expert {language} debugging and fixing specialist, resolve the following issue:

Request: {user_request}

Issue Category: {issue_analysis["category"]}
Priority: {issue_analysis["priority"]}
Complexity Factors: {", ".join(issue_analysis["complexity_factors"])}

Typical Fixes for {issue_analysis["category"]}:
{typical_fixes_str}{error_section}{broken_code_section}{context_str}

Please provide a comprehensive fix that includes:

1. **ROOT CAUSE ANALYSIS**
   - Identify the exact cause of the issue
   - Explain why the current code is failing
   - Highlight problematic patterns

2. **COMPLETE SOLUTION**
   - Provide fully corrected code
   - Include all necessary imports and dependencies
   - Ensure the fix addresses the root cause

3. **ERROR HANDLING**
   - Add appropriate error handling
   - Include input validation where needed
   - Prevent similar issues in the future

4. **TESTING STRATEGY**
   - Suggest test cases to verify the fix
   - Include edge cases that should be tested
   - Recommend validation steps

5. **PREVENTION MEASURES**
   - Code improvements to prevent similar issues
   - Best practices to follow
   - Recommended tooling or patterns

6. **EXPLANATION**
   - Clear explanation of changes made
   - Why each change was necessary
   - How the fix resolves the original issue

Format your response as:
```{language}
// Fixed code here
[corrected code]
```

**Root Cause:** [explanation]
**Changes Made:** [list of changes]
**Testing Notes:** [testing recommendations]
**Prevention:** [future prevention suggestions]

Please ensure the fix is:
- Complete and production-ready
- Well-tested and validated
- Properly documented
- Following best practices for {language}
"""
    
    def _determine_complexity(self, broken_code: str, error_message: str) -> TaskComplexity:
        """Determine fix complexity based on code and error"""
        complexity_factors = 0
        
        # Check code size
        if broken_code:
            lines = len(broken_code.split('\n'))
            if lines > 200:
                complexity_factors += 3
            elif lines > 100:
                complexity_factors += 2
            elif lines > 50:
                complexity_factors += 1
        
        # Check error complexity
        if error_message:
            error_lower = error_message.lower()
            complex_errors = [
                "memory", "threading", "async", "concurrent", "database", 
                "network", "performance", "security", "algorithm"
            ]
            for error_type in complex_errors:
                if error_type in error_lower:
                    complexity_factors += 1
        
        # Check for complex patterns in code
        if broken_code:
            complex_patterns = [
                "class", "def", "async", "await", "threading", "multiprocessing",
                "database", "sql", "api", "network", "decorator", "metaclass"
            ]
            code_lower = broken_code.lower()
            for pattern in complex_patterns:
                if pattern in code_lower:
                    complexity_factors += 0.5
        
        complexity_factors = int(complexity_factors)
        
        if complexity_factors >= 6:
            return TaskComplexity.EXPERT
        elif complexity_factors >= 4:
            return TaskComplexity.COMPLEX
        elif complexity_factors >= 2:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _parse_fix_response(self, response_content: str, language: str, issue_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the fix response into structured format"""
        try:
            # Extract fixed code
            code_pattern = f'```{language}(.*?)```'
            code_matches = re.findall(code_pattern, response_content, re.DOTALL)
            
            fixed_code = ""
            if code_matches:
                fixed_code = code_matches[0].strip()
            
            # Extract explanations
            root_cause = self._extract_section(response_content, "Root Cause")
            changes_made = self._extract_section(response_content, "Changes Made")
            testing_notes = self._extract_section(response_content, "Testing Notes")
            prevention = self._extract_section(response_content, "Prevention")
            
            # Calculate fix confidence
            confidence = self._calculate_fix_confidence(fixed_code, response_content, issue_analysis)
            
            return {
                "fixed_code": fixed_code,
                "root_cause": root_cause,
                "changes_made": changes_made,
                "testing_notes": testing_notes,
                "prevention": prevention,
                "confidence": confidence,
                "language": language,
                "issue_category": issue_analysis["category"],
                "fix_timestamp": datetime.now().isoformat(),
                "raw_response": response_content
            }
            
        except Exception as e:
            logger.warning(f"⚠️  Fix parsing failed: {e}")
            return {
                "fixed_code": "",
                "root_cause": "Parse error",
                "changes_made": [],
                "testing_notes": "",
                "prevention": "",
                "confidence": 0,
                "language": language,
                "raw_response": response_content,
                "parse_error": str(e)
            }
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the response"""
        pattern = f'\\*\\*{section_name}:\\*\\*\\s*(.*?)(?=\\*\\*|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _calculate_fix_confidence(self, fixed_code: str, response_content: str, issue_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the fix"""
        confidence = 0.0
        
        # Code quality indicators
        if fixed_code:
            confidence += 0.3
            
            # Check for proper structure
            if "def " in fixed_code or "class " in fixed_code:
                confidence += 0.2
            
            # Check for error handling
            if "try:" in fixed_code or "except:" in fixed_code:
                confidence += 0.2
            
            # Check for comments/documentation
            if "#" in fixed_code or '"""' in fixed_code:
                confidence += 0.1
        
        # Response quality indicators
        if "root cause" in response_content.lower():
            confidence += 0.1
        if "changes made" in response_content.lower():
            confidence += 0.1
        if "testing" in response_content.lower():
            confidence += 0.1
        
        # Issue-specific confidence
        if issue_analysis["category"] != "unknown":
            confidence += 0.1
        
        return min(1.0, confidence)
    
    async def _validate_fix(self, fix_results: Dict[str, Any], broken_code: str, error_message: str) -> Dict[str, Any]:
        """Validate the generated fix"""
        try:
            validated_fix = {
                **fix_results,
                "validation_results": {},
                "likely_resolved": False,
                "requires_testing": True
            }
            
            fixed_code = fix_results.get("fixed_code", "")
            
            # Basic validation checks
            validation_checks = {
                "has_code": len(fixed_code) > 0,
                "has_explanation": len(fix_results.get("root_cause", "")) > 0,
                "has_changes": len(fix_results.get("changes_made", "")) > 0,
                "syntax_likely_valid": self._check_syntax_likelihood(fixed_code),
                "addresses_issue": self._check_issue_addressed(fixed_code, error_message)
            }
            
            # Calculate overall likelihood of resolution
            passed_checks = sum(validation_checks.values())
            total_checks = len(validation_checks)
            
            validated_fix["validation_results"] = validation_checks
            validated_fix["likely_resolved"] = passed_checks >= (total_checks * 0.7)
            validated_fix["validation_score"] = passed_checks / total_checks
            
            return validated_fix
            
        except Exception as e:
            logger.warning(f"⚠️  Fix validation failed: {e}")
            return {
                **fix_results,
                "validation_error": str(e),
                "likely_resolved": False,
                "requires_testing": True
            }
    
    def _check_syntax_likelihood(self, code: str) -> bool:
        """Check if code is likely to have valid syntax"""
        if not code:
            return False
        
        # Basic syntax checks
        open_brackets = code.count('(') + code.count('[') + code.count('{')
        close_brackets = code.count(')') + code.count(']') + code.count('}')
        
        return abs(open_brackets - close_brackets) <= 1
    
    def _check_issue_addressed(self, fixed_code: str, error_message: str) -> bool:
        """Check if the fix likely addresses the reported issue"""
        if not error_message:
            return True  # No specific error to check
        
        error_lower = error_message.lower()
        code_lower = fixed_code.lower()
        
        # Check for common fix patterns
        if "undefined" in error_lower or "not defined" in error_lower:
            return "def " in code_lower or "import " in code_lower
        if "syntax" in error_lower:
            return len(fixed_code) > 0
        if "type" in error_lower:
            return "isinstance" in code_lower or "type(" in code_lower
        if "key" in error_lower:
            return "get(" in code_lower or "in " in code_lower
        
        return True  # Default to optimistic
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context and recent issues from memory"""
        try:
            # Get recent code that might be broken
            code_items = self.memory_manager.search_memory(
                query="code generated error",
                memory_type=MemoryType.CODE,
                use_vector=True,
                limit=3
            )
            
            # Get recent error reports
            error_items = self.memory_manager.search_memory(
                query="error failed bug",
                memory_type=MemoryType.TASK,
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
                "recent_errors": [],
                "architecture": {},
                "similar_fixes": []
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
            
            # Extract recent errors
            for item in error_items:
                if "error" in item.metadata:
                    context["recent_errors"].append({
                        "error": item.metadata["error"],
                        "timestamp": item.created_at.isoformat()
                    })
            
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
        """Get fixer agent statistics"""
        return {
            **self.stats,
            "fix_categories": list(self.fix_categories.keys()),
            "fixes_completed": len(self.memory_manager.search_memory(
                query="fixer",
                memory_type=MemoryType.CODE,
                limit=1000
            )),
            "fix_capabilities": [
                "syntax_error_fixing",
                "runtime_error_resolution",
                "logic_bug_repair",
                "performance_optimization",
                "security_vulnerability_patching",
                "dependency_issue_resolution"
            ]
        }


def create_fixer_agent(config: Dict[str, Any]) -> FixerAgent:
    """Factory function to create fixer agent"""
    return FixerAgent(config)