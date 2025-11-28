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

const ModelPerformanceMetrics = () => {
  const { accuracyOverTimeData, confusionMatrixData } = useDashboard();

  return (
    <div className="grid grid-cols-3 gap-6">
      <Card className="col-span-2 bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle className="text-slate-200">Accuracy Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={accuracyOverTimeData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#1e293b"
                  vertical={false}
                />
                <XAxis dataKey="time" hide />
                <YAxis
                  domain={[60, 100]}
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
                />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#60a5fa"
                  strokeWidth={2}
                  dot={false}
                  fill="url(#colorValue)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-6">
        <Card className="bg-slate-900/50 border-slate-800">
          <CardHeader>
            <CardTitle className="text-slate-200">Confusion Matrix</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4 h-full content-center">
              <div className="bg-slate-950/50 p-4 rounded-lg text-center border border-slate-800">
                <p className="text-slate-500 text-xs uppercase tracking-wider">
                  TP
                </p>
                <p className="text-2xl font-bold text-green-400">
                  {confusionMatrixData.tp}
                </p>
              </div>
              <div className="bg-slate-950/50 p-4 rounded-lg text-center border border-slate-800">
                <p className="text-slate-500 text-xs uppercase tracking-wider">
                  FP
                </p>
                <p className="text-2xl font-bold text-red-400">
                  {confusionMatrixData.fp}
                </p>
              </div>
              <div className="bg-slate-950/50 p-4 rounded-lg text-center border border-slate-800">
                <p className="text-slate-500 text-xs uppercase tracking-wider">
                  FN
                </p>
                <p className="text-2xl font-bold text-yellow-400">
                  {confusionMatrixData.fn}
                </p>
              </div>
              <div className="bg-slate-950/50 p-4 rounded-lg text-center border border-slate-800">
                <p className="text-slate-500 text-xs uppercase tracking-wider">
                  TN
                </p>
                <p className="text-2xl font-bold text-blue-400">
                  {confusionMatrixData.tn}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800">
          <CardHeader>
            <CardTitle className="text-slate-200">Feedback Log</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between items-center px-2">
              <div className="text-center">
                <p className="text-slate-500 text-xs uppercase">
                  True Positive
                </p>
                <p className="text-xl font-bold text-green-400">12</p>
              </div>
              <div className="h-8 w-px bg-slate-800"></div>
              <div className="text-center">
                <p className="text-slate-500 text-xs uppercase">
                  False Positive
                </p>
                <p className="text-xl font-bold text-red-400">3</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ModelPerformanceMetrics;
