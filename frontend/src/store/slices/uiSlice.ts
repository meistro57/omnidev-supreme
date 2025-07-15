import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  sidebar: {
    isOpen: boolean;
    activePanel: 'agents' | 'memory' | 'projects' | 'files';
  };
  bottomPanel: {
    isOpen: boolean;
    activePanel: 'tasks' | 'console' | 'terminal';
    height: number;
  };
  rightPanel: {
    isOpen: boolean;
    activePanel: 'agent-details' | 'memory-search' | 'project-info';
    width: number;
  };
  theme: 'dark' | 'light';
  notifications: Notification[];
  loading: {
    global: boolean;
    operations: Record<string, boolean>;
  };
}

interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: string;
  duration?: number;
  action?: {
    label: string;
    handler: () => void;
  };
}

const initialState: UIState = {
  sidebar: {
    isOpen: true,
    activePanel: 'agents',
  },
  bottomPanel: {
    isOpen: false,
    activePanel: 'tasks',
    height: 300,
  },
  rightPanel: {
    isOpen: false,
    activePanel: 'agent-details',
    width: 350,
  },
  theme: 'dark',
  notifications: [],
  loading: {
    global: false,
    operations: {},
  },
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebar.isOpen = !state.sidebar.isOpen;
    },
    setSidebarPanel: (state, action: PayloadAction<UIState['sidebar']['activePanel']>) => {
      state.sidebar.activePanel = action.payload;
      state.sidebar.isOpen = true;
    },
    toggleBottomPanel: (state) => {
      state.bottomPanel.isOpen = !state.bottomPanel.isOpen;
    },
    setBottomPanel: (state, action: PayloadAction<UIState['bottomPanel']['activePanel']>) => {
      state.bottomPanel.activePanel = action.payload;
      state.bottomPanel.isOpen = true;
    },
    setBottomPanelHeight: (state, action: PayloadAction<number>) => {
      state.bottomPanel.height = Math.max(200, Math.min(600, action.payload));
    },
    toggleRightPanel: (state) => {
      state.rightPanel.isOpen = !state.rightPanel.isOpen;
    },
    setRightPanel: (state, action: PayloadAction<UIState['rightPanel']['activePanel']>) => {
      state.rightPanel.activePanel = action.payload;
      state.rightPanel.isOpen = true;
    },
    setRightPanelWidth: (state, action: PayloadAction<number>) => {
      state.rightPanel.width = Math.max(300, Math.min(800, action.payload));
    },
    setTheme: (state, action: PayloadAction<'dark' | 'light'>) => {
      state.theme = action.payload;
    },
    addNotification: (state, action: PayloadAction<Omit<Notification, 'id' | 'timestamp'>>) => {
      const notification: Notification = {
        ...action.payload,
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
      };
      state.notifications.push(notification);
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    setGlobalLoading: (state, action: PayloadAction<boolean>) => {
      state.loading.global = action.payload;
    },
    setOperationLoading: (state, action: PayloadAction<{ operation: string; loading: boolean }>) => {
      const { operation, loading } = action.payload;
      if (loading) {
        state.loading.operations[operation] = true;
      } else {
        delete state.loading.operations[operation];
      }
    },
  },
});

export const {
  toggleSidebar,
  setSidebarPanel,
  toggleBottomPanel,
  setBottomPanel,
  setBottomPanelHeight,
  toggleRightPanel,
  setRightPanel,
  setRightPanelWidth,
  setTheme,
  addNotification,
  removeNotification,
  clearNotifications,
  setGlobalLoading,
  setOperationLoading,
} = uiSlice.actions;

export default uiSlice.reducer;