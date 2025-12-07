import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import {
  fetchStats,
  fetchThreatsOverTime,
  fetchThreatTypes,
  fetchAccuracyOverTime,
  fetchConfusionMatrix,
  fetchThreats,
  fetchIncidentDetails,
  fetchModelLogs,
  fetchAllEmails,
  runAutomatedTest,
  getTestSession,
  getTestLogs,
  getTestReports,
} from "../utils/api";

const DashboardContext = createContext();

export const useDashboard = () => useContext(DashboardContext);

export const DashboardProvider = ({ children }) => {
  const [stats, setStats] = useState({
    totalEmails: 0,
    phishingDetected: 0,
    safeEmails: 0,
    accuracy: 0,
  });
  const [threats, setThreats] = useState([]);
  const [allEmails, setAllEmails] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [logs, setLogs] = useState([]);
  const [threatsOverTimeData, setThreatsOverTimeData] = useState([]);
  const [threatTypesData, setThreatTypesData] = useState([]);
  const [accuracyOverTimeData, setAccuracyOverTimeData] = useState([]);
  const [confusionMatrixData, setConfusionMatrixData] = useState({
    tp: 0,
    fp: 0,
    fn: 0,
    tn: 0,
  });
  const [loading, setLoading] = useState(true);

  // Testing state
  const [testRunning, setTestRunning] = useState(false);
  const [currentTestSession, setCurrentTestSession] = useState(null);
  const [testResults, setTestResults] = useState([]);
  const [testLogs, setTestLogs] = useState([]);
  const [liveThreats, setLiveThreats] = useState([]);
  const [responseActions, setResponseActions] = useState([]);
  const [testReports, setTestReports] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [
          statsData,
          threatsData,
          allEmailsData,
          logsData,
          totData,
          ttData,
          aotData,
          cmData,
        ] = await Promise.all([
          fetchStats(),
          fetchThreats(),
          fetchAllEmails(),
          fetchModelLogs(),
          fetchThreatsOverTime(),
          fetchThreatTypes(),
          fetchAccuracyOverTime(),
          fetchConfusionMatrix(),
        ]);

        setStats(statsData);
        setThreats(threatsData);
        setAllEmails(allEmailsData);
        // Fetch first incident details if threats exist
        if (threatsData.length > 0) {
          const firstIncident = await fetchIncidentDetails(threatsData[0].id);
          setSelectedIncident(firstIncident);
        }
        setLogs(logsData);
        setThreatsOverTimeData(totData);
        setThreatTypesData(ttData);
        setAccuracyOverTimeData(aotData);
        setConfusionMatrixData(cmData);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Run automated test
  const runLiveTest = useCallback(async (count = 10) => {
    setTestRunning(true);
    setLiveThreats([]);
    setResponseActions([]);
    setTestResults([]);

    try {
      const result = await runAutomatedTest(count, true);

      if (result.success) {
        setCurrentTestSession(result.session_id);

        // Fetch full session details
        const sessionData = await getTestSession(result.session_id);
        if (sessionData.success && sessionData.session) {
          const session = sessionData.session;
          setTestResults(session.results || []);
          setLiveThreats(session.threats_detected || []);
          setResponseActions(session.actions_taken || []);
          setTestLogs(session.logs || []);

          // Update dashboard stats with new data
          if (session.summary) {
            setStats((prev) => ({
              ...prev,
              phishingDetected:
                prev.phishingDetected + (session.threats_detected?.length || 0),
              accuracy: session.summary.accuracy
                ? Math.round(session.summary.accuracy * 100)
                : prev.accuracy,
            }));
          }

          // Add detected threats to main threats list
          if (session.threats_detected?.length > 0) {
            const newThreats = session.threats_detected.map((t) => ({
              id: t.id,
              type: "Phishing",
              severity: t.severity,
              status: "Resolved",
              sender: t.sender,
              subject: t.subject,
              timestamp: t.detected_at,
            }));
            setThreats((prev) => [...newThreats, ...prev].slice(0, 20));
          }
        }

        // Fetch updated reports
        const reportsData = await getTestReports(5);
        setTestReports(reportsData.reports || []);
      }

      return result;
    } catch (error) {
      console.error("Test run failed:", error);
      throw error;
    } finally {
      setTestRunning(false);
    }
  }, []);

  // Refresh test logs
  const refreshTestLogs = useCallback(async () => {
    try {
      const logsData = await getTestLogs(null, null, 50);
      setTestLogs(logsData.logs || []);
    } catch (error) {
      console.error("Failed to refresh test logs:", error);
    }
  }, []);

  const value = {
    stats,
    threats,
    allEmails,
    selectedIncident,
    setSelectedIncident,
    logs,
    loading,
    threatsOverTimeData,
    threatTypesData,
    accuracyOverTimeData,
    confusionMatrixData,
    // Testing values
    testRunning,
    currentTestSession,
    testResults,
    testLogs,
    liveThreats,
    responseActions,
    testReports,
    runLiveTest,
    refreshTestLogs,
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
};
