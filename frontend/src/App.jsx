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

      <nav className="bg-gray-800 px-4 py-3 flex items-center justify-between shrink-0">
        <h1 className="text-lg font-bold">🚦 Traffic Control System</h1>
        <div className="flex items-center gap-5 text-sm">
          <span className="text-gray-300">🚗 {wsState.vehicles.length}</span>
          <span className="text-gray-300">🚦 {wsState.intersections.length}</span>
          <span className="text-gray-300">⚠️ {wsState.alerts.length}</span>
          <span className={wsState.connected ? "text-green-400" : "text-red-400"}>
            {wsState.connected ? "🟢" : "🔴"}
          </span>
          <span className="text-gray-400">
            {userRole}
          </span>
          <button
            onClick={handleLogout}
            className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
          >
            ↩
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
        <div className="flex flex-col gap-3 w-80 shrink-0 overflow-y-auto">
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
