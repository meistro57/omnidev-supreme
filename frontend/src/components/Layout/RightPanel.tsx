import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';

const RightPanel: React.FC = () => {
  const { activePanel } = useSelector((state: RootState) => state.ui.rightPanel);

  return (
    <div className="h-full bg-gray-800 border-l border-gray-600 p-4">
      <div className="text-white">
        <h3 className="text-lg font-semibold mb-4">
          {activePanel === 'agent-details' && 'Agent Details'}
          {activePanel === 'memory-search' && 'Memory Search'}
          {activePanel === 'project-info' && 'Project Info'}
        </h3>
        
        <div className="text-sm text-gray-400">
          {activePanel === 'agent-details' && 'Detailed agent information'}
          {activePanel === 'memory-search' && 'Search memory and knowledge'}
          {activePanel === 'project-info' && 'Project details and settings'}
        </div>
      </div>
    </div>
  );
};

export default RightPanel;