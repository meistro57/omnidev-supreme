import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';

const Sidebar: React.FC = () => {
  const { activePanel } = useSelector((state: RootState) => state.ui.sidebar);

  return (
    <div className="h-full bg-gray-800 border-r border-gray-600 p-4">
      <div className="text-white">
        <h3 className="text-lg font-semibold mb-4">
          {activePanel === 'agents' && 'Agents'}
          {activePanel === 'memory' && 'Memory'}
          {activePanel === 'projects' && 'Projects'}
          {activePanel === 'files' && 'Files'}
        </h3>
        
        <div className="text-sm text-gray-400">
          {activePanel === 'agents' && 'Agent management panel'}
          {activePanel === 'memory' && 'Memory search and management'}
          {activePanel === 'projects' && 'Project workspace'}
          {activePanel === 'files' && 'File explorer'}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;