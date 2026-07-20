import { useState } from "react";

import { generateRoute } from "../hooks/useBins.js";

export default function RoutePanel({ onRouteGenerated }) {
  const [loading, setLoading] = useState(false);
  const [route, setRoute] = useState(null);
  const [error, setError] = useState(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    try {
      const data = await generateRoute();
      setRoute(data);
      onRouteGenerated(data);
    } catch (err) {
      setError("Не удалось построить маршрут. Проверьте связь с сервером.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel-section">
      <h2 className="panel-section__title">Маршрут на смену</h2>
      <button className="route-btn" onClick={handleGenerate} disabled={loading}>
        {loading ? "Строим маршрут…" : "Построить маршрут"}
      </button>

      {error && <div className="route-error">{error}</div>}

      {route && !error && route.points?.length > 0 && (
        <div className="route-summary">
          <div className="route-summary__distance">{route.total_distance_km} км</div>
          <div className="route-summary__label">
            {route.bins_count} контейнер{route.bins_count === 1 ? "" : route.bins_count < 5 ? "а" : "ов"} на пути,
            заполнены ≥80%
          </div>
          <ul className="route-stops">
            {route.points.map((point, i) => (
              <li
                key={i}
                className={`route-stop ${
                  point.bin_id === null
                    ? i === 0
                      ? "route-stop--depot"
                      : "route-stop--unload"
                    : ""
                }`}
              >
                <span className="route-stop__dot" />
                <span className="route-stop__text">{point.label}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {route && !error && route.points?.length === 0 && (
        <div className="route-summary">
          <div className="route-summary__label">{route.message || "Нет контейнеров, заполненных выше порога"}</div>
        </div>
      )}
    </div>
  );
}
