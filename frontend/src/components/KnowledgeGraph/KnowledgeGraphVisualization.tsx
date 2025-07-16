import React, { useEffect, useRef, useCallback, useMemo } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import ForceGraph3D from 'react-force-graph-3d';
import ForceGraph2D from 'react-force-graph-2d';
import { RootState } from '../../store';
import { 
  setSelectedNode, 
  setSelectedRelationship, 
  updateNodePosition,
  setLayoutMode 
} from '../../store/slices/knowledgeGraphSlice';
import type { GraphNode, GraphRelationship } from '../../store/slices/knowledgeGraphSlice';
import { ChevronUpIcon, ChevronDownIcon } from '@heroicons/react/24/outline';

interface ForceGraphNode extends GraphNode {
  x?: number;
  y?: number;
  z?: number;
  fx?: number;
  fy?: number;
  fz?: number;
  color?: string;
  size?: number;
  label?: string;
}

interface ForceGraphLink extends GraphRelationship {
  source: string;
  target: string;
  color?: string;
  width?: number;
  opacity?: number;
}

const KnowledgeGraphVisualization: React.FC = () => {
  const dispatch = useDispatch();
  const fgRef = useRef<any>();
  
  const { 
    filteredData, 
    selectedNode, 
    layoutMode, 
    isLoading 
  } = useSelector((state: RootState) => state.knowledgeGraph);

  // Node styling based on type and system
  const getNodeColor = useCallback((node: GraphNode): string => {
    const nodeTypeColors: Record<string, string> = {
      'agent': '#3B82F6',        // Blue
      'capability': '#10B981',   // Green
      'task': '#F59E0B',         // Amber
      'workflow': '#8B5CF6',     // Purple
      'knowledge': '#EF4444',    // Red
      'dependency': '#6B7280',   // Gray
    };

    const systemColors: Record<string, string> = {
      'agency': '#DC2626',       // Red
      'meistrocraft': '#059669', // Green
      'obelisk': '#7C3AED',      // Purple
      'ai_dev_team': '#2563EB',  // Blue
      'village': '#D97706',      // Orange
    };

    // Use system color for agents, type color for others
    if (node.node_type === 'agent' && node.metadata?.system) {
      return systemColors[node.metadata.system] || nodeTypeColors['agent'];
    }

    return nodeTypeColors[node.node_type] || '#6B7280';
  }, []);

  const getNodeSize = useCallback((node: GraphNode): number => {
    const baseSizes: Record<string, number> = {
      'agent': 12,
      'capability': 8,
      'task': 6,
      'workflow': 10,
      'knowledge': 5,
      'dependency': 4,
    };

    let size = baseSizes[node.node_type] || 6;

    // Scale by importance metrics
    if (node.node_type === 'agent' && node.metadata?.priority) {
      size *= (1 + (node.metadata.priority / 10));
    }

    return size;
  }, []);

  const getLinkColor = useCallback((link: GraphRelationship): string => {
    const relationshipColors: Record<string, string> = {
      'has_capability': '#10B981',    // Green
      'depends_on': '#EF4444',        // Red
      'collaborates_with': '#3B82F6', // Blue
      'creates': '#F59E0B',           // Amber
      'uses_knowledge': '#8B5CF6',    // Purple
      'inherits_from': '#6B7280',     // Gray
      'requires': '#DC2626',          // Dark Red
      'produces': '#059669',          // Dark Green
      'executes': '#7C3AED',          // Dark Purple
      'follows': '#2563EB',           // Dark Blue
      'specializes': '#D97706',       // Orange
    };

    return relationshipColors[link.relationship_type] || '#6B7280';
  }, []);

  const getLinkWidth = useCallback((link: GraphRelationship): number => {
    return Math.max(1, link.strength * 4);
  }, []);

  // Convert data for force graph
  const graphData = useMemo(() => {
    if (!filteredData) return { nodes: [], links: [] };

    const nodes: ForceGraphNode[] = filteredData.nodes.map(node => ({
      ...node,
      color: getNodeColor(node),
      size: getNodeSize(node),
      label: node.name,
      // Preserve existing positions if available
      ...(node.metadata?.position && {
        x: node.metadata.position.x,
        y: node.metadata.position.y,
        z: node.metadata.position.z,
      }),
    }));

    const links: ForceGraphLink[] = filteredData.relationships.map(rel => ({
      ...rel,
      source: rel.source_id,
      target: rel.target_id,
      color: getLinkColor(rel),
      width: getLinkWidth(rel),
      opacity: rel.confidence,
    }));

    return { nodes, links };
  }, [filteredData, getNodeColor, getNodeSize, getLinkColor, getLinkWidth]);

  // Event handlers
  const handleNodeClick = useCallback((node: ForceGraphNode) => {
    dispatch(setSelectedNode(node));
    
    // Focus camera on node
    if (fgRef.current && layoutMode === '3d') {
      const distance = 200;
      const distRatio = 1 + distance / Math.hypot(node.x || 0, node.y || 0, node.z || 0);
      
      fgRef.current.cameraPosition(
        { x: (node.x || 0) * distRatio, y: (node.y || 0) * distRatio, z: (node.z || 0) * distRatio },
        node,
        3000
      );
    }
  }, [dispatch, layoutMode]);

  const handleLinkClick = useCallback((link: ForceGraphLink) => {
    dispatch(setSelectedRelationship(link));
  }, [dispatch]);

  const handleNodeDrag = useCallback((node: ForceGraphNode) => {
    dispatch(updateNodePosition({
      nodeId: node.id,
      x: node.x || 0,
      y: node.y || 0,
      z: node.z || 0,
    }));
  }, [dispatch]);

  // Node label rendering
  const nodeLabel = useCallback((node: ForceGraphNode): string => {
    return `
      <div style="
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px;
        border-radius: 4px;
        font-size: 12px;
        max-width: 200px;
      ">
        <div style="font-weight: bold; margin-bottom: 4px;">${node.name}</div>
        <div style="font-size: 10px; opacity: 0.8;">Type: ${node.node_type}</div>
        ${node.metadata?.system ? `<div style="font-size: 10px; opacity: 0.8;">System: ${node.metadata.system}</div>` : ''}
        <div style="font-size: 10px; opacity: 0.8;">${node.description}</div>
      </div>
    `;
  }, []);

  // Link label rendering
  const linkLabel = useCallback((link: ForceGraphLink): string => {
    return `
      <div style="
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 6px;
        border-radius: 4px;
        font-size: 11px;
      ">
        <div style="font-weight: bold;">${link.relationship_type.replace(/_/g, ' ')}</div>
        <div style="font-size: 9px;">Strength: ${(link.strength * 100).toFixed(0)}%</div>
        <div style="font-size: 9px;">Confidence: ${(link.confidence * 100).toFixed(0)}%</div>
      </div>
    `;
  }, []);

  // Auto-resize
  useEffect(() => {
    const handleResize = () => {
      if (fgRef.current) {
        fgRef.current.refresh();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-lg">Loading knowledge graph...</span>
      </div>
    );
  }

  // No data state
  if (!filteredData || filteredData.nodes.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <div className="text-xl mb-2">No graph data available</div>
          <div className="text-sm">Try adjusting your filters or populate the graph first</div>
        </div>
      </div>
    );
  }

  const commonProps = {
    ref: fgRef,
    graphData,
    nodeId: 'id',
    nodeLabel,
    nodeColor: (node: ForceGraphNode) => node.color,
    nodeVal: (node: ForceGraphNode) => node.size,
    onNodeClick: handleNodeClick,
    onNodeDrag: handleNodeDrag,
    linkSource: 'source',
    linkTarget: 'target',
    linkLabel,
    linkColor: (link: ForceGraphLink) => link.color,
    linkWidth: (link: ForceGraphLink) => link.width,
    linkOpacity: (link: ForceGraphLink) => link.opacity,
    onLinkClick: handleLinkClick,
    backgroundColor: '#0F172A',
    linkDirectionalArrowLength: 3.5,
    linkDirectionalArrowRelPos: 1,
    linkCurvature: 0.1,
    enableNodeDrag: true,
    enableZoomInteraction: true,
    enablePanInteraction: true,
    cooldownTicks: 100,
    warmupTicks: 100,
  };

  return (
    <div className="relative w-full h-full">
      {/* Layout Mode Switcher */}
      <div className="absolute top-4 right-4 z-10 flex bg-gray-800 rounded-lg p-1">
        <button
          onClick={() => dispatch(setLayoutMode('2d'))}
          className={`px-3 py-1 text-sm rounded ${
            layoutMode === '2d' 
              ? 'bg-blue-600 text-white' 
              : 'text-gray-300 hover:text-white'
          }`}
        >
          2D
        </button>
        <button
          onClick={() => dispatch(setLayoutMode('3d'))}
          className={`px-3 py-1 text-sm rounded ${
            layoutMode === '3d' 
              ? 'bg-blue-600 text-white' 
              : 'text-gray-300 hover:text-white'
          }`}
        >
          3D
        </button>
      </div>

      {/* Node Count Badge */}
      <div className="absolute top-4 left-4 z-10 bg-gray-800 rounded-lg px-3 py-2 text-sm text-white">
        {filteredData.nodes.length} nodes, {filteredData.relationships.length} relationships
      </div>

      {/* Selected Node Badge */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 z-10 bg-gray-800 rounded-lg px-3 py-2 text-sm text-white max-w-sm">
          <div className="font-semibold">{selectedNode.name}</div>
          <div className="text-xs text-gray-300">{selectedNode.node_type} • {selectedNode.metadata?.system}</div>
        </div>
      )}

      {/* Force Graph */}
      {layoutMode === '2d' ? (
        <ForceGraph2D
          {...commonProps}
          width={window.innerWidth}
          height={window.innerHeight - 64} // Account for header
        />
      ) : (
        <ForceGraph3D
          {...commonProps}
          width={window.innerWidth}
          height={window.innerHeight - 64} // Account for header
        />
      )}
    </div>
  );
};

export default KnowledgeGraphVisualization;