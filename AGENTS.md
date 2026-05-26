# AGENTS.md

## Project Overview

Spanish-language academic Operating Systems project. Models urban traffic with concurrent vehicles, synchronized traffic lights, emergency priority, fault detection, and role-based access.

**Stack:** Python/FastAPI backend (threading + asyncio) | React/Vite frontend (WebSockets) | SQLite

---

## Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev          # Development server
npm run lint         # ESLint (flat config, React hooks)
npm run build        # Vite production build
npm run preview      # Preview production build
```

### Running Single Test
**No test infrastructure configured.** If tests are added:
```bash
# pytest
cd backend && pytest tests/test_specific.py -v
cd backend && pytest tests/test_specific.py::test_name -v

# vitest (frontend)
cd frontend && npx vitest run src/components/test.spec.jsx
```

---

## Code Style Guidelines

### General

- **Backend code uses Spanish comments** explaining SO concepts (academic purpose)
- **Frontend identifiers use English** (camelCase/PascalCase)
- **No type checking tools** (no mypy, pyright, TypeScript) - types are convention-only
- **Preserve low-level SO abstractions** - never replace `threading.Semaphore`, `queue.PriorityQueue`, `threading.Event` with high-level alternatives

---

### Python (Backend)

**Imports Order:**
```python
# Standard library
import threading
import time
from enum import IntEnum
from typing import Callable, Optional

# External dependencies
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Local project imports
from config import VEHICLE_MAX_LIFETIME
from core.scheduler import TrafficScheduler
from simulation.network import IntersectionNetwork
```

**Naming Conventions:**
| Item | Convention | Example |
|------|-----------|---------|
| Modules | snake_case | `traffic_light.py` |
| Classes | PascalCase | `TrafficLight`, `SimulationEngine` |
| Functions/methods | snake_case | `trigger_fault()`, `wait_for_dispatch()` |
| Constants | UPPER_SNAKE | `JWT_SECRET`, `VEHICLE_MAX_LIFETIME` |
| Variables/instance vars | snake_case | `green_time`, `vehicle_id` |
| Private methods | `_prefix` | `_lock`, `_fault_loop()` |
| Enum members | UPPER_SNAKE | `Priority.EMERGENCY` |

**Threading Patterns:**
- Use `daemon=True` for all background threads (Vehicle, FaultHandler, DeadlockDetector)
- Use `threading.Lock()` for shared state, always with `with self._lock:` context manager
- Use `threading.Event` for interruption/fault simulation
- Use `queue.PriorityQueue` for emergency vehicle dispatch

**Error Handling:**
```python
# API errors
raise HTTPException(status_code=404, detail="Intersección no encontrada")

# JWT errors
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except JWTError:
    raise HTTPException(status_code=401, detail="Token inválido o expirado")

# Silent catch for non-critical async callbacks
try:
    await ws.send_text(msg)
except Exception:
    disconnected.append(ws)
```

**Type Hints (sparse, convention-only):**
```python
def dispatch_next(self, intersection_id: str) -> None:
def get_neighbors(self, intersection_id: str) -> list[Intersection]:
_engine: SimulationEngine | None = None
```

---

### JavaScript/React (Frontend)

**Naming Conventions:**
| Item | Convention | Example |
|------|-----------|---------|
| Components | PascalCase (file & export) | `IntersectionGrid.jsx`, `export function IntersectionGrid` |
| Hooks | camelCase with `use` prefix | `useWebSocket`, `useState`, `useEffect` |
| Services | camelCase | `ApiService`, `api.js` |
| Variables/props | camelCase | `userRole`, `simulationRunning` |
| Constants | camelCase | `WS_URL`, `API_BASE`, `CELL_SIZE` |

**Component Structure:**
```javascript
import { useState, useEffect, useRef, useCallback } from "react";
import { TrafficLight } from "./TrafficLight";
import { api } from "../services/api";

export function ComponentName({ prop1, prop2 }) {
  const [state, setState] = useState(initialValue);
  
  useEffect(() => {
    // effect logic
    return () => {}; // cleanup
  }, [dependency]);
  
  return (
    <div className="tailwind-classes">
      <ChildComponent />
    </div>
  );
}
```

**Styling:**
- Use Tailwind CSS v4 utility classes (no separate CSS files except `index.css` for animations)
- CSS classes use kebab-case: `bg-gray-800`, `text-white`, `flex items-center`
- Custom animations defined in `index.css` with keyframes

**Error Handling:**
```javascript
// API errors
try {
  const data = await api.login(username, password);
  onLogin(data.role);
} catch (err) {
  setError(err.message);
}

// WebSocket errors
.catch(() => {}); // silent for non-critical

console.error("Error parsing WS message:", e);
```

---

### Imports

**Python:**
```python
# stdlib
import threading
import time
from enum import IntEnum

# external
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# local
from core.scheduler import TrafficScheduler
from auth.roles import require_role
```

**JavaScript:**
```javascript
// React
import { useState, useEffect, useRef, useCallback } from "react";

// Components (relative)
import { TrafficLight } from "./TrafficLight";

// Services
import { api } from "../services/api";
import { useWebSocket } from "../hooks/useWebSocket";
```

---

## Architecture

### SO Concept Mappings (must preserve)
- `threading.Semaphore` → mutex controlling intersection access
- `threading.Thread` (daemon) → each Vehicle is an independent process
- `queue.PriorityQueue` → emergency vehicles (priority 0) dispatched first
- `threading.Event` → simulates traffic light fault/interruption
- JWT roles: `control` (modify lights) / `viewer` (read-only)

### Directory Structure
```
backend/
├── main.py              # FastAPI entry point
├── config.py            # Pydantic Settings
├── core/                # SO abstractions
│   ├── traffic_light.py
│   ├── vehicle.py
│   ├── scheduler.py
│   ├── intersection.py
│   ├── fault_handler.py
│   └── deadlock_detector.py
├── simulation/
│   ├── engine.py        # Kernel tick loop
│   └── network.py      # RAG graph
├── auth/
│   ├── jwt_handler.py
│   └── roles.py
├── api/
│   ├── routes_auth.py
│   ├── routes_simulation.py
│   ├── routes_control.py
│   └── websocket.py
└── db/
    ├── database.py
    └── models.py

frontend/
├── eslint.config.js     # ESLint flat config (ESM)
├── vite.config.js       # Vite + React + Tailwind v4
├── package.json         # react: "^19.2.5"
└── src/
    ├── App.jsx
    ├── index.css        # Tailwind + animations
    ├── components/
    ├── hooks/
    └── services/
```

### Key Implementation Facts
- `SimulationEngine._loop()` runs every 1s (hardware clock tick)
- Traffic light cycle: RED → GREEN → YELLOW → RED (yellow = 3s, configurable)
- `FaultHandler` triggers random faults every 15-30s, auto-recovers at 5s
- `DeadlockDetector` uses 10s timeout with vehicle rollback
- Vehicles wait via `threading.Event.wait()` (no CPU burn)

---

## Agent Constraints (from `.github/agents/agent-traffic.agent.md`)

**Rules:**
1. ALWAYS consult `README.md` before writing code
2. NEVER skip phases - implement one at a time
3. NEVER replace low-level SO abstractions with high-level libraries
4. Only use dependencies in `requirements.txt`
5. NEVER assume ambiguous design decisions - ask user first

**Approach:**
1. Read `README.md` and `requirements.txt` first
2. Identify current phase and detail steps
3. Verify new files fit the directory structure
4. Write highly readable code with extensive comments for critical sections
5. Ask clear questions if requirements are ambiguous

---

## Quirks

- `frontend/eslint.config.js` uses ESLint flat config (ESM), not `.eslintrc`
- Frontend has Tailwind v4 (`@tailwindcss/vite`), not v3
- JWT secret hardcoded as `"traffic-system-secret"` in `config.py`
- SQLite DB at `traffic.db` (gitignored)
- `Vehicle` waits on `scheduler.wait_for_dispatch()` via `threading.Event.wait()`

---

## Current State

- **Backend is complete** - all modules implemented
- **Frontend is complete** - all components implemented
- **README is a design document** - may not reflect current code