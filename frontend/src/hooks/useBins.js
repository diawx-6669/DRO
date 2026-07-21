import axios from "axios";

const API_BASE =
  import.meta.env.VITE_API_URL || "https://dro-production.up.railway.app/api";

export async function fetchBins() {
  const { data } = await axios.get(`${API_BASE}/bins/`);
  return data;
}

export async function fetchBinDetails(binId) {
  const { data } = await axios.get(`${API_BASE}/bins/${binId}`);
  return data;
}

export async function seedBins() {
  const { data } = await axios.post(`${API_BASE}/bins/seed`);
  return data;
}

export async function generateRoute() {
  const { data } = await axios.post(`${API_BASE}/routes/generate`);
  return data;
}

export async function sendTelemetry(binId, fillPercent, batteryLevel) {
  const { data } = await axios.post(`${API_BASE}/bins/telemetry`, {
    bin_id: binId,
    fill_percent: fillPercent,
    battery_level: batteryLevel,
  });
  return data;
}
