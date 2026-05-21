import { useState, useEffect } from "react";
import { LoginForm } from "./components/LoginForm";
import { AlertBanner } from "./components/AlertBanner";
import { useWebSocket } from "./hooks/useWebSocket";
import { api } from "./services/api";

function App() {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("user_role");
    return token && role ? role : null;
  });
  const [simulationRunning, setSimulationRunning] = useState(false);
  const wsState = useWebSocket();

  useEffect(() => {
    const syncSimulationState = async () => {
      try {
        const status = await api.getStatus();
        setSimulationRunning(status.running);
      } catch (err) {
        console.error("Error syncing simulation state:", err);
      }
    };
    if (user) {
      syncSimulationState();
    }
  }, [user]);

  const handleLogin = (role) => {
    setUser(role);
  };

  const handleLogout = () => {
    api.setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user_role");
    setUser(null);
    setSimulationRunning(false);
  };

  const handleStartSimulation = async () => {
    try {
      await api.startSimulation();
      setSimulationRunning(true);
    } catch (err) {
      console.error("Error starting simulation:", err);
    }
  };

  const handleStopSimulation = async () => {
    try {
      await api.stopSimulation();
      setSimulationRunning(false);
    } catch (err) {
      console.error("Error stopping simulation:", err);
    }
  };

  if (!user) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <AlertBanner alerts={wsState.alerts} />

      <header className="bg-gray-800 p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold">Traffic Control System</h1>
          <span className={`text-sm ${wsState.connected ? "text-green-400" : "text-red-400"}`}>
            {wsState.connected ? "● Conectado" : "● Desconectado"}
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-gray-400">Rol: {user}</span>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-sm"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>

      <main className="p-6">
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">Control de Simulación</h2>
          <div className="flex gap-4">
            {!simulationRunning ? (
              <button
                onClick={handleStartSimulation}
                disabled={!wsState.connected}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded disabled:opacity-50"
              >
                Iniciar Simulación
              </button>
            ) : (
              <button
                onClick={handleStopSimulation}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
              >
                Detener Simulación
              </button>
            )}
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">Intersections</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {wsState.intersections.map((intersection) => (
              <div
                key={intersection.id}
                className={`p-4 rounded-lg border-2 ${
                  intersection.state === "GREEN"
                    ? "border-green-500 bg-green-500/20"
                    : intersection.state === "YELLOW"
                    ? "border-yellow-500 bg-yellow-500/20"
                    : intersection.state === "RED"
                    ? "border-red-500 bg-red-500/20"
                    : intersection.state === "FAULT"
                    ? "border-red-700 bg-red-700/50"
                    : "border-gray-600 bg-gray-700/20"
                }`}
              >
                <div className="text-center">
                  <span className="text-3xl mb-2 block">
                    {intersection.state === "GREEN"
                      ? "🟢"
                      : intersection.state === "YELLOW"
                      ? "🟡"
                      : intersection.state === "RED"
                      ? "🔴"
                      : intersection.state === "FAULT"
                      ? "⚠️"
                      : "⚪"}
                  </span>
                  <p className="font-mono text-sm">{intersection.id}</p>
                  <p className="text-xs text-gray-400">
                    Vehículos: {intersection.vehicle_count || 0}
                  </p>
                </div>
              </div>
            ))}
          </div>
          {wsState.intersections.length === 0 && (
            <p className="text-gray-400 text-center py-8">
              {simulationRunning
                ? "Cargando intersecciones..."
                : "Inicia la simulación para ver las intersecciones"}
            </p>
          )}
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Vehículos</h2>
          <div className="space-y-2">
            {wsState.vehicles.map((vehicle) => (
              <div
                key={vehicle.id}
                className={`p-3 rounded flex items-center justify-between ${
                  vehicle.status === "MOVING"
                    ? "bg-green-500/20"
                    : vehicle.status === "WAITING"
                    ? "bg-yellow-500/20"
                    : vehicle.status === "BLOCKED"
                    ? "bg-red-500/20"
                    : "bg-gray-700/20"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">
                    {vehicle.priority === "EMERGENCY"
                      ? "🚨"
                      : vehicle.priority === "HIGH"
                      ? "⚡"
                      : "🚗"}
                  </span>
                  <div>
                    <p className="font-mono text-sm">{vehicle.id}</p>
                    <p className="text-xs text-gray-400">
                      Ruta: {vehicle.route?.join(" → ") || "N/A"}
                    </p>
                  </div>
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs ${
                    vehicle.status === "MOVING"
                      ? "bg-green-600"
                      : vehicle.status === "WAITING"
                      ? "bg-yellow-600"
                      : vehicle.status === "BLOCKED"
                      ? "bg-red-600"
                      : "bg-gray-600"
                  }`}
                >
                  {vehicle.status}
                </span>
              </div>
            ))}
          </div>
          {wsState.vehicles.length === 0 && (
            <p className="text-gray-400 text-center py-4">
              {simulationRunning
                ? "Cargando vehículos..."
                : "Inicia la simulación para ver los vehículos"}
            </p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;