import threading
import time
from config import TRAFFIC_LIGHT_YELLOW_DURATION
from simulation.network import IntersectionNetwork
from core.scheduler import TrafficScheduler
from core.vehicle import Vehicle, Priority

class SimulationEngine:
    """
    Motor central de simulación.

    --- Concepto de SO: Main Kernel Loop / Hardware Clock ---
    Actúa de modo equivalente al 'Tick' de reloj de hardware que genera interrupciones
    periódicas. Este Motor es el núcleo (Kernel) que despierta en cada tick temporal
    para coordinar los recursos físicos (semáforos) y ceder el control al
    planificador (Scheduler) en el momento idóneo.
    """
    def __init__(self, network: IntersectionNetwork, scheduler: TrafficScheduler, broadcast_func=None):
        self.network = network
        self.scheduler = scheduler

        # --- Concepto de SO: Señal de Interrupción Global (SIGTERM) ---
        # Event() permite detener grácilmente el hilo maestro de simulación imitando
        # una señal de apagado recibida por el sistema (ej. ACPI shutdown signal).
        self._stop_event = threading.Event()
        self._tick_thread = None

        # --- Concepto de SO: Tabla de Procesos (Process Table) ---
        # El Kernel rastrea centralizadamente todas las instancias de procesos (Vehículos) activos.
        self.active_vehicles: dict[str, Vehicle] = {}

        # Tiempos internos para simular el ciclo de duración de cada semáforo
        self._light_timers = {node.id: 0 for node in self.network.get_all()}

        # Función de broadcast para WebSocket
        self._broadcast_func = broadcast_func

        # Contador de ticks
        self._tick_count = 0
        self._vehicle_counter = 0

    def start(self):
        """
        Secuencia de 'Boot'. Levanta el hilo principal del Kernel.
        Al usar daemon=True, emula un hilo esencial de sistema que morirá 
        únicamente cuando la máquina entera (el proceso principal) se apague.
        """
        if self._tick_thread is None or not self._tick_thread.is_alive():
            self._stop_event.clear()
            self._tick_thread = threading.Thread(target=self._loop, daemon=True)
            self._tick_thread.start()

    def stop(self):
        """
        Dispara la señal de terminación ordenada cerrando el Loop.
        """
        self._stop_event.set()
        if self._tick_thread:
            self._tick_thread.join(timeout=2.0)

    def _loop(self):
        """
        Loop principal del Timer Interrupt (Hardware Clock).
        Corre periódicamente para gestionar transiciones de estado y despacho.
        """
        while not self._stop_event.is_set():
            self._tick_count += 1
            for inter in self.network.get_all():
                light = inter.light

                # Acceso atómico al Recurso. Garantizamos seguridad en concurrencia.
                with light._lock:
                    if light.state == "FAULT":
                        # Semáforo interrumpido. Se ignora la transición civil regular.
                        continue

                    self._light_timers[inter.id] += 1
                    timer = self._light_timers[inter.id]

                    # Máquina de estados cíclica: RED -> GREEN -> YELLOW -> RED
                    # Usa red_time independiente del semáforo
                    current_red_time = light.red_time

                    if light.state == "RED" and timer >= current_red_time:
                        light.state = "GREEN"
                        self._light_timers[inter.id] = 0

                        # --- Concepto de SO: Context Switch Yield ---
                        # Habilitado el recurso, el Kernel notifica al Scheduler para
                        # procesar inmediatamente la "Ready Queue" y despachar al vehículo ganador.
                        self.scheduler.dispatch_next(inter.id)

                    elif light.state == "YELLOW" and timer >= TRAFFIC_LIGHT_YELLOW_DURATION:
                        light.state = "RED"
                        self._light_timers[inter.id] = 0

                    elif light.state == "GREEN" and timer >= light.green_time:
                        light.state = "YELLOW"
                        self._light_timers[inter.id] = 0

                    elif light.state == "GREEN":
                        self.scheduler.dispatch_next(inter.id)

            # --- Broadcast del estado a través de WebSocket ---
            if self._broadcast_func:
                snapshot = self.state_snapshot()
                state = {
                    "type": "STATE_UPDATE",
                    "intersections": snapshot.get("intersections", []),
                    "vehicles": snapshot.get("vehicles", []),
                    "alerts": [],
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                # Llamar función async de broadcast desde contexto sync
                try:
                    import asyncio
                    # Crear un nuevo event loop en el thread secundario
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._broadcast_func(state))
                    loop.close()
                except Exception as e:
                    pass

            # --- Concepto de SO: Sleep / Idle cycle ---
            # El procesador lógico entra en Idle esperando al siguiente ciclo del Reloj.
            time.sleep(1.0)

    def add_vehicle(self, vehicle_id: str, route: list, priority: Priority):
        """
        Equivalente a la System Call fork() (Linux) o CreateProcess() (Windows).
        El Kernel solicita creación de un PCB e inserta el proceso a la vida activa,
        llamando seguidamente a su .start() para que el OS lo planifique.
        """
        vehicle = Vehicle(vehicle_id, route, priority, self.scheduler)
        self.active_vehicles[vehicle_id] = vehicle
        vehicle.start()
        vehicle._arrival_tick = self._tick_count

    def state_snapshot(self) -> dict:
        def _coords(inter_id: str) -> dict:
            parts = inter_id.split("_")
            return {"x": int(parts[1]), "y": int(parts[2])}

        # Obtener info de colas del scheduler (thread-safe)
        queue_sizes = self.scheduler.get_queue_sizes() if hasattr(self.scheduler, 'get_queue_sizes') else {}
        queue_vehicles = {}
        for inter in self.network.get_all():
            if hasattr(self.scheduler, 'get_queued_vehicles'):
                queue_vehicles[inter.id] = self.scheduler.get_queued_vehicles(inter.id)
            else:
                queue_vehicles[inter.id] = []

        intersections_state = []
        for inter in self.network.get_all():
            # Buscar vehículo MOVING en esta intersección (dueño del mutex)
            mutex_owner = None
            for v_id, v in self.active_vehicles.items():
                if v.status == "MOVING":
                    current_inter = v.route[v.current_position - 1] if v.current_position > 0 and v.current_position - 1 < len(v.route) else (v.route[0] if v.route else None)
                    if current_inter == inter.id:
                        mutex_owner = v_id
                        break

            intersections_state.append({
                "id": inter.id,
                "state": inter.light.state,
                "position": _coords(inter.id),
                "queue_size": queue_sizes.get(inter.id, 0),
                "queued_vehicles": queue_vehicles.get(inter.id, []),
                "mutex_owner": mutex_owner,
                "mutex_locked": mutex_owner is not None
            })

        vehicles_state = []
        done_vehicles = []
        for v_id, v in list(self.active_vehicles.items()):
            if v.status == "DONE":
                done_vehicles.append(v_id)
                continue
            current_inter_id = v.route[v.current_position] if v.current_position < len(v.route) else v.route[-1] if v.route else "unknown"
            vehicles_state.append({
                "id": v.vehicle_id,
                "status": v.status,
                "position": v.current_position,
                "route": v.route,
                "priority": v.priority.name,
                "current_intersection": current_inter_id,
                "currentPosition": _coords(current_inter_id),
                "wait_time_ticks": max(0, self._tick_count - getattr(v, '_arrival_tick', self._tick_count))
            })

        return {
            "intersections": intersections_state,
            "vehicles": vehicles_state,
            "tick": self._tick_count
        }

        for v_id in done_vehicles:
            self.active_vehicles.pop(v_id, None)
