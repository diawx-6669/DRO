import { MapContainer, TileLayer, CircleMarker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import { binStatus, STATUS_COLOR } from "../utils/binStatus.js";

const ASTANA_CENTER = [51.169, 71.449];

export default function DashboardMap({ bins, route, selectedId, onSelect, onSeed, seeding }) {
  const routeLine = route?.points?.map((p) => [p.lat, p.lng]) ?? null;

  return (
    <>
      <MapContainer center={ASTANA_CENTER} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {routeLine && routeLine.length > 1 && (
          <Polyline
            positions={routeLine}
            pathOptions={{ color: "#e8a33d", weight: 3, opacity: 0.85, dashArray: "1 8" }}
          />
        )}

        {bins.map((bin) => {
          const status = binStatus(bin.fill_percent);
          const isSelected = selectedId === bin.id;
          return (
            <CircleMarker
              key={bin.id}
              center={[bin.lat, bin.lng]}
              radius={isSelected ? 12 : 9}
              pathOptions={{
                color: STATUS_COLOR[status],
                fillColor: STATUS_COLOR[status],
                fillOpacity: isSelected ? 0.9 : 0.65,
                weight: isSelected ? 3 : 1.5,
                className: status === "red" ? "bin-marker bin-marker--red" : "bin-marker",
              }}
              eventHandlers={{ click: () => onSelect(bin.id) }}
            >
              <Popup>
                <div className="bin-popup__title">{bin.address}</div>
                <div className="bin-popup__row">
                  <span>Заполнение</span>
                  <span>{Math.round(bin.fill_percent)}%</span>
                </div>
                <div className="bin-popup__row">
                  <span>Батарея датчика</span>
                  <span>{Math.round(bin.battery_level)}%</span>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      <div className="map-legend">
        <span className="map-legend__item">
          <span className="status-dot" style={{ background: "var(--green)" }} /> 0–50%
        </span>
        <span className="map-legend__item">
          <span className="status-dot" style={{ background: "var(--yellow)" }} /> 51–80%
        </span>
        <span className="map-legend__item">
          <span className="status-dot" style={{ background: "var(--red)" }} /> &gt;80%
        </span>
      </div>

      {bins.length === 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 500,
            pointerEvents: "none",
          }}
        >
          <div
            className="empty-state"
            style={{
              pointerEvents: "auto",
              background: "rgba(26,31,38,0.92)",
              border: "1px solid var(--border)",
              borderRadius: "var(--radius-lg)",
              backdropFilter: "blur(6px)",
              maxWidth: 320,
            }}
          >
            <p className="empty-state__title">Нет данных с датчиков</p>
            <p className="empty-state__text">
              Контейнеры ещё не зарегистрированы в системе. Загрузите тестовый набор, чтобы
              увидеть карту в работе.
            </p>
            <button className="empty-state__btn" onClick={onSeed} disabled={seeding}>
              {seeding ? "Загружаем…" : "Загрузить тестовые баки"}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
