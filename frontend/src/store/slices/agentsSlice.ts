import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Agent, AgentStatus, AgentType } from '@/types';
import { apiClient } from '@/utils/api';

interface AgentsState {
  agents: Agent[];
  loading: boolean;
  error: string | null;
  selectedAgent: Agent | null;
  filters: {
    type: AgentType | null;
    status: AgentStatus | null;
    search: string;
  };
}

const initialState: AgentsState = {
  agents: [],
  loading: false,
  error: null,
  selectedAgent: null,
  filters: {
    type: null,
    status: null,
    search: '',
  },
};

// Async thunks
export const fetchAgents = createAsyncThunk(
  'agents/fetchAgents',
  async () => {
    const response = await apiClient.get('/agents');
    return response.data;
  }
);

export const updateAgentStatus = createAsyncThunk(
  'agents/updateStatus',
  async ({ agentId, status }: { agentId: string; status: AgentStatus }) => {
    const response = await apiClient.patch(`/agents/${agentId}/status`, { status });
    return response.data;
  }
);

export const executeTask = createAsyncThunk(
  'agents/executeTask',
  async ({ agentId, task }: { agentId: string; task: any }) => {
    const response = await apiClient.post(`/agents/${agentId}/execute`, task);
    return response.data;
  }
);

const agentsSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    setSelectedAgent: (state, action: PayloadAction<Agent | null>) => {
      state.selectedAgent = action.payload;
    },
    setFilters: (state, action: PayloadAction<Partial<AgentsState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    updateAgent: (state, action: PayloadAction<Agent>) => {
      const index = state.agents.findIndex(agent => agent.id === action.payload.id);
      if (index !== -1) {
        state.agents[index] = action.payload;
      }
    },
    updateAgentStatusLocal: (state, action: PayloadAction<{ agentId: string; status: AgentStatus }>) => {
      const agent = state.agents.find(agent => agent.id === action.payload.agentId);
      if (agent) {
        agent.status = action.payload.status;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAgents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAgents.fulfilled, (state, action) => {
        state.loading = false;
        state.agents = action.payload;
      })
      .addCase(fetchAgents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch agents';
      })
      .addCase(updateAgentStatus.fulfilled, (state, action) => {
        const agent = state.agents.find(agent => agent.id === action.payload.id);
        if (agent) {
          agent.status = action.payload.status;
        }
      })
      .addCase(executeTask.fulfilled, (_state, action) => {
        // Handle task execution response
        console.log('Task executed:', action.payload);
      });
  },
});

export const {
  setSelectedAgent,
  setFilters,
  updateAgent,
  updateAgentStatusLocal,
  clearError,
} = agentsSlice.actions;

export default agentsSlice.reducer;