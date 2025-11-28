import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { useDashboard } from "../../context/DashboardContext";

const ModelPerformanceLogs = () => {
  const { logs } = useDashboard();

  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-slate-200">Model Performance Logs</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase bg-slate-900/50 border-b border-slate-800">
              <tr>
                <th className="px-6 py-3">Date</th>
                <th className="px-6 py-3">Threat Type</th>
                <th className="px-6 py-3">Analyst Decision</th>
                <th className="px-6 py-3">Action</th>
                <th className="px-6 py-3">Model Version</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {logs.map((log) => (
                <tr
                  key={log.id}
                  className="hover:bg-slate-800/30 transition-colors"
                >
                  <td className="px-6 py-4 text-slate-300">{log.date}</td>
                  <td className="px-6 py-4 text-slate-300">{log.type}</td>
                  <td className="px-6 py-4 text-slate-300">{log.decision}</td>
                  <td className="px-6 py-4 text-slate-300">{log.action}</td>
                  <td className="px-6 py-4 text-slate-400 font-mono text-xs">
                    {log.modelVersion}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
};

export default ModelPerformanceLogs;
