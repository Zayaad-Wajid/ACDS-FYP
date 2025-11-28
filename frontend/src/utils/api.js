import axios from "axios";
import phishingData from "../mocks/phishingData.json";
import emailDetails from "../mocks/emailDetails.json";

// Create an axios instance
// Use environment variable for API URL, fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

// Helper to determine if we should use mock data
// In a real scenario, you might toggle this with an env var like VITE_USE_MOCK
const USE_MOCK = true;

// Mock API functions
export const fetchStats = async () => {
  if (!USE_MOCK) {
    const response = await api.get("/stats");
    return response.data;
  }
  // Simulate network delay
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.stats), 500);
  });
};

export const fetchThreatsOverTime = async () => {
  if (!USE_MOCK) {
    const response = await api.get("/threats/history");
    return response.data;
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.detectionsOverTime), 500);
  });
};

export const fetchThreatTypes = async () => {
  if (!USE_MOCK) {
    const response = await api.get("/threats/types");
    return response.data;
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.threatTypes), 500);
  });
};

export const fetchAccuracyOverTime = async () => {
  if (!USE_MOCK) {
    // const response = await api.get("/model/accuracy");
    // return response.data;
    return [];
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.accuracyOverTime), 500);
  });
};

export const fetchConfusionMatrix = async () => {
  if (!USE_MOCK) {
    // const response = await api.get("/model/confusion-matrix");
    // return response.data;
    return { tp: 0, fp: 0, fn: 0, tn: 0 };
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.confusionMatrix), 500);
  });
};

export const fetchThreats = async () => {
  if (!USE_MOCK) {
    const response = await api.get("/threats/recent");
    return response.data;
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.recentEmails), 500);
  });
};

export const fetchIncidentDetails = async (id) => {
  if (!USE_MOCK) {
    const response = await api.get(`/incidents/${id}`);
    return response.data;
  }
  return new Promise((resolve) => {
    const detail = emailDetails.find((d) => d.id === id) || emailDetails[0];
    setTimeout(() => resolve(detail), 500);
  });
};

export const fetchModelLogs = async () => {
  if (!USE_MOCK) {
    // const response = await api.get("/model/logs");
    // return response.data;
    return [];
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.modelLogs), 500);
  });
};

export const fetchAllEmails = async () => {
  // For the Phishing Module list
  return new Promise((resolve) => {
    setTimeout(() => resolve(emailDetails), 500);
  });
};

export const fetchFeedbackSummary = async () => {
  if (!USE_MOCK) {
    // const response = await api.get("/model/feedback-summary");
    // return response.data;
    return { truePositive: 0, falsePositive: 0 };
  }
  return new Promise((resolve) => {
    setTimeout(() => resolve(phishingData.feedbackSummary), 300);
  });
};

export default api;
