# Sistema de Gestión de Tráfico Urbano — Sistemas Operativos

## 🎯 Guía de presentación

---

## 1. El Problema de SO

> *"Una ciudad con N intersecciones y M vehículos concurrentes. Si no hay control, los vehículos colisionan. Si no hay prioridad, una ambulancia espera detrás de 10 autos. Si un semáforo falla, el caos se propaga."*

**Esto es exactamente lo que resuelve un Sistema Operativo:**

| Problema urbano | Problema de SO |
|-----------------|----------------|
| Choque de vehículos en una intersección | Condición de carrera — dos procesos acceden al mismo recurso |
| Ambulancia atrapada en el tráfico | Proceso crítico sin prioridad — inanición |
| Dos autos bloqueándose mutuamente en calles cruzadas | Deadlock — espera circular de recursos |
| Semáforo dañado | Interrupción de hardware — el recurso deja de responder |
| Cualquiera puede cambiar tiempos de semáforos | Seguridad — acceso no autorizado a recursos del kernel |

---

## 2. Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                  NAVEGADOR (Frontend)                    │
│  React + Tailwind │ WebSocket en tiempo real │ JWT Auth │
├─────────────────────────────────────────────────────────┤
│                   FastAPI (Backend)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Auth JWT │  │ API REST │  │WebSocket │  │ SQLite  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────┤
│              MOTOR DE SIMULACIÓN (Kernel)                │
│  ┌────────────┐ ┌───────────┐ ┌──────────┐ ┌─────────┐ │
│  │TrafficLight│ │ Scheduler │ │  Fault   │ │Deadlock │ │
│  │ (Mutex SO) │ │(Prioridad)│ │ Handler  │ │Detector │ │
│  └────────────┘ └───────────┘ └──────────┘ └─────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Vehículos = Threads concurrentes          │   │
│  │    Cada vehículo es un proceso independiente      │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Stack real:** Python 3.12 + FastAPI + threading + asyncio | React 19 + Vite 8 + Tailwind v4 | SQLite

---

## 3. Mapeo: Concepto SO → Implementación

### 🔒 Exclusión Mutua (Mutex)

| SO | Implementación |
|----|---------------|
| **Semáforo binario (mutex)** | `threading.Semaphore(1)` en `TrafficLight` — solo 1 vehículo puede ocupar la intersección |
| **Sección crítica** | La intersección es el recurso compartido protegido por el semáforo |
| **Primitivas P() y V()** | `light.acquire()` (Wait) y `light.release()` (Signal) |

**Cómo se ve en la demo:** 3 autos lanzados a la misma intersección → solo 1 cruza → 🔒 en el grid → Métricas: mutex TOMADO, 2 en cola.

---

### 📋 Priority Scheduling

| SO | Implementación |
|----|---------------|
| **Planificación por prioridad** | `queue.PriorityQueue` — heap interno ordena por prioridad (0=mayor, 2=menor) |
| **Ready Queue por recurso** | Cola independiente por cada intersección |
| **Dispatcher** | `scheduler.dispatch_next()` — el motor llama esto cuando el semáforo abre |
| **PCB (Process Control Block)** | `Vehicle.status`: WAITING → MOVING → DONE. `current_position`: índice en la ruta. |

**Cómo se ve en la demo:** 🚑 ambulancia (P0) + 🚗🚗 normales (P2) → la ambulancia pasa **primero** aunque llegó después. Badge P0/P2 visible en cada vehículo.

---

### 💀 Detección y Resolución de Deadlock

| SO | Implementación |
|----|---------------|
| **Detección por timeout** | `DeadlockDetector` — si un vehículo espera >10s, se declara deadlock |
| **Wait-for Graph implícito** | `IntersectionNetwork` — grafo de recursos (RAG), las rutas de vehículos forman aristas de espera |
| **Rollback** | `scheduler.remove_vehicle()` — remueve el vehículo de todas las colas (terminación de proceso) |
| **Prevención** | `Semaphore.acquire(timeout=5s)` — evita bloqueo indefinido en la adquisición |

**Cómo se ve en la demo:** 2 vehículos con rutas cruzadas → se bloquean mutuamente → a los 10s el DeadlockDetector detecta → broadcast DEADLOCK → rollback automático → EventLog registra.

---

### ⚡ Manejo de Interrupciones

| SO | Implementación |
|----|---------------|
| **Interrupción de hardware** | `TrafficLight.fault_event` (`threading.Event`) — señal asíncrona que interrumpe el flujo normal |
| **ISR (Interrupt Service Routine)** | `light.trigger_fault()` → estado FAULT → `light.restore()` → vuelve a RED |
| **Interrupciones periódicas (clock)** | `SimulationEngine._loop()` — tick cada 1s, análogo al reloj del sistema |
| **Manejo de señales** | `_stop_event` — señal de apagado (SIGTERM) para detener el motor |

**Cómo se ve en la demo:** Cada 15-30s un semáforo aleatorio entra en FAULT → overlay rojo pulsante en el grid + AlertBanner → a los 5s se recupera solo. También se puede disparar manualmente desde el panel.

---

### 🔐 Seguridad y Control de Acceso

| SO | Implementación |
|----|---------------|
| **Dominios de seguridad** | JWT con roles: `control` (puede modificar) y `viewer` (solo lectura) |
| **Protección de recursos del kernel** | Decorador `require_role("control")` en rutas sensibles |
| **Auditoría** | `EventLog` en SQLite — registra FAULT, DEADLOCK, CONFIG_CHANGE con timestamp y usuario |

**Cómo se ve en la demo:** Usuario `viewer` no ve el Panel de Control. Si intenta acceder a `/control/*` vía API → HTTP 403.

---

## 4. Guión de la Demo (5-7 minutos)

```
⏱ 0:00 — CONTEXTO
  "Una ciudad es un sistema operativo: intersecciones = recursos,
   vehículos = procesos, semáforos = mutex, ambulancias = procesos prioritarios."

⏱ 0:30 — LOGIN + ARQUITECTURA
  - Mostrar login → JWT con roles (viewer / control)
  - Explicar: "Solo usuarios 'control' pueden modificar semáforos"
  - Iniciar sesión como admin

⏱ 1:00 — INICIAR SIMULACIÓN
  - Click "Iniciar Simulación"
  - Mostrar grid 3×3: 9 intersecciones, calles, semáforos de 3 luces
  - Señalar: "Cada intersección tiene un mutex. Solo 1 vehículo a la vez."

⏱ 1:30 — DEMO: EXCLUSIÓN MUTUA
  - Tab "🎬 Demos" → Click "🔒 Exclusión Mutua"
  - 3 autos compiten por intersection_1_1
  - Señalar: 🔒 en el grid, Métricas SO muestra "mutex TOMADO por mutex-car-1"
  - "Esto es la sección crítica: solo 1 proceso puede estar en ella."

⏱ 2:30 — DEMO: PRIORITY SCHEDULING
  - Click "🚑 Priority Scheduling"
  - 1 ambulancia + 2 autos normales
  - Señalar: "La ambulancia tiene P0, los autos P2."
  - "El scheduler despacha primero al de mayor prioridad — ambulancia pasa primero."
  - Mostrar badge P0 en ambulancia, P2 en autos

⏱ 3:30 — DEMO: DEADLOCK
  - Click "💀 Deadlock + Rollback"
  - 2 vehículos con rutas que se cruzan
  - "Cada uno espera un recurso que el otro tiene — espera circular."
  - Esperar ~10s → "DeadlockDetector lo detecta por timeout."
  - Broadcast DEADLOCK → rollback → vehículo removido
  - "En un SO real: el kernel mata uno de los procesos para romper el ciclo."

⏱ 5:00 — FALLOS AUTOMÁTICOS
  - Esperar que ocurra un fallo aleatorio (cada 15-30s)
  - O disparar manual: Tab "⚙️ Semáforos" → click en un botón de fallo
  - Señalar: overlay rojo pulsante + AlertBanner
  - "FaultHandler simula una interrupción de hardware."
  - "A los 5s: auto-recuperación. Como un watchdog timer."

⏱ 6:00 — CONTROL EN TIEMPO REAL
  - Tab "⚙️ Semáforos" → seleccionar intersección → sliders green/red
  - "Tiempos modificables en caliente, como ajustar el quantum del scheduler."
  - "Solo rol 'control' puede hacer esto."

⏱ 6:30 — CIERRE
  - "Implementamos los 5 pilares de SO: sincronización, planificación,
     detección de deadlock, interrupciones, y seguridad."
  - "Todo corre en tiempo real con WebSockets, threads concurrentes,
     y un motor de simulación que emula el kernel de un SO."
```

---

## 5. Puntos clave para mencionar

- **9 intersecciones = 9 recursos compartidos**, cada uno con su propio mutex y cola de prioridad
- **Cada vehículo es un `threading.Thread` independiente** — ejecución concurrente real, no simulada
- **`threading.Semaphore(1)`** = mutex binario. `acquire()` = P(), `release()` = V(). Con timeout para prevenir deadlock.
- **`queue.PriorityQueue`** = algoritmo de planificación real. Menor valor numérico = mayor prioridad (como en Unix).
- **Detección de deadlock por timeout** (10s) + **rollback** (remover proceso). Algoritmo práctico usado en sistemas reales.
- **FaultHandler** = interrupciones aleatorias cada 15-30s. `threading.Event` = señal de interrupción. Auto-recuperación en 5s.
- **JWT + roles** = control de acceso a recursos del kernel. `control` modifica, `viewer` solo observa.
- **WebSocket** = stream de estado en tiempo real. El engine hace broadcast en cada tick (cada 1s).
- **Métricas SO en vivo** = mutex ocupado/libre, tamaño de colas, tiempos de espera, prioridades.

---

## 6. Datos técnicos rápidos

| Dato | Valor |
|------|-------|
| Lenguaje | Python 3.12 (backend) + JavaScript/React (frontend) |
| Concurrencia | `threading.Thread` (daemon) — 1 thread por vehículo |
| Sincronización | `threading.Semaphore(1)` + `threading.Lock` |
| Planificación | `queue.PriorityQueue` con heap interno |
| Comunicación | FastAPI REST + WebSocket nativo |
| Persistencia | SQLite — users, event_log, light_config |
| Auth | JWT HS256, 8h expiración, roles: viewer/control |
| Tick del kernel | 1 segundo (configurable) |
| Ciclo semáforo | RED → GREEN → YELLOW → RED (green_time/red_time configurables) |
| Fallos | Aleatorios cada 15-30s, auto-recuperación 5s |
| Deadlock timeout | 10 segundos |

---

## 🚀 Comandos para iniciar (el día de la presentación)

```bash
# Terminal 1 — Backend
cd backend && source .venv/bin/activate && rm -f traffic.db && uvicorn main:app --port 8000

# Terminal 2 — Frontend  
cd frontend && npm run dev

# Abrir navegador en http://localhost:5173
# Registrar usuario admin:
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","role":"control"}'
```
