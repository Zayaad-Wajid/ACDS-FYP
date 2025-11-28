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
import { DashboardProvider } from "./context/DashboardContext";

function App() {
  return (
    <DashboardProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="phishing" element={<PhishingModule />} />
            <Route path="logs" element={<Logs />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Router>
    </DashboardProvider>
  );
}

export default App;
