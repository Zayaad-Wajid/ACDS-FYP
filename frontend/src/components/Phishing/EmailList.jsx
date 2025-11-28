import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { useDashboard } from "../../context/DashboardContext";
import { fetchIncidentDetails } from "../../utils/api";

const EmailList = () => {
  const { allEmails, setSelectedIncident } = useDashboard();

  const handleRowClick = async (id) => {
    const details = await fetchIncidentDetails(id);
    setSelectedIncident(details);
  };

  return (
    <Card className="bg-slate-900/50 border-slate-800 h-full">
      <CardHeader>
        <CardTitle className="text-slate-200">Scanned Emails</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase bg-slate-900/50 border-b border-slate-800">
              <tr>
                <th className="px-6 py-3">Sender</th>
                <th className="px-6 py-3">Subject</th>
                <th className="px-6 py-3">Features</th>
                <th className="px-6 py-3">Confidence</th>
                <th className="px-6 py-3">Prediction</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {allEmails.map((email) => (
                <tr
                  key={email.id}
                  onClick={() => handleRowClick(email.id)}
                  className="hover:bg-slate-800/30 transition-colors cursor-pointer"
                >
                  <td className="px-6 py-4 text-slate-300 break-all max-w-[200px]">
                    {email.sender}
                  </td>
                  <td className="px-6 py-4 text-slate-300 max-w-[200px] truncate">
                    {email.subject}
                  </td>
                  <td className="px-6 py-4 text-slate-400 text-xs">
                    {email.features
                      ? Object.keys(email.features).length + " extracted"
                      : "N/A"}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-slate-700 rounded-full h-1.5 max-w-[60px]">
                        <div
                          className={`h-1.5 rounded-full ${
                            email.confidence > 80
                              ? "bg-red-500"
                              : "bg-green-500"
                          }`}
                          style={{ width: `${email.confidence}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-slate-400">
                        {email.confidence}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <Badge
                      variant={
                        email.prediction === "Phishing"
                          ? "destructive"
                          : "success"
                      }
                    >
                      {email.prediction}
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

export default EmailList;
