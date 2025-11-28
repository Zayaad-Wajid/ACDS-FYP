import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { useDashboard } from "../../context/DashboardContext";
import { fetchIncidentDetails } from "../../utils/api";

const ThreatMonitoringTable = () => {
  const { threats, setSelectedIncident } = useDashboard();

  const handleRowClick = async (id) => {
    const details = await fetchIncidentDetails(id);
    setSelectedIncident(details);
  };

  return (
    <Card className="col-span-2 bg-slate-900/50 border-slate-800 h-full">
      <CardHeader>
        <CardTitle className="text-slate-200">Email Monitoring</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase bg-slate-900/50 border-b border-slate-800">
              <tr>
                <th className="px-6 py-3">Time</th>
                <th className="px-6 py-3">Sender Email</th>
                <th className="px-6 py-3">Subject</th>
                <th className="px-6 py-3">Confidence (%)</th>
                <th className="px-6 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {threats.map((threat) => (
                <tr
                  key={threat.id}
                  onClick={() => handleRowClick(threat.id)}
                  className="hover:bg-slate-800/30 transition-colors cursor-pointer"
                >
                  <td className="px-6 py-4 font-medium text-slate-300">
                    {threat.time}
                  </td>
                  <td className="px-6 py-4 text-slate-300">{threat.sender}</td>
                  <td className="px-6 py-4 text-slate-300">{threat.subject}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-slate-700 rounded-full h-1.5 max-w-[60px]">
                        <div
                          className={`h-1.5 rounded-full ${
                            threat.confidence > 80
                              ? "bg-red-500"
                              : "bg-yellow-500"
                          }`}
                          style={{ width: `${threat.confidence}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-slate-400">
                        {threat.confidence}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <Badge
                      variant={
                        threat.status === "Phishing" ? "destructive" : "success"
                      }
                    >
                      {threat.status}
                    </Badge>
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

export default ThreatMonitoringTable;
