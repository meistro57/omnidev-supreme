"""
OBELISK Creativity Agent
Reviews and refines brainstormed ideas with creative direction
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class CreativityAgent(BaseAgent):
    """
    OBELISK Creativity Agent
    
    Specializes in:
    - Creative idea refinement
    - Concept enhancement
    - Novel angle identification
    - Creative direction and feedback
    - Artistic and aesthetic improvements
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="creativity_agent",
            agent_type=AgentType.ANALYZER,
            description="OBELISK Creativity Agent - Reviews and refines ideas with creative direction",
            capabilities=[
                "creative_idea_refinement",
                "concept_enhancement",
                "novel_angle_identification",
                "creative_direction",
                "artistic_feedback",
                "aesthetic_improvements",
                "narrative_development",
                "user_experience_creativity"
            ],
            model_requirements=["creativity", "analysis", "reasoning"],
            priority=6,
            max_concurrent_tasks=2,
            timeout_seconds=500,
            retry_count=3
        )
        
        super().__init__(metadata, config)
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Creative refinement frameworks
        self.refinement_frameworks = {
            "creative_synthesis": {
                "name": "Creative Synthesis",
                "description": "Combine and enhance ideas through creative synthesis",
                "dimensions": ["originality", "usefulness", "surprise", "elegance"],
                "techniques": ["analogical_thinking", "metaphorical_reasoning", "pattern_recognition", "concept_blending"]
            },
            "design_critique": {
                "name": "Design Critique",
                "description": "Evaluate and improve design aspects",
                "dimensions": ["functionality", "aesthetics", "usability", "innovation"],
                "techniques": ["heuristic_evaluation", "aesthetic_analysis", "user_flow_review", "design_principles"]
            },
            "narrative_enhancement": {
                "name": "Narrative Enhancement",
                "description": "Improve storytelling and user experience narrative",
                "dimensions": ["engagement", "clarity", "emotional_impact", "memorability"],
                "techniques": ["story_structure", "character_development", "emotional_arc", "user_journey"]
            },
            "innovation_amplification": {
                "name": "Innovation Amplification",
                "description": "Enhance innovative aspects of ideas",
                "dimensions": ["novelty", "impact", "feasibility", "scalability"],
                "techniques": ["disruptive_thinking", "trend_extrapolation", "technology_fusion", "market_disruption"]
            }
        }
        
        # Creative evaluation criteria
        self.evaluation_criteria = {
            "originality": {
                "description": "How novel and unique is the idea?",
                "factors": ["uniqueness", "unexpectedness", "innovation_level", "differentiation"],
                "scale": "1-10 (1=common, 10=groundbreaking)"
            },
            "aesthetic_appeal": {
                "description": "How visually and experientially appealing is the concept?",
                "factors": ["visual_design", "user_experience", "emotional_response", "beauty"],
                "scale": "1-10 (1=unappealing, 10=stunning)"
            },
            "emotional_resonance": {
                "description": "How well does the idea connect emotionally with users?",
                "factors": ["emotional_impact", "user_empathy", "personal_relevance", "inspiration"],
                "scale": "1-10 (1=disconnected, 10=deeply_moving)"
            },
            "creative_potential": {
                "description": "How much creative potential does the idea have?",
                "factors": ["expandability", "adaptability", "creative_possibilities", "inspiration_catalyst"],
                "scale": "1-10 (1=limited, 10=unlimited)"
            },
            "narrative_strength": {
                "description": "How compelling is the story or narrative?",
                "factors": ["story_clarity", "character_development", "plot_engagement", "message_strength"],
                "scale": "1-10 (1=weak, 10=compelling)"
            }
        }
        
        # Creative enhancement techniques
        self.enhancement_techniques = {
            "amplification": "Amplify the most interesting aspects of the idea",
            "transformation": "Transform the idea into something more compelling",
            "synthesis": "Combine elements in creative ways",
            "metaphor": "Use metaphors to add depth and meaning",
            "contrast": "Create interesting contrasts and tensions",
            "surprise": "Add unexpected elements that delight users",
            "emotion": "Enhance emotional connection and impact",
            "simplification": "Simplify to achieve elegant clarity",
            "elaboration": "Add rich details and layers",
            "reframing": "Present the idea from a fresh perspective"
        }
        
        logger.info(f"🎨 {self.metadata.name} initialized with creative refinement capabilities")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for creativity agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires creative refinement
        creativity_keywords = [
            "creative", "refine", "enhance", "improve", "polish", "artistic",
            "aesthetic", "design", "visual", "experience", "beauty", "elegant"
        ]
        
        return any(keyword in content for keyword in creativity_keywords)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute creative refinement task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"creative_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"🎨 Starting creative refinement: {task_id}")
            
            # Extract task parameters
            ideas_to_refine = task.get("ideas_to_refine", "")
            project_name = task.get("project_name", "Project")
            refinement_framework = task.get("refinement_framework", "creative_synthesis")
            focus_areas = task.get("focus_areas", ["originality", "aesthetic_appeal"])
            context = task.get("context", {})
            
            # Perform creative refinement
            refinement_result = await self._refine_ideas_creatively(
                ideas_text=ideas_to_refine,
                project_name=project_name,
                refinement_framework=refinement_framework,
                focus_areas=focus_areas,
                context=context
            )
            
            # Store results in memory
            await self._store_refinement_results(
                task_id=task_id,
                refinement_result=refinement_result,
                project_name=project_name,
                refinement_framework=refinement_framework,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "creative_refinement": refinement_result,
                "project_name": project_name,
                "refinement_framework": refinement_framework,
                "focus_areas": focus_areas,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"creative_{task_id}",
                "tokens_used": refinement_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Creative refinement completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Creative refinement failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _refine_ideas_creatively(
        self,
        ideas_text: str,
        project_name: str,
        refinement_framework: str,
        focus_areas: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Refine ideas using creative enhancement techniques"""
        
        # Get refinement framework
        framework = self.refinement_frameworks.get(refinement_framework, self.refinement_frameworks["creative_synthesis"])
        
        # Create creative refinement prompt
        refinement_prompt = self._create_refinement_prompt(
            ideas_text=ideas_text,
            project_name=project_name,
            framework=framework,
            focus_areas=focus_areas,
            context=context
        )
        
        # Refine ideas using creative model settings
        try:
            response = await self.orchestrator.generate_response(
                prompt=refinement_prompt,
                model_preference=["claude-3.5-sonnet", "gpt-4", "gpt-3.5-turbo"],
                temperature=0.8,  # High creativity with some consistency
                max_tokens=4000
            )
            
            # Parse and structure refinement response
            refinement_result = await self._parse_refinement_response(
                response=response,
                project_name=project_name,
                framework=framework,
                focus_areas=focus_areas
            )
            
            return refinement_result
            
        except Exception as e:
            logger.error(f"❌ Creative refinement failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_refinement": self._create_fallback_refinement(ideas_text, project_name)
            }
    
    def _create_refinement_prompt(
        self,
        ideas_text: str,
        project_name: str,
        framework: Dict[str, Any],
        focus_areas: List[str],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed creative refinement prompt"""
        
        criteria_descriptions = []
        for area in focus_areas:
            if area in self.evaluation_criteria:
                criteria = self.evaluation_criteria[area]
                criteria_descriptions.append(f"""
{area.upper()}:
- {criteria['description']}
- Factors: {criteria['factors']}
- Scale: {criteria['scale']}
""")
        
        return f"""
You are a creative director and innovation consultant tasked with reviewing and enhancing brainstormed ideas. Your goal is to provide creative direction that elevates the concepts to their full potential.

PROJECT: {project_name}

IDEAS TO REFINE:
{ideas_text}

REFINEMENT FRAMEWORK: {framework['name']}
{framework['description']}

FRAMEWORK DIMENSIONS:
{chr(10).join(f"- {dim}" for dim in framework['dimensions'])}

FRAMEWORK TECHNIQUES:
{chr(10).join(f"- {tech}" for tech in framework['techniques'])}

FOCUS AREAS FOR REFINEMENT:
{chr(10).join(criteria_descriptions)}

CONTEXT:
{context}

CREATIVE ENHANCEMENT TECHNIQUES:
{chr(10).join(f"- {name}: {desc}" for name, desc in self.enhancement_techniques.items())}

CREATIVE REFINEMENT REQUIREMENTS:
1. EVALUATE each idea across the focus areas
2. ENHANCE ideas using creative techniques
3. SUGGEST novel angles and perspectives
4. IMPROVE aesthetic and experiential qualities
5. AMPLIFY emotional resonance and impact
6. IDENTIFY creative potential and possibilities
7. PROVIDE specific, actionable creative direction

CREATIVE ANALYSIS PROCESS:
1. ASSESS current creative strengths and weaknesses
2. IDENTIFY opportunities for enhancement
3. APPLY creative techniques to improve concepts
4. SYNTHESIZE ideas into more compelling forms
5. SUGGEST implementation approaches that preserve creativity

Please provide your creative refinement in the following JSON format:
{{
    "creative_analysis": {{
        "project_name": "{project_name}",
        "refinement_framework": "{framework['name']}",
        "analysis_date": "current date",
        "original_ideas_count": "count of original ideas",
        "refined_ideas": [
            {{
                "original_idea": "original idea description",
                "refined_concept": "enhanced version of the idea",
                "creative_enhancements": [
                    {{
                        "enhancement_type": "amplification|transformation|synthesis|etc",
                        "description": "what was enhanced",
                        "creative_technique": "technique used",
                        "impact": "expected impact of enhancement"
                    }}
                ],
                "creative_evaluation": {{
                    "originality": {{
                        "score": "1-10",
                        "rationale": "why this score",
                        "improvement_suggestions": ["suggestion1", "suggestion2"]
                    }},
                    "aesthetic_appeal": {{
                        "score": "1-10",
                        "rationale": "why this score",
                        "improvement_suggestions": ["suggestion1", "suggestion2"]
                    }},
                    "emotional_resonance": {{
                        "score": "1-10",
                        "rationale": "why this score",
                        "improvement_suggestions": ["suggestion1", "suggestion2"]
                    }},
                    "creative_potential": {{
                        "score": "1-10",
                        "rationale": "why this score",
                        "improvement_suggestions": ["suggestion1", "suggestion2"]
                    }}
                }},
                "novel_angles": [
                    {{
                        "angle": "new perspective or approach",
                        "description": "detailed description",
                        "creative_value": "why this angle adds value",
                        "implementation_idea": "how to implement this angle"
                    }}
                ],
                "aesthetic_improvements": [
                    {{
                        "aspect": "visual|experiential|emotional|narrative",
                        "current_state": "current aesthetic quality",
                        "improvement": "suggested improvement",
                        "rationale": "why this improves aesthetics"
                    }}
                ]
            }}
        ]
    }},
    "creative_synthesis": [
        {{
            "synthesis_name": "name for combined concept",
            "description": "creative combination of ideas",
            "component_ideas": ["idea1", "idea2", "idea3"],
            "creative_synergy": "how ideas enhance each other creatively",
            "unique_value": "what makes this synthesis special",
            "aesthetic_vision": "overall aesthetic and experiential vision"
        }}
    ],
    "creative_direction": {{
        "overall_theme": "overarching creative theme",
        "aesthetic_philosophy": "guiding aesthetic principles",
        "emotional_journey": "intended emotional experience",
        "creative_priorities": ["priority1", "priority2", "priority3"],
        "implementation_guidelines": [
            {{
                "guideline": "creative guideline",
                "rationale": "why this guideline is important",
                "examples": ["example1", "example2"]
            }}
        ]
    }},
    "innovation_opportunities": [
        {{
            "opportunity": "creative innovation opportunity",
            "description": "detailed description",
            "creative_potential": "HIGH|MEDIUM|LOW",
            "uniqueness_factor": "what makes this uniquely creative",
            "inspiration_sources": ["source1", "source2"],
            "implementation_challenges": ["challenge1", "challenge2"]
        }}
    ],
    "next_creative_steps": [
        "immediate creative actions",
        "prototype and experimentation suggestions",
        "creative validation approaches",
        "artistic exploration recommendations"
    ]
}}

Focus on elevating the creative quality and impact of the ideas while maintaining their practical value.
"""
    
    async def _parse_refinement_response(
        self,
        response: str,
        project_name: str,
        framework: Dict[str, Any],
        focus_areas: List[str]
    ) -> Dict[str, Any]:
        """Parse and validate creative refinement response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            refinement_data = json.loads(json_str)
            
            # Count refinements
            refined_ideas = refinement_data.get("creative_analysis", {}).get("refined_ideas", [])
            total_enhancements = sum(
                len(idea.get("creative_enhancements", []))
                for idea in refined_ideas
            )
            
            # Validate and enhance refinement data
            refinement_result = {
                "success": True,
                "project_name": project_name,
                "refinement_framework": framework['name'],
                "focus_areas": focus_areas,
                "refined_at": datetime.now().isoformat(),
                "creative_analysis": refinement_data.get("creative_analysis", {}),
                "creative_synthesis": refinement_data.get("creative_synthesis", []),
                "creative_direction": refinement_data.get("creative_direction", {}),
                "innovation_opportunities": refinement_data.get("innovation_opportunities", []),
                "next_creative_steps": refinement_data.get("next_creative_steps", []),
                "metadata": {
                    "refined_ideas_count": len(refined_ideas),
                    "total_enhancements": total_enhancements,
                    "synthesis_concepts": len(refinement_data.get("creative_synthesis", [])),
                    "innovation_opportunities": len(refinement_data.get("innovation_opportunities", [])),
                    "average_creativity_score": self._calculate_average_creativity_score(refined_ideas)
                },
                "tokens_used": len(response.split())
            }
            
            return refinement_result
            
        except Exception as e:
            logger.error(f"❌ Creative refinement parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse creative refinement: {str(e)}",
                "raw_response": response,
                "fallback_refinement": self._create_fallback_refinement(response, project_name)
            }
    
    def _calculate_average_creativity_score(self, refined_ideas: List[Dict[str, Any]]) -> float:
        """Calculate average creativity score across all refined ideas"""
        
        if not refined_ideas:
            return 0.0
        
        total_score = 0.0
        score_count = 0
        
        for idea in refined_ideas:
            evaluation = idea.get("creative_evaluation", {})
            for criterion in ["originality", "aesthetic_appeal", "emotional_resonance", "creative_potential"]:
                if criterion in evaluation:
                    try:
                        score = float(evaluation[criterion].get("score", 0))
                        total_score += score
                        score_count += 1
                    except (ValueError, TypeError):
                        pass
        
        return total_score / score_count if score_count > 0 else 0.0
    
    def _create_fallback_refinement(self, ideas_text: str, project_name: str) -> Dict[str, Any]:
        """Create basic fallback refinement"""
        
        return {
            "creative_analysis": {
                "project_name": project_name,
                "refinement_framework": "Basic creative review",
                "analysis_date": datetime.now().isoformat(),
                "original_ideas_count": "multiple",
                "refined_ideas": [
                    {
                        "original_idea": "Original concepts from brainstorming",
                        "refined_concept": "Enhanced version focusing on user experience and aesthetic appeal",
                        "creative_enhancements": [
                            {
                                "enhancement_type": "amplification",
                                "description": "Amplified the most compelling aspects",
                                "creative_technique": "Focus enhancement",
                                "impact": "Increased clarity and impact"
                            }
                        ],
                        "creative_evaluation": {
                            "originality": {
                                "score": "7",
                                "rationale": "Shows creative thinking with room for more innovation",
                                "improvement_suggestions": ["Explore more unconventional approaches", "Add surprising elements"]
                            },
                            "aesthetic_appeal": {
                                "score": "6",
                                "rationale": "Good foundation but could be more visually compelling",
                                "improvement_suggestions": ["Enhance visual design", "Improve user experience flow"]
                            },
                            "emotional_resonance": {
                                "score": "6",
                                "rationale": "Some emotional connection but could be stronger",
                                "improvement_suggestions": ["Add personal relevance", "Strengthen emotional story"]
                            },
                            "creative_potential": {
                                "score": "7",
                                "rationale": "Good potential for creative expansion",
                                "improvement_suggestions": ["Explore variations", "Add interactive elements"]
                            }
                        },
                        "novel_angles": [
                            {
                                "angle": "User-centric innovation",
                                "description": "Focus on solving real user problems in creative ways",
                                "creative_value": "Creates meaningful user connections",
                                "implementation_idea": "Develop user personas and journey maps"
                            }
                        ],
                        "aesthetic_improvements": [
                            {
                                "aspect": "visual",
                                "current_state": "Functional but basic",
                                "improvement": "Add visual hierarchy and engaging design elements",
                                "rationale": "Better visual design improves user engagement"
                            }
                        ]
                    }
                ]
            },
            "creative_synthesis": [
                {
                    "synthesis_name": "Enhanced User Experience",
                    "description": "Combination of functional improvements with aesthetic enhancements",
                    "component_ideas": ["Core functionality", "Visual design", "User experience"],
                    "creative_synergy": "Function and beauty work together to create compelling experience",
                    "unique_value": "Balanced approach to both utility and delight",
                    "aesthetic_vision": "Clean, intuitive, and emotionally engaging interface"
                }
            ],
            "creative_direction": {
                "overall_theme": "Human-centered innovation",
                "aesthetic_philosophy": "Form follows function, but both serve the user",
                "emotional_journey": "From curiosity to understanding to satisfaction",
                "creative_priorities": ["User empathy", "Aesthetic coherence", "Innovative solutions"],
                "implementation_guidelines": [
                    {
                        "guideline": "Maintain user focus throughout design process",
                        "rationale": "Ensures solutions remain relevant and valuable",
                        "examples": ["User testing", "Persona development", "Journey mapping"]
                    }
                ]
            },
            "innovation_opportunities": [
                {
                    "opportunity": "Creative technology integration",
                    "description": "Explore how emerging technologies can enhance creativity",
                    "creative_potential": "MEDIUM",
                    "uniqueness_factor": "Novel application of existing technologies",
                    "inspiration_sources": ["Technology trends", "User behavior research"],
                    "implementation_challenges": ["Technical complexity", "User adoption"]
                }
            ],
            "next_creative_steps": [
                "Develop creative prototypes",
                "Test ideas with users",
                "Iterate based on feedback",
                "Explore visual design options"
            ]
        }
    
    async def _store_refinement_results(
        self,
        task_id: str,
        refinement_result: Dict[str, Any],
        project_name: str,
        refinement_framework: str,
        session_id: Optional[str] = None
    ):
        """Store creative refinement results in memory"""
        
        content = f"""
Creative Refinement Results

Task ID: {task_id}
Project: {project_name}
Framework: {refinement_framework}
Refined: {datetime.now().isoformat()}

Refinement Summary:
- Success: {refinement_result.get('success', False)}
- Refined Ideas: {refinement_result.get('metadata', {}).get('refined_ideas_count', 0)}
- Total Enhancements: {refinement_result.get('metadata', {}).get('total_enhancements', 0)}
- Synthesis Concepts: {refinement_result.get('metadata', {}).get('synthesis_concepts', 0)}
- Innovation Opportunities: {refinement_result.get('metadata', {}).get('innovation_opportunities', 0)}
- Average Creativity Score: {refinement_result.get('metadata', {}).get('average_creativity_score', 0):.1f}/10

Full Refinement Result:
{json.dumps(refinement_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.TASK,
            priority=MemoryPriority.MEDIUM,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "project_name": project_name,
                "refinement_framework": refinement_framework,
                "refinement_success": refinement_result.get("success", False),
                "refined_ideas_count": refinement_result.get("metadata", {}).get("refined_ideas_count", 0),
                "total_enhancements": refinement_result.get("metadata", {}).get("total_enhancements", 0),
                "average_creativity_score": refinement_result.get("metadata", {}).get("average_creativity_score", 0)
            },
            tags=["creativity", "refinement", "enhancement", "obelisk", "creativity_agent"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "refinement_frameworks": list(self.refinement_frameworks.keys()),
            "evaluation_criteria": list(self.evaluation_criteria.keys()),
            "enhancement_techniques": list(self.enhancement_techniques.keys()),
            "creativity_features": [
                "Creative idea refinement",
                "Aesthetic enhancement",
                "Emotional resonance improvement",
                "Novel angle identification",
                "Creative synthesis",
                "Innovation amplification",
                "Narrative development",
                "Design critique"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_creativity_agent(config: Dict[str, Any]) -> CreativityAgent:
    """Factory function to create Creativity Agent"""
    return CreativityAgent(config)