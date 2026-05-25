import threading
import random
import time
from enum import IntEnum
from config import VEHICLE_MAX_LIFETIME
from core.scheduler import log_vehicle_move

# --- Concepto de SO: Prioridad de Procesos (Priority Scheduling) ---
# En los sistemas operativos, el planificador (scheduler) usa niveles de prioridad
# para decidir qué proceso obtiene la CPU. Los valores más bajos numéricamente
# suelen inferir la prioridad más alta (como en Unix/Linux).
class Priority(IntEnum):
    EMERGENCY = 0
    HIGH      = 1
    NORMAL    = 2

_MAX_LIFETIME = VEHICLE_MAX_LIFETIME

class Vehicle(threading.Thread):
    """
    Cada Vehículo representa un Proceso o Tarea independiente en nuestro SO simulado.

    --- Mapeo de SO: Procesos concurrentes vs Hilos ---
    Al heredar de `threading.Thread`, estamos creando una unidad de ejecución concurrente.
    Cada hilo se comporta como un "proceso" que busca recursos (las intersecciones/semáforos)
    y es gestionado por un Scheduler. Se define como un hilo 'daemon' para simular procesos
    en segundo plano que mueren automáticamente si el sistema principal se apaga.
    """
    def __init__(self, vehicle_id: str, start_intersection: str, network, priority: Priority, scheduler):
        super().__init__(daemon=True)
        self.vehicle_id = vehicle_id
        self.current_intersection = start_intersection
        self.network = network
        self.priority = priority
        self.scheduler = scheduler
        self.status = "WAITING"
        self._visited_count = 0
        self.queued_at: str | None = None
        self._dispatched_this_tick = False
        self._dispatched_at_tick: int = -1  # Bug 3: tick en que fue despachado
        self._dispatch_seq: int = 0  # Bug 3: secuencia de despacho

    def run(self):
        """
        Ciclo de vida del proceso. Navegación dinámica usando get_neighbors().
        El vehículo camina aleatoriamente por la red hasta alcanzar su lifetime máximo.
        """
        while self._visited_count < _MAX_LIFETIME:
            neighbors = self.network.get_neighbors(self.current_intersection)

            if not neighbors:
                break

            next_inter = random.choice(neighbors)
            next_id = next_inter.id

            self.status = "WAITING"
            self._dispatched_this_tick = False  # Resetear al encolar
            self.queued_at = self.current_intersection  # Bug 4: guardar posición ACTUAL, no destino
            self.scheduler.enqueue(self, next_id)
            self.scheduler.wait_for_dispatch(self.vehicle_id)  # Block 1: Permission granted

            # Mandatory 1-tick delay - wait until tick advances
            tick_at_wake = self.scheduler._current_tick
            while self.scheduler._current_tick == tick_at_wake:
                time.sleep(0.05)  # Polling until tick advances
            # Tick has advanced to N+1, proceed to wait for dispatch permission

            prev_inter = self.current_intersection
            self.status = "MOVING"
            self.current_intersection = next_id
            self._visited_count += 1
            self._dispatched_this_tick = True  # Bug 3: marcar como ya despachado este tick
            # Log movimiento para diagnóstico Bug 3
            log_vehicle_move(self.vehicle_id, prev_inter, next_id, self._dispatched_at_tick, self._dispatch_seq)

        self.status = "DONE"