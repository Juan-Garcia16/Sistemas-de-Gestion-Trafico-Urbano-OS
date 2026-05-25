import { useState, useEffect } from "react";
import { LoginForm } from "./components/LoginForm";
import { IntersectionGrid } from "./components/IntersectionGrid";
import { ControlPanel } from "./components/ControlPanel";
import { MetricsPanel } from "./components/MetricsPanel";
import { AlertBanner } from "./components/AlertBanner";
import { useWebSocket } from "./hooks/useWebSocket";
import { api } from "./services/api";

function App() {
  const [userRole, setUserRole] = useState(null);
  const [simulationRunning, setSimulationRunning] = useState(false);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("user_role");
    if (savedToken && savedRole) {
      api.setToken(savedToken);
      setUserRole(savedRole);
    }
  }, []);

  useEffect(() => {
    if (userRole) {
      api.getStatus()
        .then(status => setSimulationRunning(status.running))
        .catch(() => {});
    }
  }, [userRole]);

  const wsState = useWebSocket();

  const handleLogin = (role) => {
    setUserRole(role);
  };

  const handleLogout = () => {
    api.setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user_role");
    setUserRole(null);
    setSimulationRunning(false);
  };

  if (!userRole) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900 text-white overflow-hidden">
      <AlertBanner alerts={wsState.alerts} />

      <nav className="bg-gray-900 border-b border-gray-700/60 px-4 py-2.5 flex items-center justify-between shrink-0 shadow-sm">
        <div className="flex items-center gap-3">
          <h1 className="text-sm font-bold tracking-tight text-white">Traffic Control System</h1>
          <span className="text-[10px] font-mono text-gray-500 border-l border-gray-700 pl-3">Sistema de Gestión de Tráfico Urbano</span>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="text-gray-400">
            Vehículos: <span className="text-white font-bold">{wsState.vehicles.length}</span>
          </span>
          <span className="text-gray-400">
            Intersecciones: <span className="text-white font-bold">{wsState.intersections.length}</span>
          </span>
          <span className="text-gray-400">
            Alertas: <span className={wsState.alerts.length > 0 ? "text-yellow-400 font-bold" : "text-white font-bold"}>{wsState.alerts.length}</span>
          </span>
          <span className={`flex items-center gap-1.5 px-2 py-0.5 rounded border text-[10px] font-bold ${
            wsState.connected
              ? "bg-green-950 text-green-400 border-green-900/60"
              : "bg-red-950 text-red-400 border-red-900/60"
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${wsState.connected ? "bg-green-500 animate-pulse" : "bg-red-500"}`} />
            {wsState.connected ? "WS Conectado" : "WS Desconectado"}
          </span>
          <span className="text-gray-500 text-[10px] font-mono border-l border-gray-700 pl-3">
            Rol: <span className="text-gray-300">{userRole}</span>
          </span>
          <button
            onClick={handleLogout}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded text-[10px] font-mono font-bold cursor-pointer transition border border-gray-600 hover:border-gray-500"
          >
            Cerrar sesión
          </button>
        </div>
      </nav>

      <div className="flex-1 flex overflow-hidden p-4 gap-4">
        <div className="flex-1 flex items-center justify-center min-w-0">
          <IntersectionGrid
            intersections={wsState.intersections}
            vehicles={wsState.vehicles}
          />
        </div>
        <div className="flex flex-col gap-3 w-80 shrink-0 overflow-y-auto overflow-x-hidden">
          <MetricsPanel
            intersections={wsState.intersections}
            vehicles={wsState.vehicles}
          />
          {userRole === "control" && (
            <ControlPanel
              intersections={wsState.intersections}
              simulationRunning={simulationRunning}
              onSimulationChange={setSimulationRunning}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
