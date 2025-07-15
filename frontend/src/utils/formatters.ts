import { AgentStatus, TaskStatus, MemoryPriority } from '@/types';

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return 'just now';
}

export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}h ${minutes}m ${remainingSeconds}s`;
  }
  if (minutes > 0) {
    return `${minutes}m ${remainingSeconds}s`;
  }
  return `${remainingSeconds}s`;
}

export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

export function formatPercentage(value: number, total: number): string {
  if (total === 0) return '0%';
  return Math.round((value / total) * 100) + '%';
}

export function getAgentStatusColor(status: AgentStatus): string {
  switch (status) {
    case AgentStatus.IDLE:
      return 'text-green-400';
    case AgentStatus.BUSY:
      return 'text-yellow-400';
    case AgentStatus.ERROR:
      return 'text-red-400';
    case AgentStatus.DISABLED:
      return 'text-gray-400';
    default:
      return 'text-gray-400';
  }
}

export function getAgentStatusBadgeColor(status: AgentStatus): string {
  switch (status) {
    case AgentStatus.IDLE:
      return 'bg-green-500';
    case AgentStatus.BUSY:
      return 'bg-yellow-500';
    case AgentStatus.ERROR:
      return 'bg-red-500';
    case AgentStatus.DISABLED:
      return 'bg-gray-500';
    default:
      return 'bg-gray-500';
  }
}

export function getTaskStatusColor(status: TaskStatus): string {
  switch (status) {
    case TaskStatus.PENDING:
      return 'text-blue-400';
    case TaskStatus.ASSIGNED:
      return 'text-purple-400';
    case TaskStatus.IN_PROGRESS:
      return 'text-yellow-400';
    case TaskStatus.COMPLETED:
      return 'text-green-400';
    case TaskStatus.FAILED:
      return 'text-red-400';
    case TaskStatus.CANCELLED:
      return 'text-gray-400';
    default:
      return 'text-gray-400';
  }
}

export function getMemoryPriorityColor(priority: MemoryPriority): string {
  switch (priority) {
    case MemoryPriority.CRITICAL:
      return 'text-red-400';
    case MemoryPriority.HIGH:
      return 'text-orange-400';
    case MemoryPriority.MEDIUM:
      return 'text-yellow-400';
    case MemoryPriority.LOW:
      return 'text-gray-400';
    default:
      return 'text-gray-400';
  }
}

export function capitalizeFirst(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

export function pluralize(count: number, singular: string, plural?: string): string {
  if (count === 1) return `${count} ${singular}`;
  return `${count} ${plural || singular + 's'}`;
}