import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import { fetchBins } from "../hooks/useBins.js";

const STATUS_COLOR = {
  green: "#2ecc71",
  yellow: "#f1c40f",
  red: "#e74c3c",
};

function getStatus(fillPercent) {
  if (fillPercent > 80) return "red";
  if (fillPercent > 50) return "yellow";
  return "green";
}

export default function DashboardMap() {
  const [bins, setBins] = useState([]);

  useEffect(() => {
    fetchBins().then(setBins);
  }, []);

  return (
    <MapContainer center={[51.169, 71.449]} zoom={12} style={{ height: "80vh", width: "100%" }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {bins.map((bin) => (
        <CircleMarker
          key={bin.id}
          center={[bin.lat, bin.lng]}
          radius={10}
          pathOptions={{ color: STATUS_COLOR[getStatus(bin.fill_percent)] }}
        >
          <Popup>
            <strong>{bin.address}</strong>
            <br />
            Заполнение: {bin.fill_percent}%
            <br />
            Заряд батареи: {bin.battery_level}%
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
