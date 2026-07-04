import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const predictChurn = async (payload) => {
  const { data } = await api.post("/predict", payload);
  return data;
};

export const getMetadata = async () => {
  const { data } = await api.get("/metadata");
  return data;
};

export const getSamplePayload = async () => {
  const { data } = await api.get("/sample-payload");
  return data;
};

export default api;
