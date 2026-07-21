import { useRef, useState } from "react";

function extractNumber(line) {
  const match = line.match(/-?\d+(\.\d+)?/);
  return match ? parseFloat(match[0]) : null;
}

export default function SensorPanel({ onClose }) {
  const [status, setStatus] = useState("idle"); // idle | live | error | unsupported
  const [distance, setDistance] = useState(null);
  const portRef = useRef(null);
  const readerRef = useRef(null);

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
          if (num !== null) setDistance(num.toFixed(1));
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

        <div className="status-line" style={{ justifyContent: "flex-start", marginBottom: 18 }}>
          <span className={`status-dot ${statusMeta.dot}`} />
          <span>{statusMeta.text}</span>
        </div>

        <div className="reading">
          <div className="reading__value">{distance ?? "---"}</div>
          <div className="reading__unit">см до поверхности</div>
        </div>

        {status !== "unsupported" ? (
          <button className="route-btn" onClick={handleConnect} disabled={status === "live"}>
            {status === "live" ? "Подключено" : "Подключить Arduino"}
          </button>
        ) : (
          <p className="route-error">
            Откройте сайт в Chrome или Edge — Safari и Firefox Web Serial API не поддерживают.
          </p>
        )}

        <p className="sensor-modal__hint">
          Нужен физический датчик, подключённый к этому компьютеру по USB. Плата должна
          отправлять в Serial одно число на строку (<code>Serial.println(distanceCm)</code>).
        </p>
      </div>
    </div>
  );
}
