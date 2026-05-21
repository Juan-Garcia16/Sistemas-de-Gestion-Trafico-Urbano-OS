import { useEffect, useState, useRef, useCallback } from "react";

const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

export function useWebSocket() {
  const [state, setState] = useState({
    intersections: [],
    vehicles: [],
    alerts: [],
    connected: false,
    error: null
  });

  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        setState(prev => ({ ...prev, connected: true, error: null }));
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "STATE_UPDATE") {
            setState(prev => ({
              ...prev,
              intersections: data.intersections || [],
              vehicles: data.vehicles || [],
              alerts: data.alerts || []
            }));
          } else if (data.type === "FAULT") {
            setState(prev => ({
              ...prev,
              alerts: [...prev.alerts, { type: "FAULT", intersection: data.intersection_id, timestamp: data.timestamp }]
            }));
          } else if (data.type === "EMERGENCY") {
            setState(prev => ({
              ...prev,
              alerts: [...prev.alerts, { type: "EMERGENCY", vehicle: data.vehicle_id, timestamp: data.timestamp }]
            }));
          }
        } catch (e) {
          console.error("Error parsing WS message:", e);
        }
      };

      ws.onclose = () => {
        setState(prev => ({ ...prev, connected: false }));
        // Auto-reconnect after 2 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 2000);
      };

      ws.onerror = () => {
        setState(prev => ({ ...prev, error: "WebSocket error" }));
      };

      wsRef.current = ws;
    } catch (e) {
      setState(prev => ({ ...prev, error: e.message }));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  return state;
}