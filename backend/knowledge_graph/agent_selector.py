"""
Graph-based Agent Selection Algorithms

This module implements intelligent agent selection algorithms using the knowledge graph
to optimize agent coordination and task routing.
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import math

from .knowledge_graph import KnowledgeGraph
from .schema import (
    AgentNode,
    TaskNode,
    GraphRelationship,
    RelationshipType,
    NodeType,
    CapabilityCategory
)

logger = logging.getLogger(__name__)


class SelectionStrategy(Enum):
    """Agent selection strategies"""
    GREEDY = "greedy"                    # Select best single agent
    OPTIMAL_SEQUENCE = "optimal_sequence"  # Find optimal agent sequence
    COLLABORATIVE = "collaborative"      # Multi-agent collaboration
    LOAD_BALANCED = "load_balanced"      # Balance load across agents
    ADAPTIVE = "adaptive"                # Adaptive selection based on context


@dataclass
class AgentScore:
    """Score for an agent's suitability for a task"""
    agent: AgentNode
    score: float
    confidence: float
    reasoning: List[str]
    
    def __post_init__(self):
        self.score = max(0.0, min(1.0, self.score))  # Clamp to [0, 1]
        self.confidence = max(0.0, min(1.0, self.confidence))


@dataclass
class SelectionResult:
    """Result of agent selection process"""
    agents: List[AgentNode]
    scores: List[AgentScore]
    strategy: SelectionStrategy
    execution_plan: Dict[str, Any]
    metadata: Dict[str, Any]
    total_confidence: float = 0.0
    
    def __post_init__(self):
        if self.scores:
            self.total_confidence = sum(s.confidence for s in self.scores) / len(self.scores)


class GraphBasedAgentSelector:
    """
    Intelligent agent selector using knowledge graph analysis
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.selection_history = []
        self.performance_cache = {}
    
    async def select_agents(
        self,
        task: Dict[str, Any],
        strategy: SelectionStrategy = SelectionStrategy.OPTIMAL_SEQUENCE,
        max_agents: int = 5,
        min_confidence: float = 0.3
    ) -> SelectionResult:
        """
        Select optimal agents for a task using the specified strategy
        """
        logger.info(f"Selecting agents for task using {strategy.value} strategy")
        
        # Analyze task requirements
        task_analysis = await self._analyze_task(task)
        
        # Apply selection strategy
        if strategy == SelectionStrategy.GREEDY:
            result = await self._greedy_selection(task_analysis, max_agents, min_confidence)
        elif strategy == SelectionStrategy.OPTIMAL_SEQUENCE:
            result = await self._optimal_sequence_selection(task_analysis, max_agents, min_confidence)
        elif strategy == SelectionStrategy.COLLABORATIVE:
            result = await self._collaborative_selection(task_analysis, max_agents, min_confidence)
        elif strategy == SelectionStrategy.LOAD_BALANCED:
            result = await self._load_balanced_selection(task_analysis, max_agents, min_confidence)
        elif strategy == SelectionStrategy.ADAPTIVE:
            result = await self._adaptive_selection(task_analysis, max_agents, min_confidence)
        else:
            raise ValueError(f"Unknown selection strategy: {strategy}")
        
        # Record selection for learning
        self._record_selection(task, result)
        
        return result
    
    async def _analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task to extract requirements and context"""
        content = task.get("content", "").lower()
        task_type = task.get("type", "")
        priority = task.get("priority", 5)
        complexity = task.get("complexity", "MEDIUM")
        
        # Extract capabilities from content
        required_capabilities = []
        
        # Capability keywords mapping
        capability_keywords = {
            "architecture": ["architecture", "design", "planning", "system"],
            "coding": ["code", "implement", "develop", "build", "create"],
            "testing": ["test", "verify", "validate", "check", "qa"],
            "review": ["review", "audit", "analyze", "evaluate"],
            "deployment": ["deploy", "release", "production", "launch"],
            "security": ["security", "secure", "protect", "vulnerability"],
            "orchestration": ["orchestrate", "coordinate", "manage", "workflow"],
            "creative": ["creative", "innovative", "design", "artistic"],
            "analysis": ["analyze", "research", "investigate", "study"],
            "documentation": ["document", "explain", "describe", "guide"]
        }
        
        for capability, keywords in capability_keywords.items():
            if any(keyword in content for keyword in keywords):
                required_capabilities.append(capability)
        
        # If no capabilities detected, infer from task type
        if not required_capabilities and task_type:
            type_mapping = {
                "code": ["coding", "testing"],
                "architecture": ["architecture", "planning"],
                "deploy": ["deployment", "testing"],
                "review": ["review", "analysis"],
                "test": ["testing", "analysis"]
            }
            
            for key, caps in type_mapping.items():
                if key in task_type.lower():
                    required_capabilities.extend(caps)
        
        # Determine complexity score
        complexity_scores = {
            "SIMPLE": 0.2,
            "MEDIUM": 0.5,
            "COMPLEX": 0.8,
            "EXPERT": 1.0
        }
        complexity_score = complexity_scores.get(complexity, 0.5)
        
        return {
            "content": content,
            "type": task_type,
            "priority": priority,
            "complexity": complexity,
            "complexity_score": complexity_score,
            "required_capabilities": required_capabilities,
            "estimated_duration": task.get("estimated_duration", 300),
            "session_id": task.get("session_id"),
            "workflow_id": task.get("workflow_id")
        }
    
    async def _score_agent(self, agent: AgentNode, task_analysis: Dict[str, Any]) -> AgentScore:
        """Score an agent's suitability for a task"""
        score = 0.0
        confidence = 0.0
        reasoning = []
        
        # Capability matching (40% of score)
        capability_score = 0.0
        required_caps = task_analysis["required_capabilities"]
        
        if required_caps:
            matched_caps = sum(1 for cap in required_caps if cap in agent.capabilities)
            capability_score = matched_caps / len(required_caps)
            score += capability_score * 0.4
            reasoning.append(f"Capability match: {matched_caps}/{len(required_caps)} capabilities")
        else:
            capability_score = 0.5  # Neutral if no specific capabilities required
            score += capability_score * 0.4
            reasoning.append("No specific capabilities required")
        
        # Agent type relevance (20% of score)
        type_score = 0.0
        task_type = task_analysis["type"]
        if task_type:
            type_keywords = {
                "ARCHITECT": ["architecture", "design", "planning"],
                "CODER": ["code", "implement", "develop"],
                "TESTER": ["test", "verify", "qa"],
                "REVIEWER": ["review", "audit", "analyze"],
                "DEPLOYER": ["deploy", "release", "production"],
                "ORCHESTRATOR": ["orchestrate", "manage", "coordinate"]
            }
            
            agent_type = agent.agent_type.upper()
            if agent_type in type_keywords:
                keywords = type_keywords[agent_type]
                matches = sum(1 for keyword in keywords if keyword in task_type.lower())
                type_score = min(1.0, matches / len(keywords))
            
            score += type_score * 0.2
            reasoning.append(f"Type relevance: {agent_type} for {task_type}")
        
        # Performance metrics (20% of score)
        performance_score = 0.0
        if agent.performance_metrics:
            success_rate = agent.performance_metrics.get("success_rate", 0.5)
            avg_response_time = agent.performance_metrics.get("average_response_time", 30.0)
            
            # Normalize response time (lower is better)
            time_score = max(0.0, 1.0 - (avg_response_time / 60.0))  # Normalize to 60 seconds
            
            performance_score = (success_rate * 0.7) + (time_score * 0.3)
            score += performance_score * 0.2
            reasoning.append(f"Performance: {success_rate:.2f} success rate, {avg_response_time:.1f}s avg time")
        else:
            performance_score = 0.5  # Neutral if no performance data
            score += performance_score * 0.2
            reasoning.append("No performance data available")
        
        # Priority alignment (10% of score)
        priority_score = 0.0
        task_priority = task_analysis["priority"]
        priority_diff = abs(agent.priority - task_priority)
        priority_score = max(0.0, 1.0 - (priority_diff / 10.0))  # Normalize to 0-10 scale
        
        score += priority_score * 0.1
        reasoning.append(f"Priority alignment: agent={agent.priority}, task={task_priority}")
        
        # Availability (10% of score)
        availability_score = 0.0
        if agent.status == "IDLE":
            availability_score = 1.0
        elif agent.status == "BUSY":
            # Check current load
            current_tasks = len(getattr(agent, 'current_tasks', []))
            if current_tasks < agent.max_concurrent_tasks:
                availability_score = 1.0 - (current_tasks / agent.max_concurrent_tasks)
            else:
                availability_score = 0.0
        else:
            availability_score = 0.0  # ERROR or DISABLED
        
        score += availability_score * 0.1
        reasoning.append(f"Availability: {agent.status}")
        
        # Calculate confidence based on data quality
        confidence_factors = [
            1.0 if agent.capabilities else 0.5,
            1.0 if agent.performance_metrics else 0.3,
            1.0 if agent.status == "IDLE" else 0.7,
            1.0 if required_caps else 0.8
        ]
        confidence = sum(confidence_factors) / len(confidence_factors)
        
        return AgentScore(
            agent=agent,
            score=score,
            confidence=confidence,
            reasoning=reasoning
        )
    
    async def _greedy_selection(
        self,
        task_analysis: Dict[str, Any],
        max_agents: int,
        min_confidence: float
    ) -> SelectionResult:
        """Select agents using greedy algorithm (best single agent)"""
        
        agents = self.knowledge_graph.get_agents()
        scores = []
        
        for agent in agents:
            score = await self._score_agent(agent, task_analysis)
            if score.confidence >= min_confidence:
                scores.append(score)
        
        # Sort by score
        scores.sort(key=lambda x: x.score, reverse=True)
        
        # Take the best agent
        selected_agents = [scores[0].agent] if scores else []
        selected_scores = [scores[0]] if scores else []
        
        return SelectionResult(
            agents=selected_agents,
            scores=selected_scores,
            strategy=SelectionStrategy.GREEDY,
            execution_plan={"type": "single_agent", "sequence": [a.name for a in selected_agents]},
            metadata={"total_candidates": len(agents), "qualified_candidates": len(scores)}
        )
    
    async def _optimal_sequence_selection(
        self,
        task_analysis: Dict[str, Any],
        max_agents: int,
        min_confidence: float
    ) -> SelectionResult:
        """Select optimal sequence of agents based on dependencies"""
        
        # Get all qualified agents
        agents = self.knowledge_graph.get_agents()
        qualified_scores = []
        
        for agent in agents:
            score = await self._score_agent(agent, task_analysis)
            if score.confidence >= min_confidence:
                qualified_scores.append(score)
        
        if not qualified_scores:
            return SelectionResult(
                agents=[],
                scores=[],
                strategy=SelectionStrategy.OPTIMAL_SEQUENCE,
                execution_plan={},
                metadata={"error": "No qualified agents found"}
            )
        
        # Build dependency graph
        dependency_graph = {}
        for score in qualified_scores:
            agent = score.agent
            dependencies = self.knowledge_graph.find_agent_dependencies(agent.id)
            dependency_graph[agent.id] = [dep.id for dep in dependencies if any(s.agent.id == dep.id for s in qualified_scores)]
        
        # Find optimal sequence using topological sort with scoring
        sequence = self._topological_sort_with_scoring(qualified_scores, dependency_graph)
        
        # Limit to max_agents
        sequence = sequence[:max_agents]
        
        return SelectionResult(
            agents=[s.agent for s in sequence],
            scores=sequence,
            strategy=SelectionStrategy.OPTIMAL_SEQUENCE,
            execution_plan={
                "type": "sequential",
                "sequence": [s.agent.name for s in sequence],
                "dependencies": dependency_graph
            },
            metadata={"total_candidates": len(agents), "qualified_candidates": len(qualified_scores)}
        )
    
    def _topological_sort_with_scoring(
        self,
        scores: List[AgentScore],
        dependency_graph: Dict[str, List[str]]
    ) -> List[AgentScore]:
        """Topological sort considering both dependencies and scores"""
        
        # Create mapping
        score_map = {score.agent.id: score for score in scores}
        
        # Calculate in-degrees
        in_degree = {score.agent.id: 0 for score in scores}
        for agent_id, deps in dependency_graph.items():
            for dep_id in deps:
                if dep_id in in_degree:
                    in_degree[dep_id] += 1
        
        # Initialize queue with nodes having no dependencies, sorted by score
        queue = []
        for score in scores:
            if in_degree[score.agent.id] == 0:
                queue.append(score)
        queue.sort(key=lambda x: x.score, reverse=True)
        
        result = []
        
        while queue:
            # Take the highest scoring available agent
            current_score = queue.pop(0)
            result.append(current_score)
            
            # Update in-degrees for dependent agents
            for dep_id in dependency_graph.get(current_score.agent.id, []):
                if dep_id in in_degree:
                    in_degree[dep_id] -= 1
                    if in_degree[dep_id] == 0:
                        dep_score = score_map[dep_id]
                        queue.append(dep_score)
                        queue.sort(key=lambda x: x.score, reverse=True)
        
        return result
    
    async def _collaborative_selection(
        self,
        task_analysis: Dict[str, Any],
        max_agents: int,
        min_confidence: float
    ) -> SelectionResult:
        """Select agents that work well together"""
        
        # Start with greedy selection
        greedy_result = await self._greedy_selection(task_analysis, 1, min_confidence)
        
        if not greedy_result.agents:
            return greedy_result
        
        primary_agent = greedy_result.agents[0]
        selected_agents = [primary_agent]
        selected_scores = [greedy_result.scores[0]]
        
        # Find collaborators
        collaborators = self.knowledge_graph.find_agent_collaborators(primary_agent.id)
        
        # Score collaborators
        collaborator_scores = []
        for collaborator in collaborators:
            score = await self._score_agent(collaborator, task_analysis)
            if score.confidence >= min_confidence:
                collaborator_scores.append(score)
        
        # Sort by score and add to selection
        collaborator_scores.sort(key=lambda x: x.score, reverse=True)
        
        for score in collaborator_scores:
            if len(selected_agents) >= max_agents:
                break
            
            selected_agents.append(score.agent)
            selected_scores.append(score)
        
        return SelectionResult(
            agents=selected_agents,
            scores=selected_scores,
            strategy=SelectionStrategy.COLLABORATIVE,
            execution_plan={
                "type": "collaborative",
                "primary_agent": primary_agent.name,
                "collaborators": [a.name for a in selected_agents[1:]]
            },
            metadata={"collaboration_strength": len(collaborators)}
        )
    
    async def _load_balanced_selection(
        self,
        task_analysis: Dict[str, Any],
        max_agents: int,
        min_confidence: float
    ) -> SelectionResult:
        """Select agents with load balancing considerations"""
        
        agents = self.knowledge_graph.get_agents()
        scores = []
        
        for agent in agents:
            base_score = await self._score_agent(agent, task_analysis)
            
            if base_score.confidence >= min_confidence:
                # Adjust score based on current load
                current_load = len(getattr(agent, 'current_tasks', [])) / agent.max_concurrent_tasks
                load_penalty = current_load * 0.3  # Reduce score by up to 30% for high load
                
                adjusted_score = AgentScore(
                    agent=agent,
                    score=max(0.0, base_score.score - load_penalty),
                    confidence=base_score.confidence,
                    reasoning=base_score.reasoning + [f"Load adjustment: -{load_penalty:.2f}"]
                )
                
                scores.append(adjusted_score)
        
        # Sort by adjusted score
        scores.sort(key=lambda x: x.score, reverse=True)
        
        # Select top agents
        selected_scores = scores[:max_agents]
        selected_agents = [s.agent for s in selected_scores]
        
        return SelectionResult(
            agents=selected_agents,
            scores=selected_scores,
            strategy=SelectionStrategy.LOAD_BALANCED,
            execution_plan={
                "type": "load_balanced",
                "agents": [{"name": a.name, "current_load": len(getattr(a, 'current_tasks', [])) / a.max_concurrent_tasks} for a in selected_agents]
            },
            metadata={"total_candidates": len(agents), "qualified_candidates": len(scores)}
        )
    
    async def _adaptive_selection(
        self,
        task_analysis: Dict[str, Any],
        max_agents: int,
        min_confidence: float
    ) -> SelectionResult:
        """Adaptive selection based on context and history"""
        
        # Analyze task complexity to choose strategy
        complexity_score = task_analysis["complexity_score"]
        
        if complexity_score < 0.3:
            # Simple tasks: use greedy
            return await self._greedy_selection(task_analysis, max_agents, min_confidence)
        elif complexity_score < 0.7:
            # Medium tasks: use optimal sequence
            return await self._optimal_sequence_selection(task_analysis, max_agents, min_confidence)
        else:
            # Complex tasks: use collaborative
            return await self._collaborative_selection(task_analysis, max_agents, min_confidence)
    
    def _record_selection(self, task: Dict[str, Any], result: SelectionResult) -> None:
        """Record selection for learning and improvement"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": {
                "agents": [a.name for a in result.agents],
                "strategy": result.strategy.value,
                "confidence": result.total_confidence
            }
        }
        
        self.selection_history.append(record)
        
        # Keep only last 1000 records
        if len(self.selection_history) > 1000:
            self.selection_history = self.selection_history[-1000:]
    
    async def get_selection_analytics(self) -> Dict[str, Any]:
        """Get analytics about selection performance"""
        if not self.selection_history:
            return {"message": "No selection history available"}
        
        total_selections = len(self.selection_history)
        
        # Strategy usage
        strategy_count = {}
        for record in self.selection_history:
            strategy = record["result"]["strategy"]
            strategy_count[strategy] = strategy_count.get(strategy, 0) + 1
        
        # Average confidence by strategy
        strategy_confidence = {}
        for record in self.selection_history:
            strategy = record["result"]["strategy"]
            confidence = record["result"]["confidence"]
            
            if strategy not in strategy_confidence:
                strategy_confidence[strategy] = []
            strategy_confidence[strategy].append(confidence)
        
        avg_confidence = {}
        for strategy, confidences in strategy_confidence.items():
            avg_confidence[strategy] = sum(confidences) / len(confidences)
        
        return {
            "total_selections": total_selections,
            "strategy_usage": strategy_count,
            "average_confidence_by_strategy": avg_confidence,
            "most_used_strategy": max(strategy_count.items(), key=lambda x: x[1])[0] if strategy_count else None
        }
    
    async def recommend_optimal_strategy(self, task: Dict[str, Any]) -> SelectionStrategy:
        """Recommend optimal selection strategy for a task"""
        task_analysis = await self._analyze_task(task)
        
        complexity_score = task_analysis["complexity_score"]
        required_caps = len(task_analysis["required_capabilities"])
        
        # Decision tree for strategy selection
        if complexity_score < 0.3 and required_caps <= 1:
            return SelectionStrategy.GREEDY
        elif complexity_score >= 0.8 or required_caps > 3:
            return SelectionStrategy.COLLABORATIVE
        elif required_caps > 1:
            return SelectionStrategy.OPTIMAL_SEQUENCE
        else:
            return SelectionStrategy.LOAD_BALANCED