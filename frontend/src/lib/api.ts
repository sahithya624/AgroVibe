import axios from "axios";

// Force 127.0.0.1 to debug Network Error (ignoring .env for now)
const API_URL = "http://127.0.0.1:8000/api";
// const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor for auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('smartfarm_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const diseaseApi = {
  predict: async (image: File, cropType?: string) => {
    const formData = new FormData();
    formData.append("image", image);
    if (cropType) {
      formData.append("crop_type", cropType);
    }
    const response = await api.post(`/disease-detect`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },
  getBaseUrl: () => API_URL,
  getInfo: async (name: string) => {
    const response = await api.get(`/disease-info/${name}`);
    return response.data;
  },
};

export const soilApi = {
  getAdvice: async (data: any) => {
    const response = await api.post("/soil-advice", data);
    return response.data;
  },
  getHealthScore: async (data: any) => {
    const response = await api.post("/soil-health-score", data);
    return response.data;
  },
};


export const yieldApi = {
  predict: async (data: any) => {
    const response = await api.post("/yield-predict", data);
    return response.data;
  },
  getHistory: async (crop: string) => {
    const response = await api.get(`/yield-history/${crop}`);
    return response.data;
  },
};

export const marketApi = {
  getInsights: async (data: any) => {
    const response = await api.post("/market-insights", data);
    return response.data;
  },
  getTrends: async (crop: string) => {
    const response = await api.get(`/market-trends/${crop}`);
    return response.data;
  },
};

export default api;
