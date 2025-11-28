import React from "react";
import StatsCard from "../components/Dashboard/StatsCard";
import ThreatsOverTimeChart from "../components/Dashboard/ThreatsOverTimeChart";
import ThreatTypesChart from "../components/Dashboard/ThreatTypesChart";
import ThreatMonitoringTable from "../components/Dashboard/ThreatMonitoringTable";
import IncidentDetails from "../components/Dashboard/IncidentDetails";
import ModelPerformanceMetrics from "../components/Dashboard/ModelPerformanceMetrics";
import ModelPerformanceLogs from "../components/Dashboard/ModelPerformanceLogs";
import { useDashboard } from "../context/DashboardContext";

const Dashboard = () => {
  const { stats } = useDashboard();

  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <p className="text-xs uppercase tracking-[0.35em] text-slate-500">
          Autonomous Cyber Defense System
        </p>
        <h1 className="text-3xl font-bold text-slate-100">
          Email Phishing Command Center
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Real-time visibility into phishing activity, automated containment,
          and SOC feedback loops to keep your enterprise inbox secure.
        </p>
      </header>

      <section className="space-y-4">
        <h2 className="text-sm uppercase tracking-wide text-slate-400">
          Overview
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Total Threats"
            value={stats.totalThreats}
            subtext="Detected in the last 24h"
          />
          <StatsCard
            title="Active Threats"
            value={stats.activeThreats}
            subtext="Currently under investigation"
          />
          <StatsCard
            title="Auto-Resolved Threats"
            value={stats.autoResolved}
            subtext="Closed by automation"
          />
          <StatsCard
            title="Accuracy"
            value={`${stats.accuracy}%`}
            subtext="Model precision this week"
          />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm uppercase tracking-wide text-slate-400">
          Threat Intelligence
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ThreatsOverTimeChart />
          <ThreatTypesChart />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm uppercase tracking-wide text-slate-400">
          Threat Monitoring
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ThreatMonitoringTable />
          <IncidentDetails />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm uppercase tracking-wide text-slate-400">
          Model Performance
        </h2>
        <ModelPerformanceMetrics />
      </section>

      <section className="space-y-4">
        <h2 className="text-sm uppercase tracking-wide text-slate-400">
          Model Audit Trail
        </h2>
        <ModelPerformanceLogs />
      </section>
    </div>
  );
};

export default Dashboard;
