import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import { websocketManager } from './utils/websocket';

// Layout components
import Layout from './components/Layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import Editor from './pages/Editor';
import Agents from './pages/Agents';
import Projects from './pages/Projects';
import Memory from './pages/Memory';
import Tasks from './pages/Tasks';
import Settings from './pages/Settings';

// Providers
import { NotificationProvider } from './components/Notifications/NotificationProvider';
import { ThemeProvider } from './components/Theme/ThemeProvider';

function App() {
  useEffect(() => {
    // Initialize WebSocket connection
    websocketManager.connect();
    
    // Cleanup on unmount
    return () => {
      websocketManager.disconnect();
    };
  }, []);

  return (
    <Provider store={store}>
      <ThemeProvider>
        <NotificationProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/editor" element={<Editor />} />
                <Route path="/agents" element={<Agents />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/memory" element={<Memory />} />
                <Route path="/tasks" element={<Tasks />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </Layout>
          </Router>
        </NotificationProvider>
      </ThemeProvider>
    </Provider>
  );
}

export default App;