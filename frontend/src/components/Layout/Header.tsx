import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, useLocation } from 'react-router-dom';
import { RootState } from '@/store';
import { toggleSidebar } from '@/store/slices/uiSlice';
import { 
  Bars3Icon, 
  CpuChipIcon, 
  CodeBracketIcon, 
  CubeIcon, 
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  CogIcon,
  HomeIcon,
  WifiIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { formatRelativeTime } from '@/utils/formatters';

const Header: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  
  const { } = useSelector((state: RootState) => state.ui);
  const { connected, lastMessage } = useSelector((state: RootState) => state.websocket);
  const { agents } = useSelector((state: RootState) => state.agents);
  const { tasks } = useSelector((state: RootState) => state.tasks);

  const navigationItems = [
    { path: '/', icon: HomeIcon, label: 'Dashboard' },
    { path: '/editor', icon: CodeBracketIcon, label: 'Editor' },
    { path: '/agents', icon: CpuChipIcon, label: 'Agents' },
    { path: '/projects', icon: CubeIcon, label: 'Projects' },
    { path: '/memory', icon: DocumentTextIcon, label: 'Memory' },
    { path: '/tasks', icon: ClipboardDocumentListIcon, label: 'Tasks' },
  ];

  const activeAgents = agents.filter(agent => agent.status === 'busy').length;
  const activeTasks = tasks.filter(task => task.status === 'in_progress').length;

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <header className="flex items-center justify-between h-full px-4 bg-gray-800 border-b border-gray-600">
      {/* Left section */}
      <div className="flex items-center space-x-4">
        <button
          onClick={() => dispatch(toggleSidebar())}
          className="p-2 rounded-md hover:bg-gray-700 transition-colors"
        >
          <Bars3Icon className="w-5 h-5" />
        </button>
        
        <div className="flex items-center space-x-2">
          <CpuChipIcon className="w-8 h-8 text-primary-500" />
          <h1 className="text-xl font-bold text-white">OmniDev Supreme</h1>
        </div>
      </div>

      {/* Center navigation */}
      <nav className="flex items-center space-x-1">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <button
              key={item.path}
              onClick={() => handleNavigation(item.path)}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive 
                  ? 'bg-primary-600 text-white' 
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Right section */}
      <div className="flex items-center space-x-4">
        {/* Status indicators */}
        <div className="flex items-center space-x-3 text-sm">
          <div className="flex items-center space-x-1">
            <span className="text-gray-400">Agents:</span>
            <span className="text-yellow-400">{activeAgents}</span>
            <span className="text-gray-400">/</span>
            <span className="text-gray-300">{agents.length}</span>
          </div>
          
          <div className="flex items-center space-x-1">
            <span className="text-gray-400">Tasks:</span>
            <span className="text-blue-400">{activeTasks}</span>
          </div>
        </div>

        {/* Connection status */}
        <div className="flex items-center space-x-2">
          {connected ? (
            <div className="flex items-center space-x-1 text-green-400">
              <WifiIcon className="w-4 h-4" />
              <span className="text-xs">Connected</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1 text-red-400">
              <ExclamationTriangleIcon className="w-4 h-4" />
              <span className="text-xs">Disconnected</span>
            </div>
          )}
          
          {lastMessage && (
            <div className="text-xs text-gray-400">
              {formatRelativeTime(lastMessage.timestamp)}
            </div>
          )}
        </div>

        {/* Settings button */}
        <button
          onClick={() => navigate('/settings')}
          className="p-2 rounded-md hover:bg-gray-700 transition-colors"
        >
          <CogIcon className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

export default Header;