"""
Agent Analyzer for Knowledge Graph Population

This module analyzes existing agents and populates the knowledge graph with
agent nodes, capabilities, and relationships.
"""

import asyncio
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..agents.registry.agent_registry import AgentRegistry, AgentType
from ..agents.integration_manager import AgentIntegrationManager
from .knowledge_graph import KnowledgeGraph
from .schema import (
    AgentNode,
    CapabilityNode,
    GraphRelationship,
    RelationshipType,
    CapabilityCategory,
    NodeType
)

logger = logging.getLogger(__name__)


class AgentAnalyzer:
    """
    Analyzes existing agents and populates the knowledge graph with
    agent relationships and capabilities
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.agent_registry = AgentRegistry()
        self.integration_manager = None
        
        # Capability category mapping
        self.capability_categories = {
            "planning": CapabilityCategory.PLANNING,
            "architecture": CapabilityCategory.PLANNING,
            "project": CapabilityCategory.MANAGEMENT,
            "management": CapabilityCategory.MANAGEMENT,
            "coding": CapabilityCategory.DEVELOPMENT,
            "development": CapabilityCategory.DEVELOPMENT,
            "generation": CapabilityCategory.DEVELOPMENT,
            "testing": CapabilityCategory.TESTING,
            "qa": CapabilityCategory.TESTING,
            "review": CapabilityCategory.ANALYSIS,
            "analysis": CapabilityCategory.ANALYSIS,
            "deployment": CapabilityCategory.DEPLOYMENT,
            "devops": CapabilityCategory.DEPLOYMENT,
            "security": CapabilityCategory.SECURITY,
            "creative": CapabilityCategory.CREATIVE,
            "innovation": CapabilityCategory.CREATIVE,
            "coordination": CapabilityCategory.COORDINATION,
            "orchestration": CapabilityCategory.COORDINATION,
            "communication": CapabilityCategory.COMMUNICATION,
            "collaboration": CapabilityCategory.COMMUNICATION,
        }
    
    async def initialize_integration_manager(self) -> None:
        """Initialize the agent integration manager"""
        if not self.integration_manager:
            self.integration_manager = AgentIntegrationManager()
            await self.integration_manager.initialize()
    
    def categorize_capability(self, capability: str) -> CapabilityCategory:
        """Categorize a capability based on keywords"""
        capability_lower = capability.lower()
        
        for keyword, category in self.capability_categories.items():
            if keyword in capability_lower:
                return category
        
        return CapabilityCategory.DEVELOPMENT  # Default category
    
    def calculate_capability_complexity(self, capability: str) -> float:
        """Calculate complexity score for a capability"""
        complexity_keywords = {
            "architecture": 0.9,
            "orchestration": 0.8,
            "coordination": 0.7,
            "management": 0.6,
            "analysis": 0.5,
            "generation": 0.4,
            "testing": 0.3,
            "deployment": 0.2,
        }
        
        capability_lower = capability.lower()
        max_complexity = 0.0
        
        for keyword, complexity in complexity_keywords.items():
            if keyword in capability_lower:
                max_complexity = max(max_complexity, complexity)
        
        return max_complexity if max_complexity > 0 else 0.3  # Default complexity
    
    async def analyze_and_populate(self) -> None:
        """Analyze all agents and populate the knowledge graph"""
        await self.initialize_integration_manager()
        
        logger.info("Starting agent analysis and knowledge graph population")
        
        # Get all registered agents
        agents = self.integration_manager.get_all_agents()
        
        # Step 1: Create capability nodes
        capability_nodes = await self._create_capability_nodes(agents)
        
        # Step 2: Create agent nodes
        agent_nodes = await self._create_agent_nodes(agents)
        
        # Step 3: Create agent-capability relationships
        await self._create_agent_capability_relationships(agent_nodes)
        
        # Step 4: Create agent-agent relationships
        await self._create_agent_relationships(agent_nodes)
        
        # Step 5: Create workflow patterns
        await self._create_workflow_patterns(agent_nodes)
        
        logger.info(f"Analysis complete. Created {len(agent_nodes)} agents and {len(capability_nodes)} capabilities")
    
    async def _create_capability_nodes(self, agents: List[Any]) -> List[CapabilityNode]:
        """Create capability nodes from all agent capabilities"""
        all_capabilities = set()
        
        # Collect all unique capabilities
        for agent in agents:
            if hasattr(agent, 'metadata') and agent.metadata.capabilities:
                all_capabilities.update(agent.metadata.capabilities)
        
        capability_nodes = []
        
        for capability in all_capabilities:
            category = self.categorize_capability(capability)
            complexity = self.calculate_capability_complexity(capability)
            
            capability_node = CapabilityNode(
                name=capability,
                description=f"Capability: {capability}",
                category=category,
                complexity_score=complexity,
                level=min(4, max(1, int(complexity * 4) + 1))  # Convert to 1-4 scale
            )
            
            self.knowledge_graph.add_node(capability_node)
            capability_nodes.append(capability_node)
        
        logger.info(f"Created {len(capability_nodes)} capability nodes")
        return capability_nodes
    
    async def _create_agent_nodes(self, agents: List[Any]) -> List[AgentNode]:
        """Create agent nodes from registered agents"""
        agent_nodes = []
        
        for agent in agents:
            if not hasattr(agent, 'metadata'):
                continue
            
            metadata = agent.metadata
            
            # Determine system name based on agent name or class
            system_name = self._determine_system_name(agent)
            
            agent_node = AgentNode(
                name=metadata.name,
                description=metadata.description,
                agent_type=metadata.agent_type.value if hasattr(metadata.agent_type, 'value') else str(metadata.agent_type),
                system_name=system_name,
                capabilities=metadata.capabilities or [],
                priority=metadata.priority,
                max_concurrent_tasks=metadata.max_concurrent_tasks,
                timeout_seconds=metadata.timeout_seconds,
                retry_count=metadata.retry_count,
                model_requirements=metadata.model_requirements or {},
                performance_metrics=getattr(agent, 'stats', {}) if hasattr(agent, 'stats') else {},
                status=agent.status.value if hasattr(agent, 'status') else "IDLE"
            )
            
            # Add system-specific metadata
            agent_node.metadata.update({
                "system": system_name,
                "class_name": agent.__class__.__name__,
                "created_by": "agent_analyzer"
            })
            
            self.knowledge_graph.add_node(agent_node)
            agent_nodes.append(agent_node)
        
        logger.info(f"Created {len(agent_nodes)} agent nodes")
        return agent_nodes
    
    def _determine_system_name(self, agent: Any) -> str:
        """Determine which system an agent belongs to"""
        class_name = agent.__class__.__name__.lower()
        module_name = agent.__class__.__module__.lower()
        
        if "agency" in module_name:
            return "agency"
        elif "meistrocraft" in module_name:
            return "meistrocraft"
        elif "obelisk" in module_name:
            return "obelisk"
        elif "ai_dev_team" in module_name:
            return "ai_dev_team"
        elif "village" in module_name:
            return "village"
        else:
            return "unknown"
    
    async def _create_agent_capability_relationships(self, agent_nodes: List[AgentNode]) -> None:
        """Create relationships between agents and their capabilities"""
        capability_nodes = self.knowledge_graph.get_capabilities()
        capability_map = {cap.name: cap for cap in capability_nodes}
        
        for agent in agent_nodes:
            for capability_name in agent.capabilities:
                if capability_name in capability_map:
                    capability = capability_map[capability_name]
                    
                    relationship = GraphRelationship(
                        source_id=agent.id,
                        target_id=capability.id,
                        relationship_type=RelationshipType.HAS_CAPABILITY,
                        strength=1.0,
                        confidence=1.0,
                        metadata={
                            "agent_system": agent.system_name,
                            "capability_category": capability.category.value
                        }
                    )
                    
                    self.knowledge_graph.add_relationship(relationship)
    
    async def _create_agent_relationships(self, agent_nodes: List[AgentNode]) -> None:
        """Create relationships between agents based on their roles and capabilities"""
        
        # Create system-based collaborations
        system_groups = {}
        for agent in agent_nodes:
            if agent.system_name not in system_groups:
                system_groups[agent.system_name] = []
            system_groups[agent.system_name].append(agent)
        
        # Create collaboration relationships within systems
        for system_name, agents in system_groups.items():
            for i, agent1 in enumerate(agents):
                for agent2 in agents[i+1:]:
                    relationship = GraphRelationship(
                        source_id=agent1.id,
                        target_id=agent2.id,
                        relationship_type=RelationshipType.COLLABORATES_WITH,
                        strength=0.8,  # High collaboration within systems
                        confidence=0.9,
                        metadata={
                            "system": system_name,
                            "relationship_basis": "same_system"
                        }
                    )
                    self.knowledge_graph.add_relationship(relationship)
        
        # Create dependency relationships based on agent types
        dependencies = {
            "architect": ["coder", "tester", "reviewer"],
            "coder": ["tester", "reviewer"],
            "tester": ["reviewer", "fixer"],
            "reviewer": ["fixer"],
            "fixer": ["deployer"],
            "orchestrator": ["architect", "coder", "tester"]
        }
        
        agent_map = {agent.name: agent for agent in agent_nodes}
        
        for source_name, target_names in dependencies.items():
            source_agents = [agent for agent in agent_nodes if source_name in agent.name.lower()]
            
            for source_agent in source_agents:
                for target_name in target_names:
                    target_agents = [agent for agent in agent_nodes if target_name in agent.name.lower()]
                    
                    for target_agent in target_agents:
                        if source_agent.id != target_agent.id:
                            relationship = GraphRelationship(
                                source_id=source_agent.id,
                                target_id=target_agent.id,
                                relationship_type=RelationshipType.DEPENDS_ON,
                                strength=0.7,
                                confidence=0.8,
                                metadata={
                                    "dependency_type": "workflow",
                                    "reasoning": f"{source_name} typically depends on {target_name}"
                                }
                            )
                            self.knowledge_graph.add_relationship(relationship)
        
        # Create capability-based relationships
        await self._create_capability_based_relationships(agent_nodes)
    
    async def _create_capability_based_relationships(self, agent_nodes: List[AgentNode]) -> None:
        """Create relationships between agents based on shared capabilities"""
        
        # Group agents by capabilities
        capability_groups = {}
        for agent in agent_nodes:
            for capability in agent.capabilities:
                if capability not in capability_groups:
                    capability_groups[capability] = []
                capability_groups[capability].append(agent)
        
        # Create specialization relationships
        for capability, agents in capability_groups.items():
            if len(agents) > 1:
                # Sort by system priority (some systems are more specialized)
                system_priority = {
                    "obelisk": 5,
                    "agency": 4,
                    "meistrocraft": 3,
                    "ai_dev_team": 2,
                    "village": 1
                }
                
                agents.sort(key=lambda a: system_priority.get(a.system_name, 0), reverse=True)
                
                # Create specialization relationships
                for i in range(len(agents) - 1):
                    specialist = agents[i]
                    generalist = agents[i + 1]
                    
                    relationship = GraphRelationship(
                        source_id=specialist.id,
                        target_id=generalist.id,
                        relationship_type=RelationshipType.SPECIALIZES,
                        strength=0.6,
                        confidence=0.7,
                        metadata={
                            "shared_capability": capability,
                            "specialist_system": specialist.system_name,
                            "generalist_system": generalist.system_name
                        }
                    )
                    self.knowledge_graph.add_relationship(relationship)
    
    async def _create_workflow_patterns(self, agent_nodes: List[AgentNode]) -> None:
        """Create workflow pattern nodes based on common agent sequences"""
        
        # Define common workflow patterns
        workflow_patterns = [
            {
                "name": "development_lifecycle",
                "description": "Standard development lifecycle workflow",
                "agents": ["architect", "coder", "tester", "reviewer", "fixer", "deployer"],
                "workflow_type": "sequential"
            },
            {
                "name": "code_review_cycle",
                "description": "Code review and improvement cycle",
                "agents": ["coder", "reviewer", "fixer"],
                "workflow_type": "sequential"
            },
            {
                "name": "testing_pipeline",
                "description": "Comprehensive testing pipeline",
                "agents": ["tester", "quality_checker", "reviewer"],
                "workflow_type": "parallel"
            },
            {
                "name": "architecture_planning",
                "description": "Architecture and planning workflow",
                "agents": ["architect", "orchestrator", "project_manager"],
                "workflow_type": "collaborative"
            }
        ]
        
        for pattern in workflow_patterns:
            # Find actual agents that match the pattern
            pattern_agents = []
            for agent_name in pattern["agents"]:
                matching_agents = [a for a in agent_nodes if agent_name in a.name.lower()]
                if matching_agents:
                    pattern_agents.append(matching_agents[0])  # Take the first match
            
            if pattern_agents:
                workflow = self.knowledge_graph.create_workflow_from_agents(
                    pattern_agents, 
                    pattern["name"]
                )
                workflow.description = pattern["description"]
                workflow.workflow_type = pattern["workflow_type"]
                
                # Update the workflow in the graph
                self.knowledge_graph._persist_node(workflow)
    
    async def update_agent_performance(self, agent_name: str, performance_data: Dict[str, Any]) -> None:
        """Update performance metrics for an agent"""
        agents = self.knowledge_graph.get_agents()
        
        for agent in agents:
            if agent.name == agent_name:
                self.knowledge_graph.update_agent_performance(agent.id, performance_data)
                break
    
    async def get_agent_insights(self, agent_name: str) -> Dict[str, Any]:
        """Get insights about an agent's relationships and capabilities"""
        agents = self.knowledge_graph.get_agents()
        target_agent = None
        
        for agent in agents:
            if agent.name == agent_name:
                target_agent = agent
                break
        
        if not target_agent:
            return {"error": "Agent not found"}
        
        # Get collaborators and dependencies
        collaborators = self.knowledge_graph.find_agent_collaborators(target_agent.id)
        dependencies = self.knowledge_graph.find_agent_dependencies(target_agent.id)
        
        # Get capabilities
        capabilities = []
        for rel in self.knowledge_graph.schema.get_node_relationships(target_agent.id):
            if rel.relationship_type == RelationshipType.HAS_CAPABILITY:
                cap_node = self.knowledge_graph.get_node(rel.target_id)
                if cap_node:
                    capabilities.append(cap_node.name)
        
        return {
            "agent": {
                "name": target_agent.name,
                "type": target_agent.agent_type,
                "system": target_agent.system_name,
                "status": target_agent.status
            },
            "capabilities": capabilities,
            "collaborators": [{"name": c.name, "system": c.system_name} for c in collaborators],
            "dependencies": [{"name": d.name, "system": d.system_name} for d in dependencies],
            "performance": target_agent.performance_metrics
        }