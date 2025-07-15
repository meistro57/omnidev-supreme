import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';

const BottomPanel: React.FC = () => {
  const { activePanel } = useSelector((state: RootState) => state.ui.bottomPanel);

  return (
    <div className="h-full bg-gray-800 border-t border-gray-600 p-4">
      <div className="text-white">
        <h3 className="text-lg font-semibold mb-4">
          {activePanel === 'tasks' && 'Tasks'}
          {activePanel === 'console' && 'Console'}
          {activePanel === 'terminal' && 'Terminal'}
        </h3>
        
        <div className="text-sm text-gray-400">
          {activePanel === 'tasks' && 'Task execution and monitoring'}
          {activePanel === 'console' && 'System console output'}
          {activePanel === 'terminal' && 'Integrated terminal'}
        </div>
      </div>
    </div>
  );
};

export default BottomPanel;