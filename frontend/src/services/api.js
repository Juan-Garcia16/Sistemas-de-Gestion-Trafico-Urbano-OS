const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiService {
  constructor() {
    this.token = localStorage.getItem("token");
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }

  async request(method, path, body = null, requiresAuth = true) {
    const headers = { "Content-Type": "application/json" };
    if (requiresAuth && this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const options = { method, headers };
    if (body && method !== "GET") {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${path}`, options);

    if (response.status === 401) {
      this.setToken(null);
      throw new Error("Unauthorized");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth
  async login(username, password) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      body: formData
    });

    if (response.status === 401) {
      this.setToken(null);
      throw new Error("Unauthorized");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Login failed" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async register(username, password, role) {
    return this.request("POST", "/auth/register", { username, password, role }, false);
  }

  // Simulation
  async startSimulation() {
    return this.request("POST", "/simulation/start");
  }

  async stopSimulation() {
    return this.request("POST", "/simulation/stop");
  }

  async getStatus() {
    return this.request("GET", "/simulation/status");
  }

  async addVehicle(id, route, priority) {
    return this.request("POST", "/simulation/vehicle", { id, route, priority });
  }

  // Control
  async updateLightTiming(intersectionId, greenTime, redTime) {
    return this.request("PUT", `/control/lights/${intersectionId}/timing`, { green_time: greenTime, red_time: redTime });
  }

  async triggerFault(intersectionId) {
    return this.request("POST", `/control/lights/${intersectionId}/fault`);
  }

  async getLogs(eventType, limit) {
    const params = new URLSearchParams();
    if (eventType) params.append("event_type", eventType);
    if (limit) params.append("limit", limit);
    return this.request("GET", `/logs?${params.toString()}`);
  }
}

export const api = new ApiService();