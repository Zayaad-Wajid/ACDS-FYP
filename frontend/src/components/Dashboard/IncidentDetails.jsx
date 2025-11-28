import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Button } from "../ui/Button";
import { useDashboard } from "../../context/DashboardContext";

const IncidentDetails = () => {
  const { selectedIncident } = useDashboard();

  if (!selectedIncident) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 h-full flex items-center justify-center">
        <p className="text-slate-500">Select an email to view details</p>
      </Card>
    );
  }

  return (
    <Card className="bg-slate-900/50 border-slate-800 h-full">
      <CardHeader>
        <CardTitle className="text-slate-200">Incident Details</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 gap-4 text-sm">
          <div>
            <p className="text-slate-500 text-xs">Date & Time</p>
            <p className="text-slate-200">{selectedIncident.date}</p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">Sender</p>
            <p className="text-slate-200 break-all">
              {selectedIncident.sender}
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">Subject</p>
            <p className="text-slate-200">{selectedIncident.subject}</p>
          </div>
        </div>

        <div>
          <p className="text-slate-500 text-xs mb-1">Confidence</p>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-slate-100">
              {selectedIncident.confidence}%
            </span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full ${
                selectedIncident.prediction === "Phishing"
                  ? "bg-red-900/50 text-red-200"
                  : "bg-green-900/50 text-green-200"
              }`}
            >
              {selectedIncident.prediction}
            </span>
          </div>
        </div>

        <div>
          <p className="text-slate-500 text-xs mb-1">Explanation</p>
          <p className="text-slate-300 text-sm leading-relaxed bg-slate-800/50 p-3 rounded-md border border-slate-700">
            {selectedIncident.explanation}
          </p>
        </div>

        <div>
          <p className="text-slate-500 text-xs mb-1">Automated Action</p>
          <p className="text-blue-300 text-sm font-medium">
            {selectedIncident.action}
          </p>
        </div>

        <div className="pt-4 border-t border-slate-800">
          <p className="text-slate-500 text-xs mb-2">Analyst Feedback</p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              className="flex-1 border-green-900/50 text-green-400 hover:bg-green-900/20 hover:text-green-300"
            >
              True Positive
            </Button>
            <Button
              variant="outline"
              className="flex-1 border-red-900/50 text-red-400 hover:bg-red-900/20 hover:text-red-300"
            >
              False Positive
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default IncidentDetails;
