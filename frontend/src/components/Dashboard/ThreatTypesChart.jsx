import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { useDashboard } from "../../context/DashboardContext";

const ThreatTypesChart = () => {
  const { threatTypesData } = useDashboard();
  const colors = ["#3b82f6", "#60a5fa", "#93c5fd"];

  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-slate-200">Phishing Categories</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[200px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={threatTypesData} layout="vertical">
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#1e293b"
                horizontal={false}
              />
              <XAxis type="number" hide />
              <YAxis
                dataKey="name"
                type="category"
                width={100}
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip
                cursor={{ fill: "#1e293b" }}
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#1e293b",
                  color: "#f1f5f9",
                }}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
                {threatTypesData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={colors[index % colors.length]}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default ThreatTypesChart;
