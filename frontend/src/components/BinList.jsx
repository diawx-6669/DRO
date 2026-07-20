import { binStatus } from "../utils/binStatus.js";

export default function BinList({ bins, selectedId, onSelect }) {
  if (bins.length === 0) return null;

  const sorted = [...bins].sort((a, b) => b.fill_percent - a.fill_percent);

  return (
    <ul className="bin-list">
      {sorted.map((bin) => {
        const status = binStatus(bin.fill_percent);
        return (
          <li key={bin.id}>
            <button
              type="button"
              className={`bin-row bin-row--${status} ${
                selectedId === bin.id ? "bin-row--selected" : ""
              }`}
              onClick={() => onSelect(bin.id)}
            >
              <span className={`bin-row__dot bin-row__dot--${status}`} />
              <span className="bin-row__address">{bin.address}</span>
              <span className="bin-row__percent">{Math.round(bin.fill_percent)}%</span>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
