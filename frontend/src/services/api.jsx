import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",//If Member 5's Flask backend runs on another port, change:
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;