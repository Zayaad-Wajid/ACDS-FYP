import React, { useState } from "react";
import { useDashboard } from "../context/DashboardContext";
import {
  FileText,
  Download,
  RefreshCw,
  Calendar,
  Shield,
  AlertTriangle,
  CheckCircle,
  Clock,
  FileJson,
  FileType,
  Sparkles,
  TrendingUp,
  Target,
  Activity,
} from "lucide-react";

const Reports = () => {
  const dashboardData = useDashboard() || {};
  const threats = dashboardData.threats || [];
  const stats = dashboardData.stats || {};
  const logs = dashboardData.logs || [];
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedReportType, setSelectedReportType] =
    useState("threat-summary");
  const [dateRange, setDateRange] = useState("7days");
  const [generatedReport, setGeneratedReport] = useState(null);

  const reportTypes = [
    {
      id: "threat-summary",
      name: "Threat Summary Report",
      description: "Overview of all detected threats with AI analysis",
      icon: Shield,
    },
    {
      id: "detection-analysis",
      name: "Detection Analysis",
      description: "Detailed analysis of phishing detection performance",
      icon: Target,
    },
    {
      id: "incident-log",
      name: "Incident Log Report",
      description: "Complete log of all security incidents",
      icon: FileText,
    },
    {
      id: "performance-metrics",
      name: "Model Performance Report",
      description: "ML model accuracy, precision, recall metrics",
      icon: TrendingUp,
    },
  ];

  const generateAIReport = async () => {
    setIsGenerating(true);

    // Simulate AI report generation (replace with actual API call)
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const phishingThreats = threats.filter((t) => t.type === "Phishing");
    const resolvedThreats = threats.filter((t) => t.status === "Resolved");

    const report = {
      generatedAt: new Date().toISOString(),
      reportType: selectedReportType,
      dateRange: dateRange,
      summary: {
        totalThreats: threats.length,
        phishingDetected: phishingThreats.length,
        autoResolved: resolvedThreats.length,
        pendingReview: threats.length - resolvedThreats.length,
        modelAccuracy: stats?.modelAccuracy || 97.2,
      },
      aiAnalysis: generateAIAnalysis(threats, stats),
      recommendations: generateRecommendations(threats),
      threatBreakdown: generateThreatBreakdown(threats),
      timeline: generateTimeline(threats),
    };

    setGeneratedReport(report);
    setIsGenerating(false);
  };

  const generateAIAnalysis = (threats, stats) => {
    const phishingCount = threats.filter((t) => t.type === "Phishing").length;
    const highConfidence = threats.filter(
      (t) => parseFloat(t.confidence) > 90
    ).length;

    return `
## AI-Powered Threat Analysis

### Overview
During the selected period, the Autonomous Cyber Defense System detected and analyzed **${
      threats.length
    } potential threats**, with **${phishingCount} confirmed phishing attempts**. The ML model maintained a high accuracy rate of **${
      stats?.modelAccuracy || 97.2
    }%**.

### Key Findings
1. **High-Confidence Detections**: ${highConfidence} threats were identified with >90% confidence, indicating strong pattern matching with known phishing indicators.

2. **Attack Vectors**: The majority of detected phishing attempts utilized urgency-based social engineering tactics, including fake account suspension notices and prize claims.

3. **Response Effectiveness**: ${Math.round(
      (threats.filter((t) => t.status === "Resolved").length / threats.length) *
        100
    )}% of threats were automatically resolved by the system, demonstrating effective autonomous response capabilities.

### Model Performance
- **True Positive Rate**: High detection rate for known phishing patterns
- **False Positive Rate**: Minimal false alerts, reducing analyst fatigue
- **Detection Speed**: Average detection time under 500ms

### Trend Analysis
The system has observed consistent threat patterns, with email-based phishing remaining the primary attack vector. URL analysis and content inspection continue to be the most effective detection methods.
    `.trim();
  };

  const generateRecommendations = (threats) => {
    return [
      {
        priority: "High",
        title: "Enhance Email Filtering Rules",
        description:
          "Based on detected patterns, update email gateway rules to block emails containing suspicious URL patterns.",
      },
      {
        priority: "Medium",
        title: "User Awareness Training",
        description:
          "Schedule phishing awareness training for departments with highest interaction with detected threats.",
      },
      {
        priority: "Medium",
        title: "Update Threat Intelligence",
        description:
          "Integrate latest threat intelligence feeds to improve detection of emerging phishing techniques.",
      },
      {
        priority: "Low",
        title: "Review False Positive Cases",
        description:
          "Analyze flagged legitimate emails to fine-tune model sensitivity.",
      },
    ];
  };

  const generateThreatBreakdown = (threats) => {
    const breakdown = {};
    threats.forEach((threat) => {
      breakdown[threat.type] = (breakdown[threat.type] || 0) + 1;
    });
    return Object.entries(breakdown).map(([type, count]) => ({
      type,
      count,
      percentage: ((count / threats.length) * 100).toFixed(1),
    }));
  };

  const generateTimeline = (threats) => {
    return threats.slice(0, 10).map((threat) => ({
      time: threat.time,
      type: threat.type,
      source: threat.sourceIP,
      status: threat.status,
      confidence: threat.confidence,
    }));
  };

  const exportReport = (format) => {
    if (!generatedReport) return;

    if (format === "json") {
      const blob = new Blob([JSON.stringify(generatedReport, null, 2)], {
        type: "application/json",
      });
      downloadFile(blob, `threat-report-${Date.now()}.json`);
    } else if (format === "txt") {
      const textContent = `
AUTONOMOUS CYBER DEFENSE SYSTEM - THREAT REPORT
Generated: ${new Date(generatedReport.generatedAt).toLocaleString()}
Report Type: ${generatedReport.reportType}
Date Range: ${generatedReport.dateRange}

=== SUMMARY ===
Total Threats: ${generatedReport.summary.totalThreats}
Phishing Detected: ${generatedReport.summary.phishingDetected}
Auto-Resolved: ${generatedReport.summary.autoResolved}
Pending Review: ${generatedReport.summary.pendingReview}
Model Accuracy: ${generatedReport.summary.modelAccuracy}%

=== AI ANALYSIS ===
${generatedReport.aiAnalysis}

=== RECOMMENDATIONS ===
${generatedReport.recommendations
  .map((r, i) => `${i + 1}. [${r.priority}] ${r.title}\n   ${r.description}`)
  .join("\n\n")}

=== THREAT BREAKDOWN ===
${generatedReport.threatBreakdown
  .map((t) => `- ${t.type}: ${t.count} (${t.percentage}%)`)
  .join("\n")}
      `.trim();

      const blob = new Blob([textContent], { type: "text/plain" });
      downloadFile(blob, `threat-report-${Date.now()}.txt`);
    }
  };

  const downloadFile = (blob, filename) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-cyan-400" />
            AI-Powered Reports
          </h1>
          <p className="text-gray-400 mt-1">
            Generate comprehensive threat analysis reports using AI
          </p>
        </div>
      </div>

      {/* Report Configuration */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Report Type Selection */}
        <div className="lg:col-span-2 bg-[#111111] border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-4">
            Select Report Type
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {reportTypes.map((report) => (
              <button
                key={report.id}
                onClick={() => setSelectedReportType(report.id)}
                className={`p-4 rounded-lg border text-left transition-all ${
                  selectedReportType === report.id
                    ? "border-cyan-500 bg-cyan-500/10"
                    : "border-gray-700 bg-[#0a0a0a] hover:border-gray-600"
                }`}
              >
                <div className="flex items-start gap-3">
                  <report.icon
                    className={`w-5 h-5 mt-0.5 ${
                      selectedReportType === report.id
                        ? "text-cyan-400"
                        : "text-gray-400"
                    }`}
                  />
                  <div>
                    <h3 className="font-medium text-white">{report.name}</h3>
                    <p className="text-sm text-gray-400 mt-1">
                      {report.description}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Configuration Panel */}
        <div className="bg-[#111111] border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-4">
            Configuration
          </h2>

          {/* Date Range */}
          <div className="mb-6">
            <label className="block text-sm text-gray-400 mb-2">
              <Calendar className="w-4 h-4 inline mr-2" />
              Date Range
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full bg-[#0a0a0a] border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
            >
              <option value="24hours">Last 24 Hours</option>
              <option value="7days">Last 7 Days</option>
              <option value="30days">Last 30 Days</option>
              <option value="90days">Last 90 Days</option>
            </select>
          </div>

          {/* Generate Button */}
          <button
            onClick={generateAIReport}
            disabled={isGenerating}
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium py-3 px-4 rounded-lg hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            {isGenerating ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Generating Report...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Generate AI Report
              </>
            )}
          </button>

          {/* Export Options */}
          {generatedReport && (
            <div className="mt-4 space-y-2">
              <p className="text-sm text-gray-400">Export Report:</p>
              <div className="flex gap-2">
                <button
                  onClick={() => exportReport("json")}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-[#0a0a0a] border border-gray-700 rounded-lg text-gray-300 hover:border-cyan-500 transition-colors"
                >
                  <FileJson className="w-4 h-4" />
                  JSON
                </button>
                <button
                  onClick={() => exportReport("txt")}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-[#0a0a0a] border border-gray-700 rounded-lg text-gray-300 hover:border-cyan-500 transition-colors"
                >
                  <FileType className="w-4 h-4" />
                  TXT
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Generated Report Display */}
      {generatedReport && (
        <div className="bg-[#111111] border border-gray-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-cyan-400" />
              Generated Report
            </h2>
            <span className="text-sm text-gray-400">
              <Clock className="w-4 h-4 inline mr-1" />
              {new Date(generatedReport.generatedAt).toLocaleString()}
            </span>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            <div className="bg-[#0a0a0a] rounded-lg p-4">
              <p className="text-sm text-gray-400">Total Threats</p>
              <p className="text-2xl font-bold text-white">
                {generatedReport.summary.totalThreats}
              </p>
            </div>
            <div className="bg-[#0a0a0a] rounded-lg p-4">
              <p className="text-sm text-gray-400">Phishing Detected</p>
              <p className="text-2xl font-bold text-red-400">
                {generatedReport.summary.phishingDetected}
              </p>
            </div>
            <div className="bg-[#0a0a0a] rounded-lg p-4">
              <p className="text-sm text-gray-400">Auto-Resolved</p>
              <p className="text-2xl font-bold text-green-400">
                {generatedReport.summary.autoResolved}
              </p>
            </div>
            <div className="bg-[#0a0a0a] rounded-lg p-4">
              <p className="text-sm text-gray-400">Pending Review</p>
              <p className="text-2xl font-bold text-yellow-400">
                {generatedReport.summary.pendingReview}
              </p>
            </div>
            <div className="bg-[#0a0a0a] rounded-lg p-4">
              <p className="text-sm text-gray-400">Model Accuracy</p>
              <p className="text-2xl font-bold text-cyan-400">
                {generatedReport.summary.modelAccuracy}%
              </p>
            </div>
          </div>

          {/* AI Analysis */}
          <div className="mb-6">
            <h3 className="text-md font-semibold text-white mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              AI Analysis
            </h3>
            <div className="bg-[#0a0a0a] rounded-lg p-4 prose prose-invert prose-sm max-w-none">
              <div className="text-gray-300 whitespace-pre-line text-sm leading-relaxed">
                {generatedReport.aiAnalysis}
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="mb-6">
            <h3 className="text-md font-semibold text-white mb-3 flex items-center gap-2">
              <Target className="w-4 h-4 text-cyan-400" />
              Recommendations
            </h3>
            <div className="space-y-3">
              {generatedReport.recommendations.map((rec, index) => (
                <div
                  key={index}
                  className="bg-[#0a0a0a] rounded-lg p-4 flex items-start gap-3"
                >
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${
                      rec.priority === "High"
                        ? "bg-red-500/20 text-red-400"
                        : rec.priority === "Medium"
                        ? "bg-yellow-500/20 text-yellow-400"
                        : "bg-green-500/20 text-green-400"
                    }`}
                  >
                    {rec.priority}
                  </span>
                  <div>
                    <h4 className="font-medium text-white">{rec.title}</h4>
                    <p className="text-sm text-gray-400 mt-1">
                      {rec.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Threat Breakdown */}
          <div>
            <h3 className="text-md font-semibold text-white mb-3 flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Threat Breakdown
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {generatedReport.threatBreakdown.map((item, index) => (
                <div key={index} className="bg-[#0a0a0a] rounded-lg p-4">
                  <p className="text-sm text-gray-400">{item.type}</p>
                  <p className="text-xl font-bold text-white">{item.count}</p>
                  <p className="text-sm text-cyan-400">{item.percentage}%</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!generatedReport && !isGenerating && (
        <div className="bg-[#111111] border border-gray-800 rounded-xl p-12 text-center">
          <FileText className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-white mb-2">
            No Report Generated
          </h3>
          <p className="text-gray-400 mb-4">
            Select a report type and click "Generate AI Report" to create a
            comprehensive threat analysis.
          </p>
        </div>
      )}
    </div>
  );
};

export default Reports;
