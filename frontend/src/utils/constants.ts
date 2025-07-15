export const AGENT_TYPES = {
  ARCHITECT: 'architect',
  CODER: 'coder',
  TESTER: 'tester',
  REVIEWER: 'reviewer',
  FIXER: 'fixer',
  DEPLOYER: 'deployer',
  ORCHESTRATOR: 'orchestrator',
  MEMORY: 'memory',
  CREATIVE: 'creative',
  GUARDIAN: 'guardian',
  ANALYZER: 'analyzer',
  TRAINER: 'trainer',
} as const;

export const AGENT_STATUS = {
  IDLE: 'idle',
  BUSY: 'busy',
  ERROR: 'error',
  DISABLED: 'disabled',
} as const;

export const TASK_STATUS = {
  PENDING: 'pending',
  ASSIGNED: 'assigned',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
} as const;

export const MEMORY_TYPES = {
  CODE: 'code',
  TASK: 'task',
  AGENT: 'agent',
  KNOWLEDGE: 'knowledge',
  SESSION: 'session',
} as const;

export const MEMORY_PRIORITIES = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
} as const;

export const EDITOR_THEMES = {
  DARK: 'vs-dark',
  LIGHT: 'vs-light',
  HIGH_CONTRAST: 'hc-black',
} as const;

export const SUPPORTED_LANGUAGES = [
  'javascript',
  'typescript',
  'python',
  'java',
  'cpp',
  'c',
  'csharp',
  'php',
  'ruby',
  'go',
  'rust',
  'html',
  'css',
  'scss',
  'less',
  'json',
  'xml',
  'yaml',
  'markdown',
  'sql',
  'shell',
  'dockerfile',
  'plaintext',
] as const;

export const KEYBOARD_SHORTCUTS = {
  SAVE_FILE: 'Ctrl+S',
  NEW_FILE: 'Ctrl+N',
  CLOSE_TAB: 'Ctrl+W',
  TOGGLE_SIDEBAR: 'Ctrl+B',
  TOGGLE_TERMINAL: 'Ctrl+`',
  COMMAND_PALETTE: 'Ctrl+Shift+P',
  FIND: 'Ctrl+F',
  REPLACE: 'Ctrl+H',
  GOTO_LINE: 'Ctrl+G',
  FORMAT_DOCUMENT: 'Shift+Alt+F',
} as const;

export const API_ENDPOINTS = {
  AGENTS: '/agents',
  TASKS: '/tasks',
  PROJECTS: '/projects',
  MEMORY: '/memory',
  FILES: '/files',
  HEALTH: '/health',
} as const;

export const WEBSOCKET_EVENTS = {
  CONNECT: 'connect',
  DISCONNECT: 'disconnect',
  MESSAGE: 'message',
  AGENT_STATUS_UPDATE: 'agent_status_update',
  TASK_UPDATE: 'task_update',
  MEMORY_UPDATE: 'memory_update',
  SYSTEM_HEALTH: 'system_health',
} as const;

export const UI_CONSTANTS = {
  SIDEBAR_WIDTH: 300,
  BOTTOM_PANEL_HEIGHT: 300,
  RIGHT_PANEL_WIDTH: 350,
  HEADER_HEIGHT: 64,
  TAB_HEIGHT: 40,
  NOTIFICATION_DURATION: 5000,
} as const;

export const VALIDATION_RULES = {
  PROJECT_NAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 50,
    PATTERN: /^[a-zA-Z0-9_-]+$/,
  },
  FILE_NAME: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 255,
    PATTERN: /^[^<>:"/\\|?*]+$/,
  },
  TASK_CONTENT: {
    MIN_LENGTH: 10,
    MAX_LENGTH: 5000,
  },
} as const;