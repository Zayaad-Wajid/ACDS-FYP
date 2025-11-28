import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { useDashboard } from "../../context/DashboardContext";

const ThreatsOverTimeChart = () => {
  const { threatsOverTimeData } = useDashboard();

  return (
    <Card className="col-span-2 bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-slate-200">
          Phishing Detections Over Time
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[200px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={threatsOverTimeData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#1e293b"
                vertical={false}
              />
              <XAxis
                dataKey="time"
                stroke="#64748b"
                tick={{ fill: "#64748b", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="#64748b"
                tick={{ fill: "#64748b", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#1e293b",
                  color: "#f1f5f9",
                }}
                itemStyle={{ color: "#f1f5f9" }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#60a5fa"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: "#60a5fa" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default ThreatsOverTimeChart;
