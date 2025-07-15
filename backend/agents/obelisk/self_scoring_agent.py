"""
OBELISK Self-Scoring Agent
Evaluates and scores generated outputs with improvement suggestions
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import re

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class SelfScoringAgent(BaseAgent):
    """
    OBELISK Self-Scoring Agent
    
    Specializes in:
    - Quality scoring and evaluation
    - Confidence assessment
    - Improvement suggestions
    - Performance analysis
    - Comparative scoring
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="self_scoring",
            agent_type=AgentType.ANALYZER,
            description="OBELISK Self-Scoring - Evaluates and scores outputs with improvement suggestions",
            capabilities=[
                "quality_scoring",
                "confidence_assessment",
                "improvement_suggestions",
                "performance_analysis",
                "comparative_scoring",
                "objective_evaluation",
                "detailed_feedback",
                "scoring_consistency"
            ],
            model_requirements=["analysis", "reasoning", "evaluation"],
            priority=5,
            max_concurrent_tasks=3,
            timeout_seconds=300,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Scoring dimensions and criteria
        self.scoring_dimensions = {
            "quality": {
                "description": "Overall quality and correctness of the output",
                "weight": 0.3,
                "factors": ["accuracy", "completeness", "clarity", "coherence"],
                "scale": "0-10 (0=poor, 10=excellent)"
            },
            "functionality": {
                "description": "How well the output fulfills its intended purpose",
                "weight": 0.25,
                "factors": ["effectiveness", "usability", "reliability", "performance"],
                "scale": "0-10 (0=non-functional, 10=perfectly functional)"
            },
            "innovation": {
                "description": "Creativity and novelty of the approach",
                "weight": 0.2,
                "factors": ["originality", "uniqueness", "creative_solution", "breakthrough_potential"],
                "scale": "0-10 (0=conventional, 10=groundbreaking)"
            },
            "technical_merit": {
                "description": "Technical soundness and implementation quality",
                "weight": 0.15,
                "factors": ["code_quality", "architecture", "best_practices", "maintainability"],
                "scale": "0-10 (0=poor_implementation, 10=excellent_implementation)"
            },
            "user_value": {
                "description": "Value delivered to end users",
                "weight": 0.1,
                "factors": ["user_experience", "problem_solving", "accessibility", "impact"],
                "scale": "0-10 (0=no_value, 10=high_value)"
            }
        }
        
        # Confidence assessment criteria
        self.confidence_factors = {
            "completeness": {
                "description": "How complete is the evaluation",
                "indicators": ["all_aspects_covered", "sufficient_detail", "thorough_analysis"]
            },
            "objectivity": {
                "description": "How objective is the assessment",
                "indicators": ["unbiased_evaluation", "evidence_based", "consistent_criteria"]
            },
            "expertise": {
                "description": "Level of domain expertise demonstrated",
                "indicators": ["technical_accuracy", "industry_knowledge", "best_practices"]
            },
            "consistency": {
                "description": "Internal consistency of the evaluation",
                "indicators": ["logical_coherence", "aligned_scoring", "consistent_rationale"]
            }
        }
        
        # Improvement categories
        self.improvement_categories = {
            "critical": {
                "description": "Critical issues that must be addressed",
                "priority": "HIGH",
                "urgency": "IMMEDIATE",
                "impact": "SEVERE"
            },
            "significant": {
                "description": "Significant improvements that would add substantial value",
                "priority": "HIGH",
                "urgency": "SOON",
                "impact": "MAJOR"
            },
            "moderate": {
                "description": "Moderate improvements that would enhance the output",
                "priority": "MEDIUM",
                "urgency": "EVENTUALLY",
                "impact": "MODERATE"
            },
            "minor": {
                "description": "Minor improvements and polish",
                "priority": "LOW",
                "urgency": "OPTIONAL",
                "impact": "MINOR"
            },
            "enhancement": {
                "description": "Nice-to-have enhancements",
                "priority": "LOW",
                "urgency": "FUTURE",
                "impact": "MINIMAL"
            }
        }
        
        # Content type scoring templates
        self.content_type_templates = {
            "code": {
                "specific_criteria": ["syntax_correctness", "logic_soundness", "error_handling", "documentation"],
                "quality_indicators": ["runs_without_errors", "handles_edge_cases", "follows_conventions", "well_documented"],
                "common_issues": ["syntax_errors", "logical_flaws", "missing_error_handling", "poor_documentation"]
            },
            "architecture": {
                "specific_criteria": ["scalability", "maintainability", "security", "performance"],
                "quality_indicators": ["well_designed_components", "clear_separation", "secure_by_design", "performance_optimized"],
                "common_issues": ["tight_coupling", "security_vulnerabilities", "performance_bottlenecks", "unclear_design"]
            },
            "ideas": {
                "specific_criteria": ["originality", "feasibility", "impact", "clarity"],
                "quality_indicators": ["novel_approach", "implementable", "high_impact", "clearly_expressed"],
                "common_issues": ["generic_ideas", "infeasible_concepts", "low_impact", "unclear_description"]
            },
            "tests": {
                "specific_criteria": ["coverage", "quality", "maintainability", "reliability"],
                "quality_indicators": ["comprehensive_coverage", "good_test_design", "maintainable_tests", "reliable_results"],
                "common_issues": ["poor_coverage", "brittle_tests", "hard_to_maintain", "unreliable_results"]
            }
        }
        
        logger.info(f"📊 {self.metadata.name} initialized with comprehensive scoring capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for self-scoring agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires scoring or evaluation
        scoring_keywords = [
            "score", "evaluate", "assess", "rate", "measure", "analyze",
            "grade", "rank", "judge", "appraise", "review", "quality"
        ]
        
        return any(keyword in content for keyword in scoring_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scoring and evaluation task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"score_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"📊 Starting scoring evaluation: {task_id}")
            
            # Extract task parameters
            content_to_evaluate = task.get("content", "")
            content_type = task.get("content_type", "general")
            evaluation_criteria = task.get("criteria", list(self.scoring_dimensions.keys()))
            context = task.get("context", {})
            
            # Perform comprehensive evaluation
            scoring_result = await self._perform_comprehensive_scoring(
                content=content_to_evaluate,
                content_type=content_type,
                evaluation_criteria=evaluation_criteria,
                context=context
            )
            
            # Store results in memory
            await self._store_scoring_results(
                task_id=task_id,
                scoring_result=scoring_result,
                content_type=content_type,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "scoring_evaluation": scoring_result,
                "content_type": content_type,
                "evaluation_criteria": evaluation_criteria,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"score_{task_id}",
                "tokens_used": scoring_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Scoring evaluation completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Scoring evaluation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _perform_comprehensive_scoring(
        self,
        content: str,
        content_type: str,
        evaluation_criteria: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive scoring and evaluation"""
        
        # Get content type template
        template = self.content_type_templates.get(content_type, self.content_type_templates["code"])
        
        # Create scoring prompt
        scoring_prompt = self._create_scoring_prompt(
            content=content,
            content_type=content_type,
            evaluation_criteria=evaluation_criteria,
            template=template,
            context=context
        )
        
        # Perform scoring using consistent model settings
        try:
            response = await self.orchestrator.generate_response(
                prompt=scoring_prompt,
                model_preference=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
                temperature=0.1,  # Low temperature for consistent scoring
                max_tokens=4000
            )
            
            # Parse and structure scoring response
            scoring_result = await self._parse_scoring_response(
                response=response,
                content=content,
                content_type=content_type,
                evaluation_criteria=evaluation_criteria
            )
            
            return scoring_result
            
        except Exception as e:
            logger.error(f"❌ Scoring evaluation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_score": self._create_fallback_score(content, content_type)
            }
    
    def _create_scoring_prompt(
        self,
        content: str,
        content_type: str,
        evaluation_criteria: List[str],
        template: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed scoring prompt"""
        
        criteria_details = []
        for criterion in evaluation_criteria:
            if criterion in self.scoring_dimensions:
                dim = self.scoring_dimensions[criterion]
                criteria_details.append(f"""
{criterion.upper()}:
- Description: {dim['description']}
- Weight: {dim['weight']}
- Factors: {dim['factors']}
- Scale: {dim['scale']}
""")
        
        return f"""
You are an expert evaluator tasked with providing objective, detailed scoring of the provided content. Your evaluation should be thorough, fair, and constructive.

CONTENT TO EVALUATE:
{content}

CONTENT TYPE: {content_type}

EVALUATION CRITERIA:
{chr(10).join(criteria_details)}

CONTENT-SPECIFIC CONSIDERATIONS:
- Specific Criteria: {template.get('specific_criteria', [])}
- Quality Indicators: {template.get('quality_indicators', [])}
- Common Issues: {template.get('common_issues', [])}

CONTEXT:
{context}

SCORING REQUIREMENTS:
1. Evaluate objectively using consistent criteria
2. Provide specific, actionable feedback
3. Score each dimension on the specified scale
4. Assess confidence level in your evaluation
5. Suggest concrete improvements
6. Maintain consistency across all dimensions

EVALUATION PROCESS:
1. ANALYZE the content thoroughly
2. ASSESS each evaluation criterion
3. IDENTIFY strengths and weaknesses
4. CALCULATE scores based on evidence
5. DETERMINE confidence level
6. FORMULATE improvement suggestions

Please provide your evaluation in the following JSON format:
{{
    "overall_assessment": {{
        "overall_score": "0-10 (weighted average)",
        "overall_grade": "A|B|C|D|F",
        "summary": "brief overall assessment",
        "strengths": ["key strength 1", "key strength 2", "key strength 3"],
        "weaknesses": ["key weakness 1", "key weakness 2", "key weakness 3"],
        "recommendation": "EXCELLENT|GOOD|SATISFACTORY|NEEDS_IMPROVEMENT|POOR"
    }},
    "detailed_scores": {{
        "quality": {{
            "score": "0-10",
            "rationale": "detailed explanation of score",
            "evidence": ["specific evidence 1", "specific evidence 2"],
            "improvement_potential": "0-10 (how much could be improved)"
        }},
        "functionality": {{
            "score": "0-10",
            "rationale": "detailed explanation of score",
            "evidence": ["specific evidence 1", "specific evidence 2"],
            "improvement_potential": "0-10 (how much could be improved)"
        }},
        "innovation": {{
            "score": "0-10",
            "rationale": "detailed explanation of score",
            "evidence": ["specific evidence 1", "specific evidence 2"],
            "improvement_potential": "0-10 (how much could be improved)"
        }},
        "technical_merit": {{
            "score": "0-10",
            "rationale": "detailed explanation of score",
            "evidence": ["specific evidence 1", "specific evidence 2"],
            "improvement_potential": "0-10 (how much could be improved)"
        }},
        "user_value": {{
            "score": "0-10",
            "rationale": "detailed explanation of score",
            "evidence": ["specific evidence 1", "specific evidence 2"],
            "improvement_potential": "0-10 (how much could be improved)"
        }}
    }},
    "confidence_assessment": {{
        "confidence_level": "0-100 (percentage)",
        "confidence_factors": {{
            "completeness": "0-100 (how complete is the evaluation)",
            "objectivity": "0-100 (how objective is the assessment)",
            "expertise": "0-100 (level of domain expertise)",
            "consistency": "0-100 (internal consistency)"
        }},
        "limitations": ["limitation 1", "limitation 2"],
        "assumptions": ["assumption 1", "assumption 2"]
    }},
    "improvement_suggestions": [
        {{
            "category": "critical|significant|moderate|minor|enhancement",
            "area": "quality|functionality|innovation|technical_merit|user_value",
            "description": "detailed improvement description",
            "rationale": "why this improvement is needed",
            "implementation": "how to implement this improvement",
            "priority": "HIGH|MEDIUM|LOW",
            "effort": "LOW|MEDIUM|HIGH",
            "impact": "LOW|MEDIUM|HIGH"
        }}
    ],
    "comparative_analysis": {{
        "benchmark_comparison": "how does this compare to typical outputs",
        "industry_standards": "comparison to industry standards",
        "best_practices": "alignment with best practices",
        "competitive_analysis": "comparison to alternatives"
    }},
    "next_steps": [
        "immediate actionable steps",
        "short-term improvements",
        "long-term enhancements",
        "validation recommendations"
    ]
}}

Be thorough, objective, and constructive in your evaluation. Provide specific examples and actionable feedback.
"""
    
    async def _parse_scoring_response(
        self,
        response: str,
        content: str,
        content_type: str,
        evaluation_criteria: List[str]
    ) -> Dict[str, Any]:
        """Parse and validate scoring response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            scoring_data = json.loads(json_str)
            
            # Calculate weighted overall score
            overall_score = self._calculate_weighted_score(scoring_data.get("detailed_scores", {}))
            
            # Validate and enhance scoring data
            scoring_result = {
                "success": True,
                "content_type": content_type,
                "evaluation_criteria": evaluation_criteria,
                "evaluated_at": datetime.now().isoformat(),
                "overall_assessment": scoring_data.get("overall_assessment", {}),
                "detailed_scores": scoring_data.get("detailed_scores", {}),
                "confidence_assessment": scoring_data.get("confidence_assessment", {}),
                "improvement_suggestions": scoring_data.get("improvement_suggestions", []),
                "comparative_analysis": scoring_data.get("comparative_analysis", {}),
                "next_steps": scoring_data.get("next_steps", []),
                "metadata": {
                    "calculated_overall_score": overall_score,
                    "total_improvement_suggestions": len(scoring_data.get("improvement_suggestions", [])),
                    "confidence_level": scoring_data.get("confidence_assessment", {}).get("confidence_level", 0),
                    "critical_improvements": len([
                        s for s in scoring_data.get("improvement_suggestions", [])
                        if s.get("category") == "critical"
                    ]),
                    "high_priority_improvements": len([
                        s for s in scoring_data.get("improvement_suggestions", [])
                        if s.get("priority") == "HIGH"
                    ])
                },
                "tokens_used": len(response.split())
            }
            
            return scoring_result
            
        except Exception as e:
            logger.error(f"❌ Scoring parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse scoring response: {str(e)}",
                "raw_response": response,
                "fallback_score": self._create_fallback_score(content, content_type)
            }
    
    def _calculate_weighted_score(self, detailed_scores: Dict[str, Any]) -> float:
        """Calculate weighted overall score based on dimension weights"""
        
        total_score = 0.0
        total_weight = 0.0
        
        for dimension, weight_info in self.scoring_dimensions.items():
            if dimension in detailed_scores:
                try:
                    score = float(detailed_scores[dimension].get("score", 0))
                    weight = weight_info["weight"]
                    total_score += score * weight
                    total_weight += weight
                except (ValueError, TypeError):
                    pass
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _create_fallback_score(self, content: str, content_type: str) -> Dict[str, Any]:
        """Create basic fallback score"""
        
        # Basic content analysis
        content_length = len(content.split())
        has_structure = any(marker in content for marker in ["def ", "class ", "function", "component"])
        
        # Basic scoring based on content characteristics
        base_score = 5.0  # Start with average
        
        if content_length > 100:
            base_score += 1.0  # Bonus for substantial content
        if has_structure:
            base_score += 1.0  # Bonus for structured content
        if content_length > 500:
            base_score += 0.5  # Bonus for comprehensive content
        
        base_score = min(base_score, 10.0)  # Cap at 10
        
        return {
            "overall_assessment": {
                "overall_score": base_score,
                "overall_grade": self._score_to_grade(base_score),
                "summary": f"Basic evaluation of {content_type} content",
                "strengths": ["Content provided", "Appropriate length" if content_length > 50 else "Content present"],
                "weaknesses": ["Limited analysis available", "Manual review recommended"],
                "recommendation": "SATISFACTORY" if base_score >= 6.0 else "NEEDS_IMPROVEMENT"
            },
            "detailed_scores": {
                dimension: {
                    "score": base_score,
                    "rationale": f"Basic assessment - manual review recommended",
                    "evidence": ["Content analysis limited"],
                    "improvement_potential": 10 - base_score
                }
                for dimension in self.scoring_dimensions.keys()
            },
            "confidence_assessment": {
                "confidence_level": 30,  # Low confidence for fallback
                "confidence_factors": {
                    "completeness": 20,
                    "objectivity": 40,
                    "expertise": 20,
                    "consistency": 40
                },
                "limitations": ["Automated analysis only", "Limited domain knowledge"],
                "assumptions": ["Standard quality expectations", "Basic functionality assumed"]
            },
            "improvement_suggestions": [
                {
                    "category": "significant",
                    "area": "quality",
                    "description": "Conduct thorough manual review",
                    "rationale": "Automated analysis has limitations",
                    "implementation": "Have domain expert review the content",
                    "priority": "HIGH",
                    "effort": "MEDIUM",
                    "impact": "HIGH"
                }
            ],
            "comparative_analysis": {
                "benchmark_comparison": "Unable to compare automatically",
                "industry_standards": "Manual review needed",
                "best_practices": "Review against established practices",
                "competitive_analysis": "Manual comparison recommended"
            },
            "next_steps": [
                "Conduct manual expert review",
                "Compare against quality standards",
                "Implement specific improvements",
                "Validate improvements with testing"
            ]
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 9.0:
            return "A"
        elif score >= 7.0:
            return "B"
        elif score >= 5.0:
            return "C"
        elif score >= 3.0:
            return "D"
        else:
            return "F"
    
    async def _store_scoring_results(
        self,
        task_id: str,
        scoring_result: Dict[str, Any],
        content_type: str,
        session_id: Optional[str] = None
    ):
        """Store scoring results in memory"""
        
        content = f"""
Self-Scoring Evaluation Results

Task ID: {task_id}
Content Type: {content_type}
Evaluated: {datetime.now().isoformat()}

Scoring Summary:
- Success: {scoring_result.get('success', False)}
- Overall Score: {scoring_result.get('metadata', {}).get('calculated_overall_score', 0):.1f}/10
- Confidence Level: {scoring_result.get('metadata', {}).get('confidence_level', 0)}%
- Total Improvement Suggestions: {scoring_result.get('metadata', {}).get('total_improvement_suggestions', 0)}
- Critical Improvements: {scoring_result.get('metadata', {}).get('critical_improvements', 0)}
- High Priority Improvements: {scoring_result.get('metadata', {}).get('high_priority_improvements', 0)}

Full Scoring Result:
{json.dumps(scoring_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.TASK,
            priority=MemoryPriority.HIGH,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "content_type": content_type,
                "scoring_success": scoring_result.get("success", False),
                "overall_score": scoring_result.get("metadata", {}).get("calculated_overall_score", 0),
                "confidence_level": scoring_result.get("metadata", {}).get("confidence_level", 0),
                "total_improvement_suggestions": scoring_result.get("metadata", {}).get("total_improvement_suggestions", 0),
                "critical_improvements": scoring_result.get("metadata", {}).get("critical_improvements", 0)
            },
            tags=["scoring", "evaluation", "assessment", "obelisk", "self_scoring"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "scoring_dimensions": list(self.scoring_dimensions.keys()),
            "content_types": list(self.content_type_templates.keys()),
            "improvement_categories": list(self.improvement_categories.keys()),
            "confidence_factors": list(self.confidence_factors.keys()),
            "scoring_features": [
                "Objective quality scoring",
                "Confidence assessment",
                "Improvement suggestions",
                "Comparative analysis",
                "Detailed feedback",
                "Consistent evaluation",
                "Multi-dimensional scoring",
                "Actionable recommendations"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_self_scoring_agent(config: Dict[str, Any]) -> SelfScoringAgent:
    """Factory function to create Self-Scoring Agent"""
    return SelfScoringAgent(config)