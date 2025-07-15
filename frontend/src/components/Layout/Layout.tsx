import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import Header from './Header';
import Sidebar from './Sidebar';
import BottomPanel from './BottomPanel';
import RightPanel from './RightPanel';
import { UI_CONSTANTS } from '@/utils/constants';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { sidebar, bottomPanel, rightPanel } = useSelector((state: RootState) => state.ui);

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Sidebar */}
      {sidebar.isOpen && (
        <div 
          className="flex-shrink-0 bg-gray-800 border-r border-gray-600"
          style={{ width: UI_CONSTANTS.SIDEBAR_WIDTH }}
        >
          <Sidebar />
        </div>
      )}

      {/* Main content area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Header */}
        <div 
          className="flex-shrink-0 bg-gray-800 border-b border-gray-600"
          style={{ height: UI_CONSTANTS.HEADER_HEIGHT }}
        >
          <Header />
        </div>

        {/* Content and panels */}
        <div className="flex flex-1 overflow-hidden">
          {/* Main content */}
          <div className="flex flex-col flex-1 overflow-hidden">
            {/* Page content */}
            <div 
              className="flex-1 overflow-auto"
              style={{ 
                marginBottom: bottomPanel.isOpen ? bottomPanel.height : 0 
              }}
            >
              {children}
            </div>

            {/* Bottom panel */}
            {bottomPanel.isOpen && (
              <div 
                className="flex-shrink-0 bg-gray-800 border-t border-gray-600"
                style={{ height: bottomPanel.height }}
              >
                <BottomPanel />
              </div>
            )}
          </div>

          {/* Right panel */}
          {rightPanel.isOpen && (
            <div 
              className="flex-shrink-0 bg-gray-800 border-l border-gray-600"
              style={{ width: rightPanel.width }}
            >
              <RightPanel />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Layout;