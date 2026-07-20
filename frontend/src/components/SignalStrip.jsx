export default function SignalStrip({ bins }) {
  const red = bins.filter((b) => b.fill_percent > 80).length;
  const yellow = bins.filter((b) => b.fill_percent > 50 && b.fill_percent <= 80).length;
  const green = bins.filter((b) => b.fill_percent <= 50).length;

  return (
    <div className="signal-strip">
      <div className="signal-cell signal-cell--red">
        <span className="signal-cell__label">
          <span className="status-dot status-dot--offline" style={{ boxShadow: "none" }} />
          Требуют вывоза
        </span>
        <span className="signal-cell__value">{String(red).padStart(2, "0")}</span>
      </div>
      <div className="signal-cell signal-cell--yellow">
        <span className="signal-cell__label">Ожидание</span>
        <span className="signal-cell__value">{String(yellow).padStart(2, "0")}</span>
      </div>
      <div className="signal-cell signal-cell--green">
        <span className="signal-cell__label">В норме</span>
        <span className="signal-cell__value">{String(green).padStart(2, "0")}</span>
      </div>
    </div>
  );
}
