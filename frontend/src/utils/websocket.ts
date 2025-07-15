import { io, Socket } from 'socket.io-client';
import { store } from '@/store';
import { connectionOpened, connectionClosed, connectionError, messageReceived, agentStatusUpdate, taskUpdate } from '@/store/slices/websocketSlice';
import { updateAgentStatusLocal } from '@/store/slices/agentsSlice';
import { updateTaskStatus } from '@/store/slices/tasksSlice';
import { WebSocketMessage, AgentStatusUpdate, TaskUpdate } from '@/types';

class WebSocketManager {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(): void {
    if (this.socket?.connected) return;

    const WS_URL = (import.meta as any).env.VITE_WS_URL || 'ws://localhost:8000';
    
    this.socket = io(WS_URL, {
      transports: ['websocket'],
      timeout: 20000,
      forceNew: true,
    });

    this.socket.on('connect', () => {
      store.dispatch(connectionOpened());
      this.reconnectAttempts = 0;
      console.log('🔗 WebSocket connected');
    });

    this.socket.on('disconnect', (reason) => {
      store.dispatch(connectionClosed());
      console.log('🔌 WebSocket disconnected:', reason);
      
      if (reason === 'io server disconnect') {
        // Server disconnected, reconnect manually
        this.handleReconnect();
      }
    });

    this.socket.on('connect_error', (error) => {
      store.dispatch(connectionError(error.message));
      console.error('❌ WebSocket connection error:', error);
      this.handleReconnect();
    });

    // Handle different message types
    this.socket.on('message', (data: WebSocketMessage) => {
      store.dispatch(messageReceived(data));
      this.handleMessage(data);
    });

    this.socket.on('agent_status_update', (data: AgentStatusUpdate) => {
      store.dispatch(agentStatusUpdate(data));
      store.dispatch(updateAgentStatusLocal({ 
        agentId: data.agent_id, 
        status: data.status 
      }));
    });

    this.socket.on('task_update', (data: TaskUpdate) => {
      store.dispatch(taskUpdate(data));
      store.dispatch(updateTaskStatus({ 
        taskId: data.task_id, 
        status: data.status 
      }));
    });
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      setTimeout(() => {
        console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        this.connect();
      }, delay);
    } else {
      console.error('❌ Max reconnection attempts reached');
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    switch (message.type) {
      case 'notification':
        // Handle notifications
        break;
      case 'system_health':
        // Handle system health updates
        break;
      case 'memory_update':
        // Handle memory updates
        break;
      default:
        console.log('📨 Received message:', message);
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendMessage(type: string, data: any): void {
    if (this.socket?.connected) {
      this.socket.emit(type, data);
    } else {
      console.warn('⚠️ WebSocket not connected, cannot send message');
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const websocketManager = new WebSocketManager();