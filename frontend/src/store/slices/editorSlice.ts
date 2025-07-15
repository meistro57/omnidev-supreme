import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { EditorFile, EditorTab, Project } from '@/types';
import { apiClient } from '@/utils/api';

interface EditorState {
  files: EditorFile[];
  tabs: EditorTab[];
  activeTabId: string | null;
  currentProject: Project | null;
  loading: boolean;
  error: string | null;
  settings: {
    theme: 'vs-dark' | 'vs-light' | 'hc-black';
    fontSize: number;
    tabSize: number;
    wordWrap: 'on' | 'off' | 'wordWrapColumn' | 'bounded';
    minimap: boolean;
    lineNumbers: 'on' | 'off' | 'relative' | 'interval';
    autoSave: boolean;
    autoSaveDelay: number;
  };
}

const initialState: EditorState = {
  files: [],
  tabs: [],
  activeTabId: null,
  currentProject: null,
  loading: false,
  error: null,
  settings: {
    theme: 'vs-dark',
    fontSize: 14,
    tabSize: 2,
    wordWrap: 'on',
    minimap: true,
    lineNumbers: 'on',
    autoSave: true,
    autoSaveDelay: 2000,
  },
};

// Async thunks
export const loadFile = createAsyncThunk(
  'editor/loadFile',
  async (filePath: string) => {
    const response = await apiClient.get(`/files/${encodeURIComponent(filePath)}`);
    return response.data;
  }
);

export const saveFile = createAsyncThunk(
  'editor/saveFile',
  async ({ fileId, content }: { fileId: string; content: string }) => {
    await apiClient.post(`/files/${fileId}/save`, { content });
    return { fileId, content };
  }
);

export const createFile = createAsyncThunk(
  'editor/createFile',
  async ({ name, path, content, language }: { name: string; path: string; content: string; language: string }) => {
    const response = await apiClient.post('/files', { name, path, content, language });
    return response.data;
  }
);

export const deleteFile = createAsyncThunk(
  'editor/deleteFile',
  async (fileId: string) => {
    await apiClient.delete(`/files/${fileId}`);
    return fileId;
  }
);

const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    openFile: (state, action: PayloadAction<EditorFile>) => {
      const file = action.payload;
      
      // Add file if not already present
      if (!state.files.find(f => f.id === file.id)) {
        state.files.push(file);
      }
      
      // Create or activate tab
      const existingTab = state.tabs.find(tab => tab.file_id === file.id);
      if (existingTab) {
        state.tabs.forEach(tab => tab.is_active = false);
        existingTab.is_active = true;
        state.activeTabId = existingTab.id;
      } else {
        const newTab: EditorTab = {
          id: `tab-${file.id}`,
          file_id: file.id,
          name: file.name,
          path: file.path,
          is_active: true,
          is_dirty: false,
          language: file.language,
        };
        
        state.tabs.forEach(tab => tab.is_active = false);
        state.tabs.push(newTab);
        state.activeTabId = newTab.id;
      }
    },
    
    closeTab: (state, action: PayloadAction<string>) => {
      const tabId = action.payload;
      const tabIndex = state.tabs.findIndex(tab => tab.id === tabId);
      
      if (tabIndex !== -1) {
        const tab = state.tabs[tabIndex];
        state.tabs.splice(tabIndex, 1);
        
        // If this was the active tab, activate another one
        if (state.activeTabId === tabId) {
          if (state.tabs.length > 0) {
            const newActiveTab = state.tabs[Math.min(tabIndex, state.tabs.length - 1)];
            newActiveTab.is_active = true;
            state.activeTabId = newActiveTab.id;
          } else {
            state.activeTabId = null;
          }
        }
        
        // Remove file if no tabs reference it
        if (!state.tabs.find(t => t.file_id === tab.file_id)) {
          state.files = state.files.filter(f => f.id !== tab.file_id);
        }
      }
    },
    
    setActiveTab: (state, action: PayloadAction<string>) => {
      state.tabs.forEach(tab => tab.is_active = false);
      const tab = state.tabs.find(tab => tab.id === action.payload);
      if (tab) {
        tab.is_active = true;
        state.activeTabId = action.payload;
      }
    },
    
    updateFileContent: (state, action: PayloadAction<{ fileId: string; content: string }>) => {
      const { fileId, content } = action.payload;
      const file = state.files.find(f => f.id === fileId);
      if (file) {
        file.content = content;
        file.is_dirty = true;
      }
      
      // Update corresponding tab
      const tab = state.tabs.find(tab => tab.file_id === fileId);
      if (tab) {
        tab.is_dirty = true;
      }
    },
    
    markFileSaved: (state, action: PayloadAction<string>) => {
      const fileId = action.payload;
      const file = state.files.find(f => f.id === fileId);
      if (file) {
        file.is_dirty = false;
      }
      
      const tab = state.tabs.find(tab => tab.file_id === fileId);
      if (tab) {
        tab.is_dirty = false;
      }
    },
    
    setCurrentProject: (state, action: PayloadAction<Project | null>) => {
      state.currentProject = action.payload;
    },
    
    updateSettings: (state, action: PayloadAction<Partial<EditorState['settings']>>) => {
      state.settings = { ...state.settings, ...action.payload };
    },
    
    setCursorPosition: (state, action: PayloadAction<{ fileId: string; line: number; column: number }>) => {
      const { fileId, line, column } = action.payload;
      const file = state.files.find(f => f.id === fileId);
      if (file) {
        file.cursor_position = { line, column };
      }
    },
    
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadFile.fulfilled, (state, action) => {
        state.loading = false;
        const file = action.payload;
        
        // Update or add file
        const existingIndex = state.files.findIndex(f => f.id === file.id);
        if (existingIndex !== -1) {
          state.files[existingIndex] = file;
        } else {
          state.files.push(file);
        }
      })
      .addCase(loadFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to load file';
      })
      .addCase(saveFile.fulfilled, (state, action) => {
        const { fileId } = action.payload;
        const file = state.files.find(f => f.id === fileId);
        if (file) {
          file.is_dirty = false;
        }
        
        const tab = state.tabs.find(tab => tab.file_id === fileId);
        if (tab) {
          tab.is_dirty = false;
        }
      })
      .addCase(createFile.fulfilled, (state, action) => {
        const file = action.payload;
        state.files.push(file);
      })
      .addCase(deleteFile.fulfilled, (state, action) => {
        const fileId = action.payload;
        
        // Remove file
        state.files = state.files.filter(f => f.id !== fileId);
        
        // Remove tabs associated with this file
        const tabsToRemove = state.tabs.filter(tab => tab.file_id === fileId);
        tabsToRemove.forEach(tab => {
          const tabIndex = state.tabs.findIndex(t => t.id === tab.id);
          if (tabIndex !== -1) {
            state.tabs.splice(tabIndex, 1);
          }
        });
        
        // Update active tab if necessary
        if (state.activeTabId && tabsToRemove.some(tab => tab.id === state.activeTabId)) {
          if (state.tabs.length > 0) {
            const newActiveTab = state.tabs[0];
            newActiveTab.is_active = true;
            state.activeTabId = newActiveTab.id;
          } else {
            state.activeTabId = null;
          }
        }
      });
  },
});

export const {
  openFile,
  closeTab,
  setActiveTab,
  updateFileContent,
  markFileSaved,
  setCurrentProject,
  updateSettings,
  setCursorPosition,
  clearError,
} = editorSlice.actions;

export default editorSlice.reducer;