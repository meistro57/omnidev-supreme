import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { 
  fetchKnowledgeGraph, 
  analyzeAndPopulateGraph,
  toggleDetails,
  clearSelection 
} from '../store/slices/knowledgeGraphSlice';
import KnowledgeGraphVisualization from '../components/KnowledgeGraph/KnowledgeGraphVisualization';
import KnowledgeGraphFilters from '../components/KnowledgeGraph/KnowledgeGraphFilters';
import { 
  PlayIcon, 
  ArrowPathIcon, 
  InformationCircleIcon,
  XMarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentArrowDownIcon,
  ChartBarIcon,
  CpuChipIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline';

const KnowledgeGraph: React.FC = () => {
  const dispatch = useDispatch();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [statsOpen, setStatsOpen] = useState(false);
  
  const { 
    data, 
    filteredData, 
    selectedNode, 
    selectedRelationship, 
    isLoading, 
    error, 
    lastUpdated,
    showDetails 
  } = useSelector((state: RootState) => state.knowledgeGraph);

  // Load knowledge graph on component mount
  useEffect(() => {
    dispatch(fetchKnowledgeGraph() as any);
  }, [dispatch]);

  const handleAnalyzeAndPopulate = async () => {
    await dispatch(analyzeAndPopulateGraph() as any);
    dispatch(fetchKnowledgeGraph() as any);
  };

  const handleRefresh = () => {
    dispatch(fetchKnowledgeGraph() as any);
  };

  const handleExport = () => {
    // TODO: Implement export functionality
    console.log('Export functionality to be implemented');
  };

  const renderSelectedNodeDetails = () => {
    if (!selectedNode) return null;

    return (
      <div className="bg-gray-800 rounded-lg p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Node Details</h3>
          <button
            onClick={() => dispatch(clearSelection())}
            className="text-gray-400 hover:text-white"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>

        <div className="space-y-2">
          <div>
            <span className="text-sm font-medium text-gray-300">Name:</span>
            <div className="text-white">{selectedNode.name}</div>
          </div>

          <div>
            <span className="text-sm font-medium text-gray-300">Type:</span>
            <div className="text-white capitalize">{selectedNode.node_type.replace(/_/g, ' ')}</div>
          </div>

          {selectedNode.description && (
            <div>
              <span className="text-sm font-medium text-gray-300">Description:</span>
              <div className="text-white text-sm">{selectedNode.description}</div>
            </div>
          )}

          {selectedNode.metadata?.system && (
            <div>
              <span className="text-sm font-medium text-gray-300">System:</span>
              <div className="text-white capitalize">{selectedNode.metadata.system.replace(/_/g, ' ')}</div>
            </div>
          )}

          {selectedNode.tags && selectedNode.tags.length > 0 && (
            <div>
              <span className="text-sm font-medium text-gray-300">Tags:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {selectedNode.tags.map(tag => (
                  <span key={tag} className="bg-blue-600 text-white text-xs px-2 py-1 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {selectedNode.metadata && Object.keys(selectedNode.metadata).length > 0 && (
            <div>
              <span className="text-sm font-medium text-gray-300">Metadata:</span>
              <div className="bg-gray-700 rounded p-2 mt-1">
                <pre className="text-xs text-gray-300 whitespace-pre-wrap">
                  {JSON.stringify(selectedNode.metadata, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderSelectedRelationshipDetails = () => {
    if (!selectedRelationship) return null;

    return (
      <div className="bg-gray-800 rounded-lg p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Relationship Details</h3>
          <button
            onClick={() => dispatch(clearSelection())}
            className="text-gray-400 hover:text-white"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>

        <div className="space-y-2">
          <div>
            <span className="text-sm font-medium text-gray-300">Type:</span>
            <div className="text-white capitalize">{selectedRelationship.relationship_type.replace(/_/g, ' ')}</div>
          </div>

          <div>
            <span className="text-sm font-medium text-gray-300">Strength:</span>
            <div className="text-white">{(selectedRelationship.strength * 100).toFixed(1)}%</div>
          </div>

          <div>
            <span className="text-sm font-medium text-gray-300">Confidence:</span>
            <div className="text-white">{(selectedRelationship.confidence * 100).toFixed(1)}%</div>
          </div>

          {selectedRelationship.metadata && Object.keys(selectedRelationship.metadata).length > 0 && (
            <div>
              <span className="text-sm font-medium text-gray-300">Metadata:</span>
              <div className="bg-gray-700 rounded p-2 mt-1">
                <pre className="text-xs text-gray-300 whitespace-pre-wrap">
                  {JSON.stringify(selectedRelationship.metadata, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderStatistics = () => {
    if (!data) return null;

    const stats = data.statistics || {};

    return (
      <div className="bg-gray-800 rounded-lg p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Statistics</h3>
          <button
            onClick={() => setStatsOpen(!statsOpen)}
            className="text-gray-400 hover:text-white"
          >
            <ChartBarIcon className="h-5 w-5" />
          </button>
        </div>

        {statsOpen && (
          <div className="space-y-2">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-700 rounded p-3">
                <div className="text-2xl font-bold text-white">{data.nodes.length}</div>
                <div className="text-sm text-gray-300">Total Nodes</div>
              </div>
              <div className="bg-gray-700 rounded p-3">
                <div className="text-2xl font-bold text-white">{data.relationships.length}</div>
                <div className="text-sm text-gray-300">Total Relationships</div>
              </div>
            </div>

            {stats.nodes_by_type && (
              <div>
                <span className="text-sm font-medium text-gray-300">Nodes by Type:</span>
                <div className="mt-1 space-y-1">
                  {Object.entries(stats.nodes_by_type).map(([type, count]) => (
                    <div key={type} className="flex justify-between text-sm">
                      <span className="text-gray-300 capitalize">{type.replace(/_/g, ' ')}</span>
                      <span className="text-white">{count as number}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {stats.relationships_by_type && (
              <div>
                <span className="text-sm font-medium text-gray-300">Relationships by Type:</span>
                <div className="mt-1 space-y-1 max-h-32 overflow-y-auto">
                  {Object.entries(stats.relationships_by_type).map(([type, count]) => (
                    <div key={type} className="flex justify-between text-sm">
                      <span className="text-gray-300 capitalize">{type.replace(/_/g, ' ')}</span>
                      <span className="text-white">{count as number}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex h-full bg-gray-900">
      {/* Sidebar */}
      <div 
        className={`${
          sidebarOpen ? 'w-80' : 'w-0'
        } transition-all duration-300 overflow-hidden bg-gray-900 border-r border-gray-700`}
      >
        <div className="p-4 space-y-4 h-full overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">Knowledge Graph</h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-gray-400 hover:text-white"
            >
              <ChevronLeftIcon className="h-5 w-5" />
            </button>
          </div>

          {/* Action Buttons */}
          <div className="space-y-2">
            <button
              onClick={handleAnalyzeAndPopulate}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {isLoading ? (
                <ArrowPathIcon className="h-4 w-4 animate-spin" />
              ) : (
                <PlayIcon className="h-4 w-4" />
              )}
              {isLoading ? 'Analyzing...' : 'Analyze & Populate'}
            </button>

            <div className="flex gap-2">
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="flex-1 flex items-center justify-center gap-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 text-white px-3 py-2 rounded-lg transition-colors"
              >
                <ArrowPathIcon className="h-4 w-4" />
                Refresh
              </button>
              
              <button
                onClick={handleExport}
                className="flex-1 flex items-center justify-center gap-2 bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded-lg transition-colors"
              >
                <DocumentArrowDownIcon className="h-4 w-4" />
                Export
              </button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-900 border border-red-700 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <InformationCircleIcon className="h-5 w-5 text-red-400" />
                <span className="text-red-200 text-sm">Error</span>
              </div>
              <div className="text-red-100 text-sm mt-1">{error}</div>
            </div>
          )}

          {/* Last Updated */}
          {lastUpdated && (
            <div className="text-xs text-gray-400">
              Last updated: {new Date(lastUpdated).toLocaleString()}
            </div>
          )}

          {/* Filters */}
          <KnowledgeGraphFilters />

          {/* Statistics */}
          {renderStatistics()}

          {/* Selected Node/Relationship Details */}
          {selectedNode && renderSelectedNodeDetails()}
          {selectedRelationship && renderSelectedRelationshipDetails()}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 relative">
        {/* Sidebar Toggle Button */}
        {!sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            className="absolute top-4 left-4 z-10 bg-gray-800 hover:bg-gray-700 text-white p-2 rounded-lg transition-colors"
          >
            <ChevronRightIcon className="h-5 w-5" />
          </button>
        )}

        {/* Knowledge Graph Visualization */}
        <KnowledgeGraphVisualization />
      </div>
    </div>
  );
};

export default KnowledgeGraph;