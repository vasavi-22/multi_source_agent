import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const runProductAgent = async () => {
  const response = await API.post("/run-agent");
  return response.data;
};

export const runFinanceAgent = async () => {
  const response = await API.post("/run-finance-agent");
  return response.data;
};
