import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { setFilters, clearFilters } from '../../store/slices/knowledgeGraphSlice';
import { 
  FunnelIcon, 
  XMarkIcon, 
  ChevronDownIcon,
  MagnifyingGlassIcon 
} from '@heroicons/react/24/outline';

const KnowledgeGraphFilters: React.FC = () => {
  const dispatch = useDispatch();
  const { filters, data } = useSelector((state: RootState) => state.knowledgeGraph);

  // Extract unique values from data for filter options
  const filterOptions = React.useMemo(() => {
    if (!data) return { nodeTypes: [], relationshipTypes: [], systems: [] };

    const nodeTypes = [...new Set(data.nodes.map(node => node.node_type))].sort();
    const relationshipTypes = [...new Set(data.relationships.map(rel => rel.relationship_type))].sort();
    const systems = [...new Set(data.nodes
      .map(node => node.metadata?.system)
      .filter(Boolean))].sort();

    return { nodeTypes, relationshipTypes, systems };
  }, [data]);

  const hasActiveFilters = React.useMemo(() => {
    return filters.nodeTypes.length > 0 ||
           filters.relationshipTypes.length > 0 ||
           filters.systems.length > 0 ||
           filters.searchQuery.length > 0 ||
           filters.minConfidence > 0;
  }, [filters]);

  const handleNodeTypeToggle = (nodeType: string) => {
    const newNodeTypes = filters.nodeTypes.includes(nodeType)
      ? filters.nodeTypes.filter(type => type !== nodeType)
      : [...filters.nodeTypes, nodeType];
    
    dispatch(setFilters({ nodeTypes: newNodeTypes }));
  };

  const handleRelationshipTypeToggle = (relType: string) => {
    const newRelTypes = filters.relationshipTypes.includes(relType)
      ? filters.relationshipTypes.filter(type => type !== relType)
      : [...filters.relationshipTypes, relType];
    
    dispatch(setFilters({ relationshipTypes: newRelTypes }));
  };

  const handleSystemToggle = (system: string) => {
    const newSystems = filters.systems.includes(system)
      ? filters.systems.filter(sys => sys !== system)
      : [...filters.systems, system];
    
    dispatch(setFilters({ systems: newSystems }));
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setFilters({ searchQuery: e.target.value }));
  };

  const handleConfidenceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setFilters({ minConfidence: parseFloat(e.target.value) }));
  };

  const handleClearFilters = () => {
    dispatch(clearFilters());
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FunnelIcon className="h-5 w-5 text-gray-400" />
          <h3 className="text-lg font-semibold text-white">Filters</h3>
          {hasActiveFilters && (
            <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
              Active
            </span>
          )}
        </div>
        {hasActiveFilters && (
          <button
            onClick={handleClearFilters}
            className="flex items-center gap-1 text-gray-400 hover:text-white text-sm"
          >
            <XMarkIcon className="h-4 w-4" />
            Clear All
          </button>
        )}
      </div>

      {/* Search */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">Search</label>
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={filters.searchQuery}
            onChange={handleSearchChange}
            placeholder="Search nodes..."
            className="w-full pl-10 pr-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Confidence Threshold */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">
          Min Confidence: {Math.round(filters.minConfidence * 100)}%
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={filters.minConfidence}
          onChange={handleConfidenceChange}
          className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
        />
      </div>

      {/* Node Types */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">Node Types</label>
        <div className="space-y-1 max-h-32 overflow-y-auto">
          {filterOptions.nodeTypes.map(nodeType => (
            <label key={nodeType} className="flex items-center">
              <input
                type="checkbox"
                checked={filters.nodeTypes.includes(nodeType)}
                onChange={() => handleNodeTypeToggle(nodeType)}
                className="mr-2 rounded border-gray-600 text-blue-600 focus:ring-blue-500 focus:ring-offset-gray-800"
              />
              <span className="text-sm text-gray-300 capitalize">
                {nodeType.replace(/_/g, ' ')}
              </span>
              <span className="ml-auto text-xs text-gray-500">
                {data?.nodes.filter(n => n.node_type === nodeType).length || 0}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Systems */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">Systems</label>
        <div className="space-y-1 max-h-32 overflow-y-auto">
          {filterOptions.systems.map(system => (
            <label key={system} className="flex items-center">
              <input
                type="checkbox"
                checked={filters.systems.includes(system)}
                onChange={() => handleSystemToggle(system)}
                className="mr-2 rounded border-gray-600 text-blue-600 focus:ring-blue-500 focus:ring-offset-gray-800"
              />
              <span className="text-sm text-gray-300 capitalize">
                {system.replace(/_/g, ' ')}
              </span>
              <span className="ml-auto text-xs text-gray-500">
                {data?.nodes.filter(n => n.metadata?.system === system).length || 0}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Relationship Types */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">Relationship Types</label>
        <div className="space-y-1 max-h-32 overflow-y-auto">
          {filterOptions.relationshipTypes.map(relType => (
            <label key={relType} className="flex items-center">
              <input
                type="checkbox"
                checked={filters.relationshipTypes.includes(relType)}
                onChange={() => handleRelationshipTypeToggle(relType)}
                className="mr-2 rounded border-gray-600 text-blue-600 focus:ring-blue-500 focus:ring-offset-gray-800"
              />
              <span className="text-sm text-gray-300 capitalize">
                {relType.replace(/_/g, ' ')}
              </span>
              <span className="ml-auto text-xs text-gray-500">
                {data?.relationships.filter(r => r.relationship_type === relType).length || 0}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Filter Summary */}
      {hasActiveFilters && (
        <div className="mt-4 p-3 bg-gray-700 rounded-md">
          <div className="text-sm font-medium text-gray-300 mb-2">Active Filters:</div>
          <div className="space-y-1 text-xs text-gray-400">
            {filters.nodeTypes.length > 0 && (
              <div>Node Types: {filters.nodeTypes.join(', ')}</div>
            )}
            {filters.systems.length > 0 && (
              <div>Systems: {filters.systems.join(', ')}</div>
            )}
            {filters.relationshipTypes.length > 0 && (
              <div>Relationships: {filters.relationshipTypes.slice(0, 2).join(', ')}{filters.relationshipTypes.length > 2 ? '...' : ''}</div>
            )}
            {filters.searchQuery && (
              <div>Search: "{filters.searchQuery}"</div>
            )}
            {filters.minConfidence > 0 && (
              <div>Min Confidence: {Math.round(filters.minConfidence * 100)}%</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default KnowledgeGraphFilters;