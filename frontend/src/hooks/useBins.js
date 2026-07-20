import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function fetchBins() {
  const { data } = await axios.get(`${API_BASE}/bins/`);
  return data;
}

export async function fetchBinDetails(binId) {
  const { data } = await axios.get(`${API_BASE}/bins/${binId}`);
  return data;
}
