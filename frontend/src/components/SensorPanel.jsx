import { useEffect, useRef, useState } from "react";

import { fetchBins, seedBins, sendTelemetry } from "../hooks/useBins.js";

const SEND_INTERVAL_MS = 3000;

function extractNumber(line) {
  const match = line.match(/-?\d+(\.\d+)?/);
  return match ? parseFloat(match[0]) : null;
}

export default function SensorPanel({ onClose, onTelemetrySent }) {
  const [status, setStatus] = useState("idle"); // idle | live | error | unsupported
  const [distance, setDistance] = useState(null);
  const [fillPercent, setFillPercent] = useState(null);
  const [containerHeight, setContainerHeight] = useState(100);
  const [binId, setBinId] = useState(null);
  const [binReady, setBinReady] = useState(false);

  const portRef = useRef(null);
  const readerRef = useRef(null);
  const lastSentRef = useRef(0);

  // При открытии окна убеждаемся, что в базе есть тот самый единственный
  // демо-бак, и запоминаем его id, чтобы слать телеметрию именно туда.
  useEffect(() => {
    (async () => {
      try {
        let bins = await fetchBins();
        if (bins.length === 0) {
          await seedBins();
          bins = await fetchBins();
        }
        if (bins.length > 0) {
          setBinId(bins[0].id);
          setBinReady(true);
        }
      } catch (err) {
        console.error("Не удалось подготовить демо-бак:", err);
      }
    })();
  }, []);

  async function handleConnect() {
    if (!("serial" in navigator)) {
      setStatus("unsupported");
      return;
    }

    try {
      const port = await navigator.serial.requestPort();
      await port.open({ baudRate: 9600 });
      portRef.current = port;
      setStatus("live");

      const textDecoder = new TextDecoderStream();
      port.readable.pipeTo(textDecoder.writable);
      const reader = textDecoder.readable.getReader();
      readerRef.current = reader;

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          reader.releaseLock();
          break;
        }
        if (!value) continue;

        buffer += value;
        const lines = buffer.split("\n");
        buffer = lines.pop();

        for (const rawLine of lines) {
          const num = extractNumber(rawLine.trim());
          if (num === null) continue;

          setDistance(num.toFixed(1));
          const percent = Math.max(0, Math.min(100, (1 - num / containerHeight) * 100));
          setFillPercent(percent);

          const now = Date.now();
          if (binId && now - lastSentRef.current > SEND_INTERVAL_MS) {
            lastSentRef.current = now;
            sendTelemetry(binId, percent, 100)
              .then(() => onTelemetrySent?.())
              .catch((err) => console.error("Не удалось отправить телеметрию:", err));
          }
        }
      }

      setStatus((s) => (s === "live" ? "error" : s));
    } catch (err) {
      console.error(err);
      setStatus("error");
    }
  }

  async function handleClose() {
    try {
      await readerRef.current?.cancel();
      await portRef.current?.close();
    } catch (err) {
      // порт мог уже закрыться сам — это нормально
    }
    onClose();
  }

  const statusMeta = {
    idle: { dot: "", text: "Не подключено" },
    live: { dot: "status-dot--online", text: "Приём данных" },
    error: { dot: "status-dot--offline", text: "Соединение прервано" },
    unsupported: { dot: "status-dot--offline", text: "Браузер не поддерживает Web Serial" },
  }[status];

  return (
    <div className="sensor-modal-backdrop" onClick={handleClose}>
      <div className="sensor-modal" onClick={(e) => e.stopPropagation()}>
        <div className="sensor-modal__header">
          <span className="sensor-modal__eyebrow">DRO · Проверка датчика</span>
          <button className="sensor-modal__close" onClick={handleClose} aria-label="Закрыть">
            ✕
          </button>
        </div>

        <h2 className="sensor-modal__title">Датчик заполнения контейнера</h2>

        <div className="status-line" style={{ justifyContent: "flex-start", marginBottom: 14 }}>
          <span className={`status-dot ${statusMeta.dot}`} />
          <span>{statusMeta.text}</span>
        </div>

        <label className="sensor-modal__field">
          Высота контейнера (см)
          <input
            type="number"
            min="1"
            value={containerHeight}
            onChange={(e) => setContainerHeight(Number(e.target.value) || 1)}
            disabled={status === "live"}
          />
        </label>

        <div className="reading">
          <div className="reading__value">
            {fillPercent !== null ? `${Math.round(fillPercent)}%` : "---"}
          </div>
          <div className="reading__unit">
            {distance !== null ? `${distance} см до поверхности` : "заполнение контейнера"}
          </div>
        </div>

        {status !== "unsupported" ? (
          <button
            className="route-btn"
            onClick={handleConnect}
            disabled={status === "live" || !binReady}
          >
            {status === "live"
              ? "Подключено"
              : binReady
              ? "Подключить Arduino"
              : "Готовим демо-бак…"}
          </button>
        ) : (
          <p className="route-error">
            Откройте сайт в Chrome или Edge — Safari и Firefox Web Serial API не поддерживают.
          </p>
        )}

        <p className="sensor-modal__hint">
          Данные отправляются на карту диспетчерской каждые {SEND_INTERVAL_MS / 1000} сек.
          Плата должна отправлять в Serial одно число на строку
          (<code>Serial.println(distanceCm)</code>).
        </p>
      </div>
    </div>
  );
}
