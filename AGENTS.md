# AGENTS.md

## Project Overview
Spanish-language academic Operating Systems project. Models urban traffic with concurrent vehicles, synchronized traffic lights, emergency priority, fault detection, and role-based access.

**Stack:** Python/FastAPI backend (threading + asyncio) | React/Vite frontend (WebSockets) | SQLite

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
  core/           # SO abstractions: TrafficLight, Vehicle, Scheduler, Intersection
  simulation/    # Engine (kernel tick loop), Network (RAG)
  auth/          # JWT handler, role decorators (missing - not created yet)
  api/           # REST routes + WebSocket broadcast (missing)
  db/            # SQLite models (missing)
  main.py        # MISSING - FastAPI entry point needs to be created
  config.py      # MISSING - config needs to be created
frontend/
  src/
    App.jsx      # Currently default Vite scaffold - not implemented per README
    components/  # MISSING - components listed in README don't exist yet
    hooks/       # MISSING
    services/    # MISSING
```

### Key Code Facts
- `SimulationEngine._loop()` runs every 1s (hardware clock tick analogy)
- Traffic light cycle: RED → GREEN → YELLOW → RED (yellow = 3s)
- `FaultHandler` triggers random faults every 15-30s, auto-recovers at 5s
- Vehicles use `daemon=True` threads (die when main process exits)

---

## Commands

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000

# Frontend (Tailwind v4 via @tailwindcss/vite plugin)
cd frontend && npm install && npm run dev
npm run lint   # ESLint (flat config, React hooks)
npm run build # Vite build
```

---

## Current State (important)

**Backend is partially implemented:** `core/` and `simulation/` exist with well-commented academic code, but `main.py`, `config.py`, `auth/`, `api/`, and `db/` are missing.

**Frontend is a default Vite scaffold:** `App.jsx` is the boilerplate screen, not the traffic grid described in README.

**README is a design document**, not a reflection of current code.

---

## Conventions

- Backend code uses Spanish comments explaining SO concepts
- JWT secret hardcoded as `"traffic-system-secret"` in `auth/jwt_handler.py`
- SQLite DB at `traffic.db` (gitignored)
- `requirements.txt` has exact pinned versions; `frontend/package.json` has broad semver

---

## Existing Agent Instructions

`.github/agents/agent-traffic.agent.md` defines constraints:
- Always consult `README.md` before writing code
- Implement one phase at a time (do not skip ahead)
- Never replace low-level SO abstractions with high-level libraries
- Only use deps in `requirements.txt`
- Ask user before ambiguous design decisions

---

## Quirks

- `frontend/eslint.config.js` uses ESLint flat config (ESM), not `.eslintrc`
- Frontend has Tailwind v4 (`@tailwindcss/vite`), not v3
- Frontend `package.json` has `react: "^19.2.5"` (very recent)
- `Vehicle` waits on `scheduler.wait_for_dispatch()` which blocks via `threading.Event.wait()` (no CPU burn while waiting)