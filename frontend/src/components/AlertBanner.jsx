import { useState } from "react";

export function AlertBanner({ alerts }) {
  const [dismissed, setDismissed] = useState([]);

  const visibleAlerts = alerts.filter(a => !dismissed.includes(a.timestamp));

  if (visibleAlerts.length === 0) return null;

  return (
    <div className="fixed top-0 left-0 right-0 z-50 p-4 space-y-2">
      {visibleAlerts.map((alert) => (
        <div
          key={alert.timestamp}
          className={`p-4 rounded-lg shadow-lg flex items-center justify-between animate-slide-down ${
            alert.type === "FAULT"
              ? "bg-red-600 text-white"
              : "bg-yellow-500 text-black"
          }`}
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">{alert.type === "FAULT" ? "⚠️" : "🚨"}</span>
            <div>
              <p className="font-bold">
                {alert.type === "FAULT"
                  ? `Fallo en intersección ${alert.intersection}`
                  : `Vehículo de emergencia: ${alert.vehicle}`}
              </p>
              <p className="text-sm opacity-80">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
          <button
            onClick={() => setDismissed([...dismissed, alert.timestamp])}
            className="p-2 hover:bg-black/20 rounded"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}