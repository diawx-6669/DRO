export function binStatus(fillPercent) {
  if (fillPercent > 80) return "red";
  if (fillPercent > 50) return "yellow";
  return "green";
}

export const STATUS_LABEL = {
  red: "Требует вывоза",
  yellow: "Ожидание",
  green: "В норме",
};

export const STATUS_COLOR = {
  red: "#e2543d",
  yellow: "#e8b23d",
  green: "#4caf6d",
};
