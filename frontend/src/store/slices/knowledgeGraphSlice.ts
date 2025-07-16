import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../utils/api';

// Types
export interface GraphNode {
  id: string;
  node_type: string;
  name: string;
  description: string;
  metadata: Record<string, any>;
  tags: string[];
}

export interface GraphRelationship {
  id: string;
  source_id: string;
  target_id: string;
  relationship_type: string;
  strength: number;
  confidence: number;
  metadata: Record<string, any>;
}

export interface KnowledgeGraphData {
  nodes: GraphNode[];
  relationships: GraphRelationship[];
  statistics: Record<string, any>;
}

export interface GraphFilters {
  nodeTypes: string[];
  relationshipTypes: string[];
  systems: string[];
  searchQuery: string;
  minConfidence: number;
}

export interface KnowledgeGraphState {
  data: KnowledgeGraphData | null;
  filteredData: KnowledgeGraphData | null;
  filters: GraphFilters;
  selectedNode: GraphNode | null;
  selectedRelationship: GraphRelationship | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: string | null;
  layoutMode: 'force' | '2d' | '3d';
  showDetails: boolean;
}

const initialState: KnowledgeGraphState = {
  data: null,
  filteredData: null,
  filters: {
    nodeTypes: [],
    relationshipTypes: [],
    systems: [],
    searchQuery: '',
    minConfidence: 0.0,
  },
  selectedNode: null,
  selectedRelationship: null,
  isLoading: false,
  error: null,
  lastUpdated: null,
  layoutMode: 'force',
  showDetails: false,
};

// Async thunks
export const fetchKnowledgeGraph = createAsyncThunk(
  'knowledgeGraph/fetchKnowledgeGraph',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/knowledge-graph');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch knowledge graph');
    }
  }
);

export const analyzeAndPopulateGraph = createAsyncThunk(
  'knowledgeGraph/analyzeAndPopulateGraph',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.post('/knowledge-graph/analyze');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to analyze and populate graph');
    }
  }
);

export const getAgentRecommendations = createAsyncThunk(
  'knowledgeGraph/getAgentRecommendations',
  async (task: any, { rejectWithValue }) => {
    try {
      const response = await api.post('/knowledge-graph/recommend-agents', { task });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get agent recommendations');
    }
  }
);

export const getAgentInsights = createAsyncThunk(
  'knowledgeGraph/getAgentInsights',
  async (agentName: string, { rejectWithValue }) => {
    try {
      const response = await api.get(`/knowledge-graph/agent-insights/${agentName}`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get agent insights');
    }
  }
);

export const exportKnowledgeGraph = createAsyncThunk(
  'knowledgeGraph/exportKnowledgeGraph',
  async (format: 'json' | 'graphml' | 'csv', { rejectWithValue }) => {
    try {
      const response = await api.get(`/knowledge-graph/export/${format}`, { responseType: 'blob' });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to export knowledge graph');
    }
  }
);

// Helper functions
const applyFilters = (data: KnowledgeGraphData, filters: GraphFilters): KnowledgeGraphData => {
  if (!data) return data;

  let filteredNodes = data.nodes;
  let filteredRelationships = data.relationships;

  // Filter by node types
  if (filters.nodeTypes.length > 0) {
    filteredNodes = filteredNodes.filter(node => 
      filters.nodeTypes.includes(node.node_type)
    );
  }

  // Filter by systems
  if (filters.systems.length > 0) {
    filteredNodes = filteredNodes.filter(node => 
      filters.systems.includes(node.metadata?.system || '')
    );
  }

  // Filter by search query
  if (filters.searchQuery) {
    const query = filters.searchQuery.toLowerCase();
    filteredNodes = filteredNodes.filter(node =>
      node.name.toLowerCase().includes(query) ||
      node.description.toLowerCase().includes(query) ||
      node.tags.some(tag => tag.toLowerCase().includes(query))
    );
  }

  // Get node IDs for relationship filtering
  const nodeIds = new Set(filteredNodes.map(node => node.id));

  // Filter relationships
  filteredRelationships = filteredRelationships.filter(rel => {
    // Only include relationships between filtered nodes
    if (!nodeIds.has(rel.source_id) || !nodeIds.has(rel.target_id)) {
      return false;
    }

    // Filter by relationship types
    if (filters.relationshipTypes.length > 0 && 
        !filters.relationshipTypes.includes(rel.relationship_type)) {
      return false;
    }

    // Filter by confidence
    if (rel.confidence < filters.minConfidence) {
      return false;
    }

    return true;
  });

  return {
    nodes: filteredNodes,
    relationships: filteredRelationships,
    statistics: data.statistics,
  };
};

const knowledgeGraphSlice = createSlice({
  name: 'knowledgeGraph',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<Partial<GraphFilters>>) => {
      state.filters = { ...state.filters, ...action.payload };
      if (state.data) {
        state.filteredData = applyFilters(state.data, state.filters);
      }
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
      state.filteredData = state.data;
    },
    setSelectedNode: (state, action: PayloadAction<GraphNode | null>) => {
      state.selectedNode = action.payload;
      state.selectedRelationship = null; // Clear relationship selection when selecting a node
    },
    setSelectedRelationship: (state, action: PayloadAction<GraphRelationship | null>) => {
      state.selectedRelationship = action.payload;
      state.selectedNode = null; // Clear node selection when selecting a relationship
    },
    setLayoutMode: (state, action: PayloadAction<'force' | '2d' | '3d'>) => {
      state.layoutMode = action.payload;
    },
    toggleDetails: (state) => {
      state.showDetails = !state.showDetails;
    },
    setShowDetails: (state, action: PayloadAction<boolean>) => {
      state.showDetails = action.payload;
    },
    clearSelection: (state) => {
      state.selectedNode = null;
      state.selectedRelationship = null;
    },
    updateNodePosition: (state, action: PayloadAction<{ nodeId: string; x: number; y: number; z?: number }>) => {
      if (state.filteredData) {
        const node = state.filteredData.nodes.find(n => n.id === action.payload.nodeId);
        if (node) {
          node.metadata = {
            ...node.metadata,
            position: {
              x: action.payload.x,
              y: action.payload.y,
              z: action.payload.z,
            },
          };
        }
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch knowledge graph
      .addCase(fetchKnowledgeGraph.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchKnowledgeGraph.fulfilled, (state, action) => {
        state.isLoading = false;
        state.data = action.payload;
        state.filteredData = applyFilters(action.payload, state.filters);
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchKnowledgeGraph.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Analyze and populate graph
      .addCase(analyzeAndPopulateGraph.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(analyzeAndPopulateGraph.fulfilled, (state, action) => {
        state.isLoading = false;
        state.error = null;
        // Trigger a refetch of the graph data
      })
      .addCase(analyzeAndPopulateGraph.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Get agent recommendations
      .addCase(getAgentRecommendations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getAgentRecommendations.fulfilled, (state) => {
        state.isLoading = false;
        state.error = null;
      })
      .addCase(getAgentRecommendations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Get agent insights
      .addCase(getAgentInsights.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getAgentInsights.fulfilled, (state) => {
        state.isLoading = false;
        state.error = null;
      })
      .addCase(getAgentInsights.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setFilters,
  clearFilters,
  setSelectedNode,
  setSelectedRelationship,
  setLayoutMode,
  toggleDetails,
  setShowDetails,
  clearSelection,
  updateNodePosition,
} = knowledgeGraphSlice.actions;

export default knowledgeGraphSlice.reducer;