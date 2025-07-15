import { configureStore } from '@reduxjs/toolkit';
import agentsReducer from './slices/agentsSlice';
import tasksReducer from './slices/tasksSlice';
import projectsReducer from './slices/projectsSlice';
import memoryReducer from './slices/memorySlice';
import editorReducer from './slices/editorSlice';
import uiReducer from './slices/uiSlice';
import websocketReducer from './slices/websocketSlice';

export const store = configureStore({
  reducer: {
    agents: agentsReducer,
    tasks: tasksReducer,
    projects: projectsReducer,
    memory: memoryReducer,
    editor: editorReducer,
    ui: uiReducer,
    websocket: websocketReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['websocket/messageReceived'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;