import { useCallback, useEffect, useState } from "react";

import Header from "./components/Header.jsx";
import SignalStrip from "./components/SignalStrip.jsx";
import BinList from "./components/BinList.jsx";
import RoutePanel from "./components/RoutePanel.jsx";
import DashboardMap from "./components/DashboardMap.jsx";
import { fetchBins, seedBins } from "./hooks/useBins.js";

const POLL_INTERVAL_MS = 30000;

function App() {
  const [bins, setBins] = useState([]);
  const [route, setRoute] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState("pending");
  const [seeding, setSeeding] = useState(false);

  const loadBins = useCallback(async () => {
    try {
      const data = await fetchBins();
      setBins(data);
      setConnectionStatus("online");
    } catch (err) {
      setConnectionStatus("offline");
    }
  }, []);

  useEffect(() => {
    loadBins();
    const id = setInterval(loadBins, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [loadBins]);

  async function handleSeed() {
    setSeeding(true);
    try {
      await seedBins();
      await loadBins();
    } catch (err) {
      setConnectionStatus("offline");
    } finally {
      setSeeding(false);
    }
  }

  return (
    <div className="app">
      <Header connectionStatus={connectionStatus} />
      <SignalStrip bins={bins} />
      <div className="app__body">
        <div className="app__map">
          <DashboardMap
            bins={bins}
            route={route}
            selectedId={selectedId}
            onSelect={setSelectedId}
            onSeed={handleSeed}
            seeding={seeding}
          />
        </div>
        <aside className="app__sidebar">
          <RoutePanel onRouteGenerated={setRoute} />
          <div className="panel-section panel-section--scroll">
            <h2 className="panel-section__title">
              Контейнеры
              <span className="panel-section__count">{bins.length}</span>
            </h2>
            {bins.length > 0 ? (
              <BinList bins={bins} selectedId={selectedId} onSelect={setSelectedId} />
            ) : (
              <p style={{ fontSize: 12.5, color: "var(--text-faint)" }}>
                {connectionStatus === "offline"
                  ? "Не удаётся получить данные с сервера."
                  : "Ожидаем данные с датчиков…"}
              </p>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
