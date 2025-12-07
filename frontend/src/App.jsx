import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Layout from "./components/Layout/Layout";
import Dashboard from "./pages/Dashboard";
import PhishingModule from "./pages/PhishingModule";
import Logs from "./pages/Logs";
import Login from "./pages/Login";
import Reports from "./pages/Reports";
import AutomatedTesting from "./pages/AutomatedTesting";
import ConnectionTest from "./components/ConnectionTest";
import { DashboardProvider } from "./context/DashboardContext";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/Auth/ProtectedRoute";

// Wrapper for protected layout routes
const ProtectedLayout = () => {
  return (
    <ProtectedRoute>
      <Layout />
    </ProtectedRoute>
  );
};

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Public Route - Login */}
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/" replace /> : <Login />}
      />

      {/* Test Routes (public for debugging) */}
      <Route path="/test" element={<ConnectionTest />} />
      <Route path="/testing" element={<AutomatedTesting />} />

      {/* Protected Routes */}
      <Route path="/" element={<ProtectedLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="phishing" element={<PhishingModule />} />
        <Route path="logs" element={<Logs />} />
        <Route path="reports" element={<Reports />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <DashboardProvider>
        <Router>
          <AppRoutes />
        </Router>
      </DashboardProvider>
    </AuthProvider>
  );
}

export default App;
