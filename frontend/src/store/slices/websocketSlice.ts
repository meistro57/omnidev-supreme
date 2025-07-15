import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { WebSocketMessage, AgentStatusUpdate, TaskUpdate } from '@/types';

interface WebSocketState {
  connected: boolean;
  messages: WebSocketMessage[];
  lastMessage: WebSocketMessage | null;
  error: string | null;
}

const initialState: WebSocketState = {
  connected: false,
  messages: [],
  lastMessage: null,
  error: null,
};

const websocketSlice = createSlice({
  name: 'websocket',
  initialState,
  reducers: {
    connectionOpened: (state) => {
      state.connected = true;
      state.error = null;
    },
    connectionClosed: (state) => {
      state.connected = false;
    },
    connectionError: (state, action: PayloadAction<string>) => {
      state.connected = false;
      state.error = action.payload;
    },
    messageReceived: (state, action: PayloadAction<WebSocketMessage>) => {
      state.messages.push(action.payload);
      state.lastMessage = action.payload;
      
      // Keep only last 100 messages
      if (state.messages.length > 100) {
        state.messages = state.messages.slice(-100);
      }
    },
    agentStatusUpdate: (_state, _action: PayloadAction<AgentStatusUpdate>) => {
      // This will be handled by the agents slice
    },
    taskUpdate: (_state, _action: PayloadAction<TaskUpdate>) => {
      // This will be handled by the tasks slice
    },
    clearMessages: (state) => {
      state.messages = [];
      state.lastMessage = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  connectionOpened,
  connectionClosed,
  connectionError,
  messageReceived,
  agentStatusUpdate,
  taskUpdate,
  clearMessages,
  clearError,
} = websocketSlice.actions;

export default websocketSlice.reducer;