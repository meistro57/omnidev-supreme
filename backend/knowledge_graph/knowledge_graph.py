"""
Knowledge Graph Implementation for OmniDev Supreme

This module provides the core knowledge graph implementation with in-memory storage,
graph operations, and agent relationship management.
"""

import json
import sqlite3
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import logging
from pathlib import Path

from .schema import (
    NodeType,
    RelationshipType,
    CapabilityCategory,
    GraphNode,
    AgentNode,
    CapabilityNode,
    TaskNode,
    WorkflowNode,
    KnowledgeNode,
    GraphRelationship,
    GraphPath,
    KnowledgeGraphSchema,
)

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    Core knowledge graph implementation with persistence and querying capabilities
    """
    
    def __init__(self, db_path: str = "knowledge_graph.db"):
        self.db_path = db_path
        self.schema = KnowledgeGraphSchema()
        self._init_database()
        self._load_from_database()
    
    def _init_database(self) -> None:
        """Initialize SQLite database for persistence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                metadata TEXT,
                created_at TEXT,
                updated_at TEXT,
                tags TEXT
            )
        ''')
        
        # Create relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL,
                confidence REAL,
                metadata TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (source_id) REFERENCES nodes (id),
                FOREIGN KEY (target_id) REFERENCES nodes (id)
            )
        ''')
        
        # Create indices for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_name ON nodes(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_id)')
        
        conn.commit()
        conn.close()
    
    def _load_from_database(self) -> None:
        """Load existing graph data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load nodes
        cursor.execute('SELECT * FROM nodes')
        for row in cursor.fetchall():
            node_data = {
                'id': row[0],
                'node_type': row[1],
                'name': row[2],
                'description': row[3] or "",
                'metadata': json.loads(row[4]) if row[4] else {},
                'created_at': datetime.fromisoformat(row[5]) if row[5] else datetime.now(),
                'updated_at': datetime.fromisoformat(row[6]) if row[6] else datetime.now(),
                'tags': set(json.loads(row[7])) if row[7] else set()
            }
            
            # Create appropriate node type
            node_type = NodeType(row[1])
            if node_type == NodeType.AGENT:
                node = AgentNode(**node_data)
            elif node_type == NodeType.CAPABILITY:
                node = CapabilityNode(**node_data)
            elif node_type == NodeType.TASK:
                node = TaskNode(**node_data)
            elif node_type == NodeType.WORKFLOW:
                node = WorkflowNode(**node_data)
            elif node_type == NodeType.KNOWLEDGE:
                node = KnowledgeNode(**node_data)
            else:
                node = GraphNode(**node_data)
            
            self.schema.add_node(node)
        
        # Load relationships
        cursor.execute('SELECT * FROM relationships')
        for row in cursor.fetchall():
            relationship = GraphRelationship(
                id=row[0],
                source_id=row[1],
                target_id=row[2],
                relationship_type=RelationshipType(row[3]),
                strength=row[4] or 1.0,
                confidence=row[5] or 1.0,
                metadata=json.loads(row[6]) if row[6] else {},
                created_at=datetime.fromisoformat(row[7]) if row[7] else datetime.now(),
                updated_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now()
            )
            self.schema.add_relationship(relationship)
        
        conn.close()
        logger.info(f"Loaded {len(self.schema.nodes)} nodes and {len(self.schema.relationships)} relationships")
    
    def add_node(self, node: GraphNode, persist: bool = True) -> None:
        """Add a node to the knowledge graph"""
        self.schema.add_node(node)
        
        if persist:
            self._persist_node(node)
        
        logger.debug(f"Added node: {node.name} ({node.node_type.value})")
    
    def add_relationship(self, relationship: GraphRelationship, persist: bool = True) -> None:
        """Add a relationship to the knowledge graph"""
        self.schema.add_relationship(relationship)
        
        if persist:
            self._persist_relationship(relationship)
        
        logger.debug(f"Added relationship: {relationship.source_id} -> {relationship.target_id} ({relationship.relationship_type.value})")
    
    def _persist_node(self, node: GraphNode) -> None:
        """Persist a node to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO nodes 
            (id, node_type, name, description, metadata, created_at, updated_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            node.id,
            node.node_type.value,
            node.name,
            node.description,
            json.dumps(node.metadata),
            node.created_at.isoformat(),
            node.updated_at.isoformat(),
            json.dumps(list(node.tags))
        ))
        
        conn.commit()
        conn.close()
    
    def _persist_relationship(self, relationship: GraphRelationship) -> None:
        """Persist a relationship to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO relationships
            (id, source_id, target_id, relationship_type, strength, confidence, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            relationship.id,
            relationship.source_id,
            relationship.target_id,
            relationship.relationship_type.value,
            relationship.strength,
            relationship.confidence,
            json.dumps(relationship.metadata),
            relationship.created_at.isoformat(),
            relationship.updated_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID"""
        return self.schema.nodes.get(node_id)
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        """Get all nodes of a specific type"""
        return self.schema.get_nodes_by_type(node_type)
    
    def get_agents(self) -> List[AgentNode]:
        """Get all agent nodes"""
        return [node for node in self.get_nodes_by_type(NodeType.AGENT) if isinstance(node, AgentNode)]
    
    def get_capabilities(self) -> List[CapabilityNode]:
        """Get all capability nodes"""
        return [node for node in self.get_nodes_by_type(NodeType.CAPABILITY) if isinstance(node, CapabilityNode)]
    
    def find_agents_by_capability(self, capability: str) -> List[AgentNode]:
        """Find agents that have a specific capability"""
        agents = []
        for agent in self.get_agents():
            if capability in agent.capabilities:
                agents.append(agent)
        return agents
    
    def find_agent_collaborators(self, agent_id: str) -> List[AgentNode]:
        """Find agents that collaborate with the given agent"""
        collaborators = []
        for rel in self.schema.get_node_relationships(agent_id):
            if rel.relationship_type == RelationshipType.COLLABORATES_WITH:
                other_id = rel.target_id if rel.source_id == agent_id else rel.source_id
                other_node = self.get_node(other_id)
                if isinstance(other_node, AgentNode):
                    collaborators.append(other_node)
        return collaborators
    
    def find_agent_dependencies(self, agent_id: str) -> List[AgentNode]:
        """Find agents that the given agent depends on"""
        dependencies = []
        for rel in self.schema.get_node_relationships(agent_id):
            if rel.relationship_type == RelationshipType.DEPENDS_ON and rel.source_id == agent_id:
                target_node = self.get_node(rel.target_id)
                if isinstance(target_node, AgentNode):
                    dependencies.append(target_node)
        return dependencies
    
    def get_optimal_agent_sequence(self, task_capabilities: List[str]) -> List[AgentNode]:
        """
        Find the optimal sequence of agents to handle a task based on capabilities
        and dependencies
        """
        # Find all agents that can handle the required capabilities
        capable_agents = set()
        for capability in task_capabilities:
            agents = self.find_agents_by_capability(capability)
            capable_agents.update(agents)
        
        if not capable_agents:
            return []
        
        # Build dependency graph for capable agents
        agent_deps = {}
        for agent in capable_agents:
            deps = self.find_agent_dependencies(agent.id)
            agent_deps[agent.id] = [dep.id for dep in deps if dep in capable_agents]
        
        # Topological sort to find optimal sequence
        sequence = []
        visited = set()
        temp_visited = set()
        
        def dfs(agent_id: str):
            if agent_id in temp_visited:
                return  # Cycle detected, skip
            if agent_id in visited:
                return
            
            temp_visited.add(agent_id)
            for dep_id in agent_deps.get(agent_id, []):
                dfs(dep_id)
            
            temp_visited.remove(agent_id)
            visited.add(agent_id)
            
            agent = self.get_node(agent_id)
            if isinstance(agent, AgentNode):
                sequence.append(agent)
        
        for agent in capable_agents:
            if agent.id not in visited:
                dfs(agent.id)
        
        return sequence
    
    def get_agent_recommendations(self, task: Dict[str, Any]) -> List[Tuple[AgentNode, float]]:
        """
        Get agent recommendations for a task with confidence scores
        """
        task_content = task.get("content", "").lower()
        task_type = task.get("type", "")
        required_capabilities = task.get("capabilities", [])
        
        recommendations = []
        
        for agent in self.get_agents():
            score = 0.0
            
            # Score based on capabilities match
            if required_capabilities:
                matched_caps = sum(1 for cap in required_capabilities if cap in agent.capabilities)
                score += (matched_caps / len(required_capabilities)) * 0.4
            
            # Score based on agent type relevance
            if task_type and task_type.lower() in agent.agent_type.lower():
                score += 0.3
            
            # Score based on content keywords
            keyword_matches = sum(1 for cap in agent.capabilities if cap.lower() in task_content)
            if agent.capabilities:
                score += (keyword_matches / len(agent.capabilities)) * 0.2
            
            # Score based on performance metrics
            if agent.performance_metrics:
                success_rate = agent.performance_metrics.get("success_rate", 0.5)
                score += success_rate * 0.1
            
            if score > 0:
                recommendations.append((agent, score))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations
    
    def update_agent_performance(self, agent_id: str, performance_data: Dict[str, Any]) -> None:
        """Update agent performance metrics"""
        agent = self.get_node(agent_id)
        if isinstance(agent, AgentNode):
            agent.performance_metrics.update(performance_data)
            agent.updated_at = datetime.now()
            self._persist_node(agent)
    
    def create_workflow_from_agents(self, agents: List[AgentNode], workflow_name: str) -> WorkflowNode:
        """Create a workflow node from a sequence of agents"""
        workflow = WorkflowNode(
            name=workflow_name,
            description=f"Workflow with {len(agents)} agents",
            workflow_type="sequential",
            stages=[agent.name for agent in agents]
        )
        
        self.add_node(workflow)
        
        # Create relationships between workflow and agents
        for agent in agents:
            rel = GraphRelationship(
                source_id=workflow.id,
                target_id=agent.id,
                relationship_type=RelationshipType.EXECUTES,
                strength=1.0,
                confidence=1.0
            )
            self.add_relationship(rel)
        
        return workflow
    
    def export_to_json(self, file_path: str) -> None:
        """Export the knowledge graph to JSON format"""
        data = {
            "nodes": {node_id: node.to_dict() for node_id, node in self.schema.nodes.items()},
            "relationships": {rel_id: rel.to_dict() for rel_id, rel in self.schema.relationships.items()},
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "statistics": self.schema.get_statistics()
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported knowledge graph to {file_path}")
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the knowledge graph"""
        stats = self.schema.get_statistics()
        
        # Add agent-specific statistics
        agents = self.get_agents()
        if agents:
            stats["agent_systems"] = {}
            for agent in agents:
                system = agent.system_name
                if system not in stats["agent_systems"]:
                    stats["agent_systems"][system] = 0
                stats["agent_systems"][system] += 1
            
            stats["agent_types"] = {}
            for agent in agents:
                agent_type = agent.agent_type
                if agent_type not in stats["agent_types"]:
                    stats["agent_types"][agent_type] = 0
                stats["agent_types"][agent_type] += 1
        
        # Add capability statistics
        capabilities = self.get_capabilities()
        if capabilities:
            stats["capability_categories"] = {}
            for cap in capabilities:
                category = cap.category.value
                if category not in stats["capability_categories"]:
                    stats["capability_categories"][category] = 0
                stats["capability_categories"][category] += 1
        
        return stats