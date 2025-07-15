import React from 'react';

interface NotificationProviderProps {
  children: React.ReactNode;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  // Simple notification provider - can be enhanced later
  return <>{children}</>;
};