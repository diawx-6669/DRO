import { useEffect, useState } from "react";

export default function Header({ connectionStatus }) {
  const [time, setTime] = useState(() => new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const timeString = time.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const statusMeta = {
    online: { dot: "status-dot--online", text: "Связь с сервером — активна" },
    offline: { dot: "status-dot--offline", text: "Нет связи с сервером" },
    pending: { dot: "status-dot--pending", text: "Подключение…" },
  }[connectionStatus];

  return (
    <header className="header">
      <div className="header__brand">
        <span className="header__mark">DRO</span>
        <span className="header__subtitle">Диспетчерская · Астана</span>
      </div>
      <div className="header__status">
        <span className={`status-dot ${statusMeta.dot}`} />
        <span>{statusMeta.text}</span>
        <span style={{ color: "var(--text-faint)", marginLeft: 4 }}>{timeString}</span>
      </div>
    </header>
  );
}
