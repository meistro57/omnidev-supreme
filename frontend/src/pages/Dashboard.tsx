import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { fetchAgents } from '@/store/slices/agentsSlice';
import { fetchTasks } from '@/store/slices/tasksSlice';
import { fetchProjects } from '@/store/slices/projectsSlice';
import { 
  CpuChipIcon, 
  ClipboardDocumentListIcon, 
  CubeIcon, 
  DocumentTextIcon,
  ChartBarIcon,
  WifiIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';
import { formatNumber, formatRelativeTime, getAgentStatusColor, getTaskStatusColor } from '@/utils/formatters';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { agents } = useSelector((state: RootState) => state.agents);
  const { tasks } = useSelector((state: RootState) => state.tasks);
  const { projects } = useSelector((state: RootState) => state.projects);
  const { memories } = useSelector((state: RootState) => state.memory);
  const { connected } = useSelector((state: RootState) => state.websocket);

  useEffect(() => {
    dispatch(fetchAgents() as any);
    dispatch(fetchTasks() as any);
    dispatch(fetchProjects() as any);
  }, [dispatch]);

  // Calculate stats
  const stats = {
    totalAgents: agents.length,
    activeAgents: agents.filter(a => a.status === 'busy').length,
    idleAgents: agents.filter(a => a.status === 'idle').length,
    errorAgents: agents.filter(a => a.status === 'error').length,
    
    totalTasks: tasks.length,
    completedTasks: tasks.filter(t => t.status === 'completed').length,
    failedTasks: tasks.filter(t => t.status === 'failed').length,
    activeTasks: tasks.filter(t => t.status === 'in_progress').length,
    
    totalProjects: projects.length,
    activeProjects: projects.filter(p => p.status === 'active').length,
    
    memoryEntries: memories.length,
  };

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ComponentType<{ className?: string }>;
    color: string;
    change?: string;
  }> = ({ title, value, icon: Icon, color, change }) => (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400">{title}</p>
          <p className={`text-2xl font-bold ${color}`}>{value}</p>
          {change && (
            <p className="text-xs text-gray-500 mt-1">{change}</p>
          )}
        </div>
        <Icon className={`w-8 h-8 ${color}`} />
      </div>
    </div>
  );

  const AgentStatusCard: React.FC<{
    agent: any;
  }> = ({ agent }) => (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-medium text-white">{agent.name}</h4>
        <span className={`px-2 py-1 rounded-full text-xs ${getAgentStatusColor(agent.status)}`}>
          {agent.status}
        </span>
      </div>
      <p className="text-sm text-gray-400 mb-2">{agent.description}</p>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Tasks: {agent.stats.tasks_completed}</span>
        <span>Tokens: {formatNumber(agent.stats.total_tokens_used)}</span>
      </div>
    </div>
  );

  const TaskStatusCard: React.FC<{
    task: any;
  }> = ({ task }) => (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-medium text-white truncate">{task.content.substring(0, 50)}...</h4>
        <span className={`px-2 py-1 rounded-full text-xs ${getTaskStatusColor(task.status)}`}>
          {task.status}
        </span>
      </div>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>{task.type}</span>
        <span>{formatRelativeTime(task.created_at)}</span>
      </div>
    </div>
  );

  return (
    <div className="p-6 bg-gray-900 min-h-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">OmniDev Supreme - The One Platform to Rule Them All</p>
      </div>

      {/* System Status */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white">System Status</h2>
          <div className="flex items-center space-x-2">
            {connected ? (
              <div className="flex items-center space-x-1 text-green-400">
                <WifiIcon className="w-4 h-4" />
                <span className="text-sm">Connected</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1 text-red-400">
                <ExclamationTriangleIcon className="w-4 h-4" />
                <span className="text-sm">Disconnected</span>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Agents"
            value={stats.totalAgents}
            icon={CpuChipIcon}
            color="text-blue-400"
            change="29 integrated"
          />
          <StatCard
            title="Active Tasks"
            value={stats.activeTasks}
            icon={ClipboardDocumentListIcon}
            color="text-yellow-400"
            change={`${stats.completedTasks} completed`}
          />
          <StatCard
            title="Projects"
            value={stats.totalProjects}
            icon={CubeIcon}
            color="text-green-400"
            change={`${stats.activeProjects} active`}
          />
          <StatCard
            title="Memory Entries"
            value={formatNumber(stats.memoryEntries)}
            icon={DocumentTextIcon}
            color="text-purple-400"
            change="Growing"
          />
        </div>
      </div>

      {/* Agent Status Overview */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Agent Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
            <div className="flex items-center space-x-2 mb-2">
              <CheckCircleIcon className="w-5 h-5 text-green-400" />
              <span className="text-green-400">Idle</span>
            </div>
            <p className="text-2xl font-bold text-white">{stats.idleAgents}</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
            <div className="flex items-center space-x-2 mb-2">
              <ClockIcon className="w-5 h-5 text-yellow-400" />
              <span className="text-yellow-400">Active</span>
            </div>
            <p className="text-2xl font-bold text-white">{stats.activeAgents}</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
            <div className="flex items-center space-x-2 mb-2">
              <XCircleIcon className="w-5 h-5 text-red-400" />
              <span className="text-red-400">Error</span>
            </div>
            <p className="text-2xl font-bold text-white">{stats.errorAgents}</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
            <div className="flex items-center space-x-2 mb-2">
              <ChartBarIcon className="w-5 h-5 text-blue-400" />
              <span className="text-blue-400">Total</span>
            </div>
            <p className="text-2xl font-bold text-white">{stats.totalAgents}</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Agent Activity */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Recent Agent Activity</h3>
          <div className="space-y-4">
            {agents.slice(0, 5).map(agent => (
              <AgentStatusCard key={agent.id} agent={agent} />
            ))}
          </div>
        </div>

        {/* Recent Tasks */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Recent Tasks</h3>
          <div className="space-y-4">
            {tasks.slice(0, 5).map(task => (
              <TaskStatusCard key={task.id} task={task} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;