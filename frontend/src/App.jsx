import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { useThemeStore } from './store/themeStore';

// Layout
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import SubmissionPage from './pages/SubmissionPage';
import JobMonitorPage from './pages/JobMonitorPage';
import EvidenceDetailPage from './pages/EvidenceDetailPage';
import SettingsPage from './pages/SettingsPage';
import PlaceholderPage from './pages/PlaceholderPage'; // Import the new page

// Styles
import GlobalStyles from './styles/GlobalStyles';
import { cyberTheme, darkTheme, lightTheme } from './styles/theme';

function App() {
  const { theme } = useThemeStore();

  const getTheme = () => {
    switch (theme) {
      case 'cyber': return cyberTheme;
      case 'dark': return darkTheme;
      case 'light': return lightTheme;
      default: return cyberTheme;
    }
  };

  return (
    <ThemeProvider theme={getTheme()}>
      <GlobalStyles />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/submit" element={<SubmissionPage />} />
            
            {/* Monitor and Database point to the same list for now */}
            <Route path="/monitor" element={<JobMonitorPage />} />
            <Route path="/database" element={<JobMonitorPage />} /> 
            
            <Route path="/evidence/:jobId" element={<EvidenceDetailPage />} />
            <Route path="/settings" element={<SettingsPage />} />

            {/* Fix for missing Sidebar Links */}
            <Route path="/analytics" element={<PlaceholderPage title="Analytics Module" />} />
            <Route path="/chain-of-custody" element={<PlaceholderPage title="Global Chain of Custody" />} />
            <Route path="/security" element={<PlaceholderPage title="Security Audit" />} />
            <Route path="/help" element={<PlaceholderPage title="Documentation" />} />
            
            {/* 404 Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
