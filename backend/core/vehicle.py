import threading
import random
import time
from enum import IntEnum
from config import VEHICLE_MAX_LIFETIME
from core.scheduler import log_vehicle_move

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
    def __init__(self, vehicle_id: str, start_intersection: str, network, priority: Priority, scheduler, route_path: list[str] | None = None):
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
        self._dispatched_at_tick: int = -1
        self._dispatch_seq: int = 0
        self._held_light: str | None = None
        self._waiting_for_fault_clear: bool = False
        self.route_path = route_path
        self.route_index = 0

    def run(self):
        """
        Ciclo de vida del proceso. Navegación dinámica usando get_neighbors().
        El vehículo camina aleatoriamente por la red hasta alcanzar su lifetime máximo.
        """
        while self._visited_count < _MAX_LIFETIME:
            if self._waiting_for_fault_clear and self.queued_at:
                dest_light = self.network.nodes[self.queued_at].light
                if dest_light.state == "FAULT":
                    
                    self.scheduler.enqueue(self, self.queued_at)
                    time.sleep(0.05)
                    continue
                
                self._waiting_for_fault_clear = False

            if self._held_light is not None:
                
                self.network.nodes[self._held_light].light.release()
                self._held_light = None

            neighbors = self.network.get_neighbors(self.current_intersection)

            if not neighbors:
                break

            if self.route_path and self.route_index < len(self.route_path) - 1:
                self.route_index += 1
                next_id = self.route_path[self.route_index]
            else:
                next_inter = random.choice(neighbors)
                next_id = next_inter.id

            self.status = "WAITING"
            self._dispatched_this_tick = False
            self.queued_at = self.current_intersection
            self.scheduler.enqueue(self, next_id)
            self.scheduler.wait_for_dispatch(self.vehicle_id)

            dest_light = self.network.nodes[next_id].light
            
            acquired = dest_light.acquire(self.vehicle_id, timeout=5.0)

            if not acquired:
                if dest_light.state == "FAULT":
                    
                    self.status = "WAITING"
                    self._dispatched_this_tick = False
                    self._waiting_for_fault_clear = True
                    self.queued_at = next_id
                    self.scheduler.enqueue(self, next_id)
                    time.sleep(0.05)
                    continue
                
                self.status = "WAITING"
                self._dispatched_this_tick = False
                self.queued_at = self.current_intersection
                self.scheduler.enqueue(self, self.current_intersection)
                continue

            

            self._held_light = next_id

            tick_at_wake = self.scheduler._current_tick
            while self.scheduler._current_tick == tick_at_wake:
                if dest_light.state == "FAULT":
                    self.status = "WAITING"
                    while dest_light.state == "FAULT":
                        time.sleep(0.1)
                    self.status = "MOVING"
                time.sleep(0.05)

            if dest_light.state == "FAULT":
                self.status = "WAITING"
                while dest_light.state == "FAULT":
                    time.sleep(0.1)

            prev_inter = self.current_intersection
            self.status = "MOVING"
            self.current_intersection = next_id
            self._dispatched_this_tick = True
            
            log_vehicle_move(self.vehicle_id, prev_inter, next_id, self._dispatched_at_tick, self._dispatch_seq)

            if self.route_path and self.route_index >= len(self.route_path) - 1:
                
                break

        if self._held_light is not None:
            try:
                self.network.nodes[self._held_light].light.release()
            except Exception:
                pass

        self.status = "DONE"