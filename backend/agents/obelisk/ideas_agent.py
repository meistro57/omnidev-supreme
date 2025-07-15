"""
OBELISK Ideas Agent
Brainstorms creative features and improvements for software projects
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..base_agent import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator

logger = logging.getLogger(__name__)


class IdeasAgent(BaseAgent):
    """
    OBELISK Ideas Agent
    
    Specializes in:
    - Creative feature brainstorming
    - Innovation suggestions
    - Enhancement recommendations
    - Problem-solving ideation
    - Technology exploration
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize metadata
        metadata = AgentMetadata(
            name="ideas_agent",
            agent_type=AgentType.ANALYZER,
            description="OBELISK Ideas Agent - Brainstorms creative features and improvements",
            capabilities=[
                "creative_feature_brainstorming",
                "innovation_suggestions",
                "enhancement_recommendations",
                "problem_solving_ideation",
                "technology_exploration",
                "user_experience_improvements",
                "business_value_analysis",
                "trend_identification"
            ],
            model_requirements=["reasoning", "creativity", "analysis"],
            priority=6,
            max_concurrent_tasks=3,
            timeout_seconds=600,
            retry_count=3
        )
        
        super().__init__(metadata)
        
        self.config = config
        self.obelisk_config = config.get("obelisk", {})
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Idea categories and frameworks
        self.idea_categories = {
            "user_experience": {
                "focus": "Improving user interaction and satisfaction",
                "aspects": ["usability", "accessibility", "performance", "aesthetics", "personalization"],
                "techniques": ["user_journey_mapping", "persona_development", "a_b_testing", "user_feedback"]
            },
            "functionality": {
                "focus": "Enhancing core features and capabilities",
                "aspects": ["new_features", "feature_enhancement", "automation", "integration", "customization"],
                "techniques": ["feature_prioritization", "use_case_analysis", "competitive_analysis", "mvp_planning"]
            },
            "technical": {
                "focus": "Improving technical architecture and performance",
                "aspects": ["scalability", "performance", "security", "maintainability", "reliability"],
                "techniques": ["architecture_review", "performance_profiling", "security_audit", "code_quality"]
            },
            "business": {
                "focus": "Adding business value and market advantages",
                "aspects": ["monetization", "user_acquisition", "retention", "analytics", "compliance"],
                "techniques": ["business_model_analysis", "market_research", "competitor_analysis", "roi_calculation"]
            },
            "innovation": {
                "focus": "Exploring cutting-edge technologies and approaches",
                "aspects": ["emerging_tech", "ai_integration", "automation", "novel_approaches", "future_trends"],
                "techniques": ["technology_scouting", "trend_analysis", "prototype_development", "proof_of_concept"]
            }
        }
        
        # Creative thinking frameworks
        self.thinking_frameworks = {
            "scamper": {
                "name": "SCAMPER",
                "description": "Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse",
                "prompts": [
                    "What can be substituted?",
                    "What can be combined?",
                    "What can be adapted?",
                    "What can be modified?",
                    "What other uses are there?",
                    "What can be eliminated?",
                    "What can be reversed?"
                ]
            },
            "design_thinking": {
                "name": "Design Thinking",
                "description": "Empathize, Define, Ideate, Prototype, Test",
                "prompts": [
                    "Who are the users and what do they need?",
                    "What problems are we solving?",
                    "What solutions can we brainstorm?",
                    "How can we prototype this?",
                    "How can we test and validate?"
                ]
            },
            "blue_ocean": {
                "name": "Blue Ocean Strategy",
                "description": "Create uncontested market space",
                "prompts": [
                    "What can be eliminated?",
                    "What can be reduced?",
                    "What can be raised?",
                    "What can be created?"
                ]
            },
            "jobs_to_be_done": {
                "name": "Jobs-to-be-Done",
                "description": "Focus on what users are trying to accomplish",
                "prompts": [
                    "What job is the user trying to get done?",
                    "What are the pain points in the current process?",
                    "What would make this job easier?",
                    "What would delight the user?"
                ]
            }
        }
        
        # Innovation techniques
        self.innovation_techniques = {
            "brainstorming": "Generate many ideas without judgment",
            "mind_mapping": "Visual representation of ideas and connections",
            "analogical_thinking": "Apply solutions from other domains",
            "reverse_brainstorming": "Think about how to cause the problem",
            "six_thinking_hats": "Consider different perspectives systematically",
            "morphological_analysis": "Systematic exploration of possibilities",
            "triz": "Theory of inventive problem solving",
            "biomimicry": "Learn from nature's solutions"
        }
        
        logger.info(f"💡 {self.metadata.name} initialized with creative ideation capabilities")
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute idea generation task"""
        try:
            self.status = AgentStatus.BUSY
            task_id = task.get("id", f"ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            logger.info(f"💡 Starting idea generation: {task_id}")
            
            # Extract task parameters
            project_description = task.get("content", "")
            architecture_spec = task.get("architecture_spec", {})
            focus_areas = task.get("focus_areas", list(self.idea_categories.keys()))
            thinking_framework = task.get("thinking_framework", "design_thinking")
            context = task.get("context", {})
            
            # Generate creative ideas
            ideas_result = await self._generate_ideas(
                project_description=project_description,
                architecture_spec=architecture_spec,
                focus_areas=focus_areas,
                thinking_framework=thinking_framework,
                context=context
            )
            
            # Store results in memory
            await self._store_ideas_results(
                task_id=task_id,
                ideas_result=ideas_result,
                focus_areas=focus_areas,
                thinking_framework=thinking_framework,
                session_id=task.get("session_id")
            )
            
            self.status = AgentStatus.IDLE
            
            result = {
                "success": True,
                "task_id": task_id,
                "agent": self.metadata.name,
                "ideas_generation": ideas_result,
                "focus_areas": focus_areas,
                "thinking_framework": thinking_framework,
                "timestamp": datetime.now().isoformat(),
                "memory_id": f"ideas_{task_id}",
                "tokens_used": ideas_result.get("tokens_used", 0)
            }
            
            logger.info(f"✅ Idea generation completed: {task_id}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Idea generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task.get("id", "unknown"),
                "agent": self.metadata.name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_ideas(
        self,
        project_description: str,
        architecture_spec: Dict[str, Any],
        focus_areas: List[str],
        thinking_framework: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate creative ideas using specified framework"""
        
        # Get thinking framework
        framework = self.thinking_frameworks.get(thinking_framework, self.thinking_frameworks["design_thinking"])
        
        # Create idea generation prompt
        ideas_prompt = self._create_ideas_prompt(
            project_description=project_description,
            architecture_spec=architecture_spec,
            focus_areas=focus_areas,
            framework=framework,
            context=context
        )
        
        # Generate ideas using creative model settings
        try:
            response = await self.orchestrator.generate_response(
                prompt=ideas_prompt,
                model_preference=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
                temperature=0.9,  # High temperature for maximum creativity
                max_tokens=5000
            )
            
            # Parse and structure ideas response
            ideas_result = await self._parse_ideas_response(
                response=response,
                project_description=project_description,
                focus_areas=focus_areas,
                framework=framework
            )
            
            return ideas_result
            
        except Exception as e:
            logger.error(f"❌ Ideas generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_ideas": self._create_fallback_ideas(project_description, focus_areas)
            }
    
    def _create_ideas_prompt(
        self,
        project_description: str,
        architecture_spec: Dict[str, Any],
        focus_areas: List[str],
        framework: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create detailed idea generation prompt"""
        
        architecture_context = ""
        if architecture_spec:
            architecture_context = f"""
PROJECT ARCHITECTURE:
- Technology Stack: {architecture_spec.get('technology_stack', 'Not specified')}
- System Components: {architecture_spec.get('components', 'Not specified')}
- Current Features: {architecture_spec.get('current_features', 'Not specified')}
"""
        
        focus_descriptions = []
        for area in focus_areas:
            if area in self.idea_categories:
                category = self.idea_categories[area]
                focus_descriptions.append(f"""
{area.upper()}:
- Focus: {category['focus']}
- Aspects: {category['aspects']}
- Techniques: {category['techniques']}
""")
        
        return f"""
You are a creative innovation consultant tasked with generating breakthrough ideas for a software project. Use your creativity, industry knowledge, and the specified thinking framework to brainstorm innovative solutions.

PROJECT DESCRIPTION:
{project_description}

{architecture_context}

FOCUS AREAS:
{chr(10).join(focus_descriptions)}

THINKING FRAMEWORK: {framework['name']}
{framework['description']}

FRAMEWORK PROMPTS:
{chr(10).join(f"- {prompt}" for prompt in framework['prompts'])}

CONTEXT:
{context}

INNOVATION REQUIREMENTS:
1. Think creatively and outside the box
2. Consider emerging technologies and trends
3. Focus on user value and business impact
4. Explore unconventional approaches
5. Consider different user personas and use cases
6. Think about scalability and future evolution
7. Consider market opportunities and differentiators

IDEATION PROCESS:
For each focus area, apply the thinking framework to generate innovative ideas:

1. DIVERGENT THINKING:
   - Generate as many ideas as possible
   - Don't judge ideas during generation
   - Build on other ideas
   - Think beyond obvious solutions

2. CONVERGENT THINKING:
   - Evaluate ideas for feasibility
   - Assess potential impact
   - Consider implementation complexity
   - Identify synergies between ideas

3. ENHANCEMENT:
   - Combine complementary ideas
   - Refine and improve concepts
   - Consider variations and alternatives
   - Think about implementation approaches

Please provide your ideas in the following JSON format:
{{
    "ideation_session": {{
        "project_name": "extracted or generated project name",
        "thinking_framework": "{framework['name']}",
        "focus_areas": {focus_areas},
        "session_date": "current date",
        "total_ideas": 0,
        "ideas_by_category": {{
            "user_experience": [
                {{
                    "title": "idea title",
                    "description": "detailed description",
                    "category": "user_experience",
                    "priority": "HIGH|MEDIUM|LOW",
                    "feasibility": "HIGH|MEDIUM|LOW",
                    "impact": "HIGH|MEDIUM|LOW",
                    "implementation_effort": "LOW|MEDIUM|HIGH",
                    "target_users": ["user_type1", "user_type2"],
                    "business_value": "potential business value",
                    "technical_requirements": ["requirement1", "requirement2"],
                    "inspiration_source": "what inspired this idea",
                    "related_trends": ["trend1", "trend2"],
                    "success_metrics": ["metric1", "metric2"]
                }}
            ],
            "functionality": [...],
            "technical": [...],
            "business": [...],
            "innovation": [...]
        }}
    }},
    "idea_combinations": [
        {{
            "combination_name": "name for combined concept",
            "description": "how ideas work together",
            "combined_ideas": ["idea1", "idea2", "idea3"],
            "synergy_benefits": ["benefit1", "benefit2"],
            "implementation_approach": "how to implement together"
        }}
    ],
    "implementation_roadmap": [
        {{
            "phase": "phase name",
            "timeframe": "estimated timeframe",
            "ideas_to_implement": ["idea1", "idea2"],
            "dependencies": ["dependency1", "dependency2"],
            "success_criteria": ["criteria1", "criteria2"]
        }}
    ],
    "innovation_opportunities": [
        {{
            "opportunity": "opportunity description",
            "market_potential": "market potential assessment",
            "competitive_advantage": "potential competitive advantage",
            "technology_enablers": ["technology1", "technology2"],
            "implementation_challenges": ["challenge1", "challenge2"]
        }}
    ],
    "next_steps": [
        "immediate actions to explore ideas",
        "validation approaches",
        "prototyping suggestions",
        "market research recommendations"
    ]
}}

Be creative, think big, and focus on ideas that could significantly enhance the project's value and user experience.
"""
    
    async def _parse_ideas_response(
        self,
        response: str,
        project_description: str,
        focus_areas: List[str],
        framework: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse and validate ideas response"""
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            ideas_data = json.loads(json_str)
            
            # Count total ideas
            total_ideas = 0
            for category in ideas_data.get("ideation_session", {}).get("ideas_by_category", {}).values():
                total_ideas += len(category)
            
            # Validate and enhance ideas data
            ideas_result = {
                "success": True,
                "project_description": project_description,
                "focus_areas": focus_areas,
                "thinking_framework": framework['name'],
                "generated_at": datetime.now().isoformat(),
                "ideation_session": ideas_data.get("ideation_session", {}),
                "idea_combinations": ideas_data.get("idea_combinations", []),
                "implementation_roadmap": ideas_data.get("implementation_roadmap", []),
                "innovation_opportunities": ideas_data.get("innovation_opportunities", []),
                "next_steps": ideas_data.get("next_steps", []),
                "metadata": {
                    "total_ideas": total_ideas,
                    "categories_explored": len(focus_areas),
                    "combinations_suggested": len(ideas_data.get("idea_combinations", [])),
                    "implementation_phases": len(ideas_data.get("implementation_roadmap", [])),
                    "innovation_opportunities": len(ideas_data.get("innovation_opportunities", []))
                },
                "tokens_used": len(response.split())
            }
            
            return ideas_result
            
        except Exception as e:
            logger.error(f"❌ Ideas parsing failed: {e}")
            return {
                "success": False,
                "error": f"Failed to parse ideas: {str(e)}",
                "raw_response": response,
                "fallback_ideas": self._create_fallback_ideas(project_description, focus_areas)
            }
    
    def _create_fallback_ideas(self, project_description: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create basic fallback ideas"""
        
        fallback_ideas = {
            "user_experience": [
                {
                    "title": "Improved User Interface",
                    "description": "Enhance the user interface for better usability and accessibility",
                    "category": "user_experience",
                    "priority": "HIGH",
                    "feasibility": "HIGH",
                    "impact": "MEDIUM",
                    "implementation_effort": "MEDIUM",
                    "target_users": ["all users"],
                    "business_value": "Better user satisfaction and retention",
                    "technical_requirements": ["UI/UX design", "frontend development"],
                    "inspiration_source": "Best practices in UI design",
                    "related_trends": ["responsive design", "accessibility"],
                    "success_metrics": ["user satisfaction", "task completion rate"]
                }
            ],
            "functionality": [
                {
                    "title": "Enhanced Core Features",
                    "description": "Improve and expand core functionality based on user feedback",
                    "category": "functionality",
                    "priority": "HIGH",
                    "feasibility": "HIGH",
                    "impact": "HIGH",
                    "implementation_effort": "MEDIUM",
                    "target_users": ["power users", "regular users"],
                    "business_value": "Increased user engagement and value",
                    "technical_requirements": ["backend development", "API enhancement"],
                    "inspiration_source": "User feedback and market research",
                    "related_trends": ["feature richness", "user empowerment"],
                    "success_metrics": ["feature adoption", "user engagement"]
                }
            ],
            "technical": [
                {
                    "title": "Performance Optimization",
                    "description": "Optimize system performance for better speed and scalability",
                    "category": "technical",
                    "priority": "MEDIUM",
                    "feasibility": "HIGH",
                    "impact": "HIGH",
                    "implementation_effort": "HIGH",
                    "target_users": ["all users"],
                    "business_value": "Better user experience and reduced costs",
                    "technical_requirements": ["performance profiling", "optimization techniques"],
                    "inspiration_source": "Performance best practices",
                    "related_trends": ["high-performance computing", "cloud optimization"],
                    "success_metrics": ["response time", "throughput", "resource usage"]
                }
            ],
            "business": [
                {
                    "title": "Analytics Dashboard",
                    "description": "Add comprehensive analytics and reporting capabilities",
                    "category": "business",
                    "priority": "MEDIUM",
                    "feasibility": "MEDIUM",
                    "impact": "MEDIUM",
                    "implementation_effort": "MEDIUM",
                    "target_users": ["administrators", "business users"],
                    "business_value": "Better decision making and insights",
                    "technical_requirements": ["data analytics", "visualization tools"],
                    "inspiration_source": "Business intelligence trends",
                    "related_trends": ["data-driven decision making", "real-time analytics"],
                    "success_metrics": ["dashboard usage", "decision speed", "insights quality"]
                }
            ],
            "innovation": [
                {
                    "title": "AI Integration",
                    "description": "Integrate artificial intelligence for intelligent automation",
                    "category": "innovation",
                    "priority": "LOW",
                    "feasibility": "MEDIUM",
                    "impact": "HIGH",
                    "implementation_effort": "HIGH",
                    "target_users": ["all users"],
                    "business_value": "Competitive advantage and automation",
                    "technical_requirements": ["AI/ML models", "data processing"],
                    "inspiration_source": "AI advancement trends",
                    "related_trends": ["machine learning", "automation", "intelligent systems"],
                    "success_metrics": ["automation rate", "accuracy", "user satisfaction"]
                }
            ]
        }
        
        return {
            "ideation_session": {
                "project_name": "Software Project",
                "thinking_framework": "Basic brainstorming",
                "focus_areas": focus_areas,
                "session_date": datetime.now().isoformat(),
                "total_ideas": sum(len(ideas) for ideas in fallback_ideas.values()),
                "ideas_by_category": {
                    area: fallback_ideas.get(area, [])
                    for area in focus_areas
                }
            },
            "idea_combinations": [
                {
                    "combination_name": "Enhanced User Experience",
                    "description": "Combine UI improvements with performance optimization",
                    "combined_ideas": ["Improved User Interface", "Performance Optimization"],
                    "synergy_benefits": ["Better overall user experience", "Faster and more intuitive interface"],
                    "implementation_approach": "Implement UI changes alongside performance improvements"
                }
            ],
            "implementation_roadmap": [
                {
                    "phase": "Foundation",
                    "timeframe": "1-2 months",
                    "ideas_to_implement": ["Performance Optimization", "Improved User Interface"],
                    "dependencies": ["System analysis", "UI/UX design"],
                    "success_criteria": ["Performance baseline", "UI prototype"]
                },
                {
                    "phase": "Enhancement",
                    "timeframe": "2-3 months",
                    "ideas_to_implement": ["Enhanced Core Features", "Analytics Dashboard"],
                    "dependencies": ["Foundation phase completion"],
                    "success_criteria": ["Feature delivery", "Analytics implementation"]
                },
                {
                    "phase": "Innovation",
                    "timeframe": "3-6 months",
                    "ideas_to_implement": ["AI Integration"],
                    "dependencies": ["Core system stability"],
                    "success_criteria": ["AI prototype", "User validation"]
                }
            ],
            "innovation_opportunities": [
                {
                    "opportunity": "Market differentiation through AI",
                    "market_potential": "High potential for competitive advantage",
                    "competitive_advantage": "Intelligent automation capabilities",
                    "technology_enablers": ["Machine learning", "Natural language processing"],
                    "implementation_challenges": ["Data quality", "Model training", "User acceptance"]
                }
            ],
            "next_steps": [
                "Conduct user research to validate ideas",
                "Create prototypes for high-priority ideas",
                "Perform technical feasibility analysis",
                "Develop detailed implementation plans"
            ]
        }
    
    async def _store_ideas_results(
        self,
        task_id: str,
        ideas_result: Dict[str, Any],
        focus_areas: List[str],
        thinking_framework: str,
        session_id: Optional[str] = None
    ):
        """Store ideas generation results in memory"""
        
        content = f"""
Ideas Generation Results

Task ID: {task_id}
Focus Areas: {focus_areas}
Thinking Framework: {thinking_framework}
Generated: {datetime.now().isoformat()}

Ideas Summary:
- Success: {ideas_result.get('success', False)}
- Total Ideas: {ideas_result.get('metadata', {}).get('total_ideas', 0)}
- Categories Explored: {ideas_result.get('metadata', {}).get('categories_explored', 0)}
- Combinations Suggested: {ideas_result.get('metadata', {}).get('combinations_suggested', 0)}
- Implementation Phases: {ideas_result.get('metadata', {}).get('implementation_phases', 0)}
- Innovation Opportunities: {ideas_result.get('metadata', {}).get('innovation_opportunities', 0)}

Full Ideas Result:
{json.dumps(ideas_result, indent=2)}
"""
        
        self.memory_manager.store_memory(
            content=content,
            memory_type=MemoryType.TASK,
            priority=MemoryPriority.MEDIUM,
            metadata={
                "agent": self.metadata.name,
                "task_id": task_id,
                "focus_areas": focus_areas,
                "thinking_framework": thinking_framework,
                "ideas_success": ideas_result.get("success", False),
                "total_ideas": ideas_result.get("metadata", {}).get("total_ideas", 0),
                "categories_explored": ideas_result.get("metadata", {}).get("categories_explored", 0)
            },
            tags=["ideas", "innovation", "brainstorming", "obelisk", "ideas_agent"],
            session_id=session_id
        )
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_name": self.metadata.name,
            "agent_type": self.metadata.agent_type.value,
            "capabilities": self.metadata.capabilities,
            "idea_categories": list(self.idea_categories.keys()),
            "thinking_frameworks": list(self.thinking_frameworks.keys()),
            "innovation_techniques": list(self.innovation_techniques.keys()),
            "ideation_features": [
                "Creative brainstorming",
                "Structured thinking frameworks",
                "Multi-category idea generation",
                "Idea combination and synthesis",
                "Implementation roadmapping",
                "Innovation opportunity identification",
                "Business value assessment",
                "Technical feasibility analysis"
            ],
            "max_concurrent_tasks": self.metadata.max_concurrent_tasks,
            "timeout_seconds": self.metadata.timeout_seconds
        }


def create_ideas_agent(config: Dict[str, Any]) -> IdeasAgent:
    """Factory function to create Ideas Agent"""
    return IdeasAgent(config)