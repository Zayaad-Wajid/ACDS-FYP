import React from "react";
import { useDashboard } from "../../context/DashboardContext";

const ModelPerformanceLogs = () => {
  const dashboardData = useDashboard() || {};
  const { logs = [] } = dashboardData;

  // Ensure logs is an array
  const safeLogs = Array.isArray(logs) ? logs : [];

  return (
    <div>
      <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
        Model Performance
      </h2>
      <div className="bg-slate-900/60 border border-slate-800 rounded-lg">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-500 uppercase bg-slate-900/30">
              <tr>
                <th className="px-4 py-3">Date</th>
                <th className="px-4 py-3">Threat Type</th>
                <th className="px-4 py-3">Analyst Decision</th>
                <th className="px-4 py-3">Action</th>
                <th className="px-4 py-3">Model Version</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {safeLogs.map((log, index) => (
                <tr
                  key={log?.id || index}
                  className="hover:bg-slate-800/30 transition-colors"
                >
                  <td className="px-4 py-3 text-slate-400 font-mono text-xs">
                    {log?.date || "N/A"}
                  </td>
                  <td className="px-4 py-3 text-slate-300">
                    {log?.type || "N/A"}
                  </td>
                  <td className="px-4 py-3 text-green-400 text-xs">
                    {log?.decision || "N/A"}
                  </td>
                  <td className="px-4 py-3 text-slate-300">
                    {log?.action || "N/A"}
                  </td>
                  <td className="px-4 py-3 text-slate-500 font-mono text-xs">
                    {log?.modelVersion || "N/A"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ModelPerformanceLogs;
