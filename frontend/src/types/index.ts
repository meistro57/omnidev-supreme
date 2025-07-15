// Agent Types
export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  description: string;
  capabilities: string[];
  status: AgentStatus;
  stats: AgentStats;
  metadata: AgentMetadata;
}

export enum AgentType {
  ARCHITECT = 'architect',
  CODER = 'coder',
  TESTER = 'tester',
  REVIEWER = 'reviewer',
  FIXER = 'fixer',
  DEPLOYER = 'deployer',
  ORCHESTRATOR = 'orchestrator',
  MEMORY = 'memory',
  CREATIVE = 'creative',
  GUARDIAN = 'guardian',
  ANALYZER = 'analyzer',
  TRAINER = 'trainer',
}

export enum AgentStatus {
  IDLE = 'idle',
  BUSY = 'busy',
  ERROR = 'error',
  DISABLED = 'disabled',
}

export interface AgentStats {
  tasks_completed: number;
  tasks_failed: number;
  average_response_time: number;
  total_tokens_used: number;
}

export interface AgentMetadata {
  name: string;
  agent_type: AgentType;
  description: string;
  capabilities: string[];
  model_requirements: string[];
  priority: number;
  max_concurrent_tasks: number;
  timeout_seconds: number;
  retry_count: number;
}

// Task Types
export interface Task {
  id: string;
  content: string;
  type: string;
  complexity: TaskComplexity;
  priority: number;
  status: TaskStatus;
  agent_id?: string;
  session_id?: string;
  created_at: string;
  updated_at: string;
  result?: TaskResult;
}

export enum TaskComplexity {
  SIMPLE = 'simple',
  MEDIUM = 'medium',
  COMPLEX = 'complex',
  EXPERT = 'expert',
}

export enum TaskStatus {
  PENDING = 'pending',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
}

export interface TaskResult {
  success: boolean;
  result?: any;
  error?: string;
  tokens_used?: number;
  response_time?: number;
}

// Project Types
export interface Project {
  id: string;
  name: string;
  description: string;
  language: string;
  framework?: string;
  created_at: string;
  updated_at: string;
  files: ProjectFile[];
  status: ProjectStatus;
  agents_assigned: string[];
}

export enum ProjectStatus {
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  ARCHIVED = 'archived',
}

export interface ProjectFile {
  id: string;
  name: string;
  path: string;
  content: string;
  language: string;
  size: number;
  last_modified: string;
  is_dirty: boolean;
}

// Memory Types
export interface Memory {
  id: string;
  content: string;
  type: MemoryType;
  priority: MemoryPriority;
  metadata: Record<string, any>;
  tags: string[];
  session_id?: string;
  created_at: string;
  updated_at: string;
}

export enum MemoryType {
  CODE = 'code',
  TASK = 'task',
  AGENT = 'agent',
  KNOWLEDGE = 'knowledge',
  SESSION = 'session',
}

export enum MemoryPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

// Session Types
export interface Session {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  project_id?: string;
  agents_involved: string[];
  memory_entries: string[];
  status: SessionStatus;
}

export enum SessionStatus {
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  ARCHIVED = 'archived',
}

// WebSocket Types
export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
}

export interface AgentStatusUpdate {
  agent_id: string;
  status: AgentStatus;
  current_task?: string;
  progress?: number;
}

export interface TaskUpdate {
  task_id: string;
  status: TaskStatus;
  progress?: number;
  result?: TaskResult;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Monaco Editor Types
export interface EditorFile {
  id: string;
  name: string;
  path: string;
  content: string;
  language: string;
  is_dirty: boolean;
  cursor_position?: {
    line: number;
    column: number;
  };
}

export interface EditorTab {
  id: string;
  file_id: string;
  name: string;
  path: string;
  is_active: boolean;
  is_dirty: boolean;
  language: string;
}

// Dashboard Types
export interface DashboardStats {
  total_agents: number;
  active_agents: number;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  memory_entries: number;
  projects: number;
  sessions: number;
}

export interface SystemHealth {
  overall_status: 'healthy' | 'warning' | 'error';
  services: {
    api: 'up' | 'down';
    database: 'up' | 'down';
    memory: 'up' | 'down';
    agents: 'up' | 'down';
  };
  memory_usage: {
    used: number;
    total: number;
    percentage: number;
  };
  active_connections: number;
}