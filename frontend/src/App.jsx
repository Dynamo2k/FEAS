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
import PlaceholderPage from './pages/PlaceholderPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import AnalyticsPage from './pages/AnalyticsPage';

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
        <Routes>
          {/* Auth Routes (without Layout) */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Main App Routes (with Layout) */}
          <Route path="/" element={<Layout><Navigate to="/dashboard" replace /></Layout>} />
          <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
          <Route path="/submit" element={<Layout><SubmissionPage /></Layout>} />
          
          {/* Monitor and Database point to the same list for now */}
          <Route path="/monitor" element={<Layout><JobMonitorPage /></Layout>} />
          <Route path="/database" element={<Layout><JobMonitorPage /></Layout>} />
          
          <Route path="/evidence/:jobId" element={<Layout><EvidenceDetailPage /></Layout>} />
          <Route path="/settings" element={<Layout><SettingsPage /></Layout>} />
          <Route path="/profile" element={<Layout><ProfilePage /></Layout>} />

          {/* Feature Pages */}
          <Route path="/analytics" element={<Layout><AnalyticsPage /></Layout>} />
          <Route path="/chain-of-custody" element={<Layout><PlaceholderPage title="Global Chain of Custody" /></Layout>} />
          <Route path="/security" element={<Layout><PlaceholderPage title="Security Audit" /></Layout>} />
          <Route path="/help" element={<Layout><PlaceholderPage title="Documentation" /></Layout>} />
          
          {/* 404 Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
