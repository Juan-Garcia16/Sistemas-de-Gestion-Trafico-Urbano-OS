import threading
import time
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
                    # Asumimos que rojo dura lo mismo que el tiempo en verde por simplicidad didáctica
                    current_red_time = light.green_time

                    if light.state == "RED" and timer >= current_red_time:
                        light.state = "GREEN"
                        self._light_timers[inter.id] = 0

                        # --- Concepto de SO: Context Switch Yield ---
                        # Habilitado el recurso, el Kernel notifica al Scheduler para
                        # procesar inmediatamente la "Ready Queue" y despachar al vehículo ganador.
                        self.scheduler.dispatch_next(inter.id)

                    elif light.state == "GREEN" and timer >= light.green_time:
                        light.state = "YELLOW"
                        self._light_timers[inter.id] = 0

                    elif light.state == "YELLOW" and timer >= 3: # 3s de transición amarilla
                        light.state = "RED"
                        self._light_timers[inter.id] = 0

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

    def state_snapshot(self) -> dict:
        """
        Punto de inspección para extraer estadísticas del sistema operante en un corte temporal.
        Equivalente a consultar el sistema de archivos virtual dinámico nativo, como /proc en UNIX.
        """
        intersections_state = []
        for inter in self.network.get_all():
            intersections_state.append({
                "id": inter.id,
                "state": inter.light.state
            })

        vehicles_state = []
        # Eliminamos limpieza profunda por ahora, mostramos tanto los WAIT como los DONE.
        for v_id, v in list(self.active_vehicles.items()):
            vehicles_state.append({
                "id": v.vehicle_id,
                "status": v.status,
                "position": v.current_position
            })

        return {
            "intersections": intersections_state,
            "vehicles": vehicles_state,
            "tick": self._tick_count
        }
