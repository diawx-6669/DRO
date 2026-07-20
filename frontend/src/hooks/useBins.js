import axios from "axios";

const API_BASE = "https://dro-production.up.railway.app/api";

export async function fetchBins() {
  const { data } = await axios.get(`${API_BASE}/bins/`);
  return data;
}

export async function fetchBinDetails(binId) {
  const { data } = await axios.get(`${API_BASE}/bins/${binId}`);
  return data;
}
