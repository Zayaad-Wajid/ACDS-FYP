import React, { createContext, useContext, useState, useEffect } from "react";
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
  fetchFeedbackSummary,
} from "../utils/api";

const DashboardContext = createContext();

export const useDashboard = () => useContext(DashboardContext);

export const DashboardProvider = ({ children }) => {
  const [stats, setStats] = useState({
    totalThreats: 0,
    activeThreats: 0,
    autoResolved: 0,
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
  const [feedbackSummary, setFeedbackSummary] = useState({
    truePositive: 0,
    falsePositive: 0,
  });
  const [loading, setLoading] = useState(true);

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
          feedbackData,
        ] = await Promise.all([
          fetchStats(),
          fetchThreats(),
          fetchAllEmails(),
          fetchModelLogs(),
          fetchThreatsOverTime(),
          fetchThreatTypes(),
          fetchAccuracyOverTime(),
          fetchConfusionMatrix(),
          fetchFeedbackSummary(),
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
        setFeedbackSummary(feedbackData);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
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
    feedbackSummary,
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
};
