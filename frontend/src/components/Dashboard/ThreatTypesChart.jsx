import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { useDashboard } from "../../context/DashboardContext";

const ThreatTypesChart = () => {
  const dashboardData = useDashboard() || {};
  const { threatTypesData = [] } = dashboardData;
  const colors = ["#64748b", "#3b82f6", "#1e3a5f"];

  // Ensure data is an array
  const safeData = Array.isArray(threatTypesData) ? threatTypesData : [];

  // Take top 3 for the legend display
  const topThreats = safeData.slice(0, 3);

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">
        Top Threat Types
      </h3>
      <div className="flex gap-6">
        {/* Legend */}
        <div className="flex flex-col justify-center space-y-3">
          {topThreats.map((item, index) => (
            <div key={item?.name || index} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-sm"
                style={{ backgroundColor: colors[index] }}
              />
              <span className="text-xs text-slate-400">
                {item?.name || "Unknown"}
              </span>
            </div>
          ))}
        </div>
        {/* Chart */}
        <div className="h-[150px] flex-1">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topThreats}>
              <XAxis dataKey="name" hide />
              <YAxis hide />
              <Tooltip
                cursor={{ fill: "#1e293b" }}
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#334155",
                  color: "#f1f5f9",
                  fontSize: 12,
                }}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]} barSize={40}>
                {topThreats.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={colors[index % colors.length]}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ThreatTypesChart;
