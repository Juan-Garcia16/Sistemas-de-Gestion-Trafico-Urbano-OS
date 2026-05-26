# Historial de Progreso — Sistema de Gestión de Tráfico Urbano OS

Este documento rastrea el avance de la implementación del proyecto, asegurando que el desarrollo mantenga coherencia con la arquitectura trazada y los conceptos fundamentales de Sistemas Operativos.

## 🟢 Fase 1: Modelos Core (Completada)

Se definieron los modelos atómicos que sustentan la lógica concurrente del sistema.

- `backend/core/traffic_light.py`: Construcción de la clase **TrafficLight**. Se usó `threading.Semaphore(1)` para aplicar el esquema de Exclusión Mutua (**Mutex**) previniendo condiciones de carrera sobre el recurso crítico (la intersección). Integra primitivas de límite temporal (timeouts en lugar de interbloqueos eternos) y `threading.Event` para instanciar interrupciones por fallos.
- `backend/core/vehicle.py`: Creación de la clase **Vehicle**. Hereda de `threading.Thread`, lo que lo mapea directamente como un **Proceso independiente o hilo de núcleo**, el cual mantiene un modelo de estados análogo a un **PCB** (Process Control Block), operando asíncronamente con enum de prioridades.
- `backend/core/scheduler.py`: Desarrollo del **TrafficScheduler**. Simula al **Planificador de la CPU (CPU Scheduler)** implementando una política de _Priority Scheduling_ mediante `queue.PriorityQueue`, permitiendo la preferencia expedita de vehículos de Estado 0 (Emergencias) junto con eventos de despacho (**Dispatch**) para transicionar vehículos de `WAITING` a `RUNNING` libre de espera activa pura.

## 🟢 Fase 2: Motor de Simulación y Lógica Concurrente (Completada)

Se estructuró el entorno donde coexistirán los semáforos, el planificador y los vehículos de forma coordinada.

- `backend/core/intersection.py`: Aislamiento formal del entorno físico. Define **Intersection** para encapsular al recurso subyacente (`TrafficLight`) como el vértice mínimo de la cuadrícula operativa.
- `backend/simulation/network.py`: Configuración de la topología con **IntersectionNetwork**. Este grafo se comporta como el **Resource Allocation Graph (RAG)** de la instancia, registrando estáticamente colindancias/adyacencias vitales para la subsecuente detección matemática de colisiones en racimo (Deadlocks).
- `backend/simulation/engine.py`: Despliegue del motor principal **SimulationEngine**. Trabaja como el hilo principal asíncrono o bucle central de sistema (**Kernel Loop / Hardware Clock**). Periódicamente interviene alterando los recursos globales (luces que transicionan) y gatillando expropiaciones mediante cambio de contexto al invocar al Scheduler cuando corresponde. Retiene también la lista general (Process Table).

## 🟡 Fase 3: Exposición de API REST y WebSockets (Pendiente)

_Rutas con FastAPI para control backend-frontend y streams bidireccionales nativos de WS. (Siguiente paso)_

## 🔴 Fases 4 a 9 (Pendientes)

- **Fase 4**: Autenticación JWT y sistema de roles base.
- **Fase 5**: Lógica de fallos (FaultHandler) e interbloqueos (DeadlockDetector).
- **Fase 6**: Frontend visual fundacional (Grilla, Semáforos y Trazadores con React+Vite).
- **Fase 7**: Panel interactivo de control de simulación.
- **Fase 8**: Persistencia real en capa SQLite (logs de auditoría).
- **Fase 9**: Ajuste global, calibración y test finales.
