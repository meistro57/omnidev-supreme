import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Memory, MemoryType, MemoryPriority } from '@/types';
import { apiClient } from '@/utils/api';

interface MemoryState {
  memories: Memory[];
  loading: boolean;
  error: string | null;
  searchResults: Memory[];
  isSearching: boolean;
  filters: {
    type: MemoryType | null;
    priority: MemoryPriority | null;
    tags: string[];
    search: string;
  };
}

const initialState: MemoryState = {
  memories: [],
  loading: false,
  error: null,
  searchResults: [],
  isSearching: false,
  filters: {
    type: null,
    priority: null,
    tags: [],
    search: '',
  },
};

export const fetchMemories = createAsyncThunk('memory/fetchMemories', async () => {
  const response = await apiClient.get('/memory');
  return response.data;
});

export const searchMemories = createAsyncThunk('memory/searchMemories', async (query: string) => {
  const response = await apiClient.get(`/memory/search?q=${encodeURIComponent(query)}`);
  return response.data;
});

export const createMemory = createAsyncThunk('memory/createMemory', async (memory: Partial<Memory>) => {
  const response = await apiClient.post('/memory', memory);
  return response.data;
});

export const deleteMemory = createAsyncThunk('memory/deleteMemory', async (memoryId: string) => {
  await apiClient.delete(`/memory/${memoryId}`);
  return memoryId;
});

const memorySlice = createSlice({
  name: 'memory',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<Partial<MemoryState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearSearchResults: (state) => {
      state.searchResults = [];
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMemories.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMemories.fulfilled, (state, action) => {
        state.loading = false;
        state.memories = action.payload;
      })
      .addCase(fetchMemories.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch memories';
      })
      .addCase(searchMemories.pending, (state) => {
        state.isSearching = true;
      })
      .addCase(searchMemories.fulfilled, (state, action) => {
        state.isSearching = false;
        state.searchResults = action.payload;
      })
      .addCase(searchMemories.rejected, (state, action) => {
        state.isSearching = false;
        state.error = action.error.message || 'Search failed';
      })
      .addCase(createMemory.fulfilled, (state, action) => {
        state.memories.push(action.payload);
      })
      .addCase(deleteMemory.fulfilled, (state, action) => {
        state.memories = state.memories.filter(m => m.id !== action.payload);
      });
  },
});

export const { setFilters, clearSearchResults, clearError } = memorySlice.actions;
export default memorySlice.reducer;