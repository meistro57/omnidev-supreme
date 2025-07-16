"""
Knowledge Graph Schema for OmniDev Supreme

This module defines the data structures and relationships for the knowledge graph system
that models agent interactions, capabilities, and workflows.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class NodeType(Enum):
    """Types of nodes in the knowledge graph"""
    AGENT = "agent"
    CAPABILITY = "capability"
    TASK = "task"
    WORKFLOW = "workflow"
    KNOWLEDGE = "knowledge"
    DEPENDENCY = "dependency"
    PERFORMANCE = "performance"


class RelationshipType(Enum):
    """Types of relationships between nodes"""
    HAS_CAPABILITY = "has_capability"
    DEPENDS_ON = "depends_on"
    COLLABORATES_WITH = "collaborates_with"
    CREATES = "creates"
    USES_KNOWLEDGE = "uses_knowledge"
    INHERITS_FROM = "inherits_from"
    REQUIRES = "requires"
    PRODUCES = "produces"
    EXECUTES = "executes"
    FOLLOWS = "follows"
    SPECIALIZES = "specializes"
    COMPETES_WITH = "competes_with"


class CapabilityCategory(Enum):
    """Categories of agent capabilities"""
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    ANALYSIS = "analysis"
    COORDINATION = "coordination"
    CREATIVE = "creative"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    MANAGEMENT = "management"
    COMMUNICATION = "communication"


@dataclass
class GraphNode:
    """Base class for all knowledge graph nodes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: NodeType = NodeType.AGENT
    name: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation"""
        return {
            "id": self.id,
            "node_type": self.node_type.value,
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": list(self.tags)
        }


@dataclass
class AgentNode(GraphNode):
    """Node representing an agent in the knowledge graph"""
    agent_type: str = ""
    system_name: str = ""  # agency, meistrocraft, obelisk, ai_dev_team, village
    capabilities: List[str] = field(default_factory=list)
    priority: int = 5
    max_concurrent_tasks: int = 3
    timeout_seconds: int = 300
    retry_count: int = 3
    model_requirements: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    status: str = "IDLE"
    
    def __post_init__(self):
        self.node_type = NodeType.AGENT


@dataclass
class CapabilityNode(GraphNode):
    """Node representing a capability in the knowledge graph"""
    category: CapabilityCategory = CapabilityCategory.DEVELOPMENT
    level: int = 1  # 1=basic, 2=intermediate, 3=advanced, 4=expert
    prerequisites: List[str] = field(default_factory=list)
    complexity_score: float = 0.0
    usage_frequency: int = 0
    
    def __post_init__(self):
        self.node_type = NodeType.CAPABILITY


@dataclass
class TaskNode(GraphNode):
    """Node representing a task in the knowledge graph"""
    task_type: str = ""
    complexity: str = "MEDIUM"  # SIMPLE, MEDIUM, COMPLEX, EXPERT
    required_capabilities: List[str] = field(default_factory=list)
    estimated_duration: int = 0  # seconds
    priority: int = 5
    session_id: Optional[str] = None
    workflow_id: Optional[str] = None
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = NodeType.TASK


@dataclass
class WorkflowNode(GraphNode):
    """Node representing a workflow pattern in the knowledge graph"""
    workflow_type: str = ""  # sequential, parallel, conditional, adaptive
    stages: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    average_duration: float = 0.0
    usage_count: int = 0
    template: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = NodeType.WORKFLOW


@dataclass
class KnowledgeNode(GraphNode):
    """Node representing knowledge in the graph"""
    knowledge_type: str = ""  # code, documentation, pattern, solution
    content: str = ""
    confidence_score: float = 0.0
    source_agent: Optional[str] = None
    validation_status: str = "UNVALIDATED"  # VALIDATED, UNVALIDATED, DEPRECATED
    access_count: int = 0
    
    def __post_init__(self):
        self.node_type = NodeType.KNOWLEDGE


@dataclass
class GraphRelationship:
    """Represents a relationship between two nodes in the knowledge graph"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    target_id: str = ""
    relationship_type: RelationshipType = RelationshipType.DEPENDS_ON
    strength: float = 1.0  # 0.0 to 1.0
    confidence: float = 1.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary representation"""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "strength": self.strength,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class GraphPath:
    """Represents a path through the knowledge graph"""
    nodes: List[GraphNode] = field(default_factory=list)
    relationships: List[GraphRelationship] = field(default_factory=list)
    total_strength: float = 0.0
    path_length: int = 0
    
    def calculate_strength(self) -> float:
        """Calculate the total strength of the path"""
        if not self.relationships:
            return 0.0
        
        total = sum(rel.strength * rel.confidence for rel in self.relationships)
        return total / len(self.relationships)


@dataclass
class KnowledgeGraphSchema:
    """Complete schema definition for the knowledge graph"""
    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    relationships: Dict[str, GraphRelationship] = field(default_factory=dict)
    node_indices: Dict[NodeType, Set[str]] = field(default_factory=dict)
    relationship_indices: Dict[RelationshipType, Set[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize indices"""
        for node_type in NodeType:
            self.node_indices[node_type] = set()
        for rel_type in RelationshipType:
            self.relationship_indices[rel_type] = set()
    
    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph"""
        self.nodes[node.id] = node
        self.node_indices[node.node_type].add(node.id)
        node.updated_at = datetime.now()
    
    def add_relationship(self, relationship: GraphRelationship) -> None:
        """Add a relationship to the graph"""
        self.relationships[relationship.id] = relationship
        self.relationship_indices[relationship.relationship_type].add(relationship.id)
        relationship.updated_at = datetime.now()
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        """Get all nodes of a specific type"""
        node_ids = self.node_indices.get(node_type, set())
        return [self.nodes[node_id] for node_id in node_ids if node_id in self.nodes]
    
    def get_relationships_by_type(self, rel_type: RelationshipType) -> List[GraphRelationship]:
        """Get all relationships of a specific type"""
        rel_ids = self.relationship_indices.get(rel_type, set())
        return [self.relationships[rel_id] for rel_id in rel_ids if rel_id in self.relationships]
    
    def get_node_relationships(self, node_id: str) -> List[GraphRelationship]:
        """Get all relationships involving a specific node"""
        return [
            rel for rel in self.relationships.values()
            if rel.source_id == node_id or rel.target_id == node_id
        ]
    
    def find_path(self, source_id: str, target_id: str, max_depth: int = 5) -> Optional[GraphPath]:
        """Find a path between two nodes using BFS"""
        if source_id == target_id:
            return GraphPath(nodes=[self.nodes[source_id]], path_length=0)
        
        visited = set()
        queue = [(source_id, [source_id], [])]
        
        while queue:
            current_id, path, relationships = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            # Find all relationships from current node
            for rel in self.get_node_relationships(current_id):
                next_id = rel.target_id if rel.source_id == current_id else rel.source_id
                
                if next_id == target_id:
                    # Found target
                    final_path = path + [next_id]
                    final_relationships = relationships + [rel]
                    
                    graph_path = GraphPath(
                        nodes=[self.nodes[node_id] for node_id in final_path],
                        relationships=final_relationships,
                        path_length=len(final_path) - 1
                    )
                    graph_path.total_strength = graph_path.calculate_strength()
                    return graph_path
                
                if next_id not in visited:
                    queue.append((next_id, path + [next_id], relationships + [rel]))
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph"""
        return {
            "total_nodes": len(self.nodes),
            "total_relationships": len(self.relationships),
            "nodes_by_type": {
                node_type.value: len(self.node_indices[node_type])
                for node_type in NodeType
            },
            "relationships_by_type": {
                rel_type.value: len(self.relationship_indices[rel_type])
                for rel_type in RelationshipType
            }
        }