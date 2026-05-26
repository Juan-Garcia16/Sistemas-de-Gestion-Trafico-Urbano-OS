import queue
import threading
import time
from typing import Optional

# Logger para movimientos de vehículos (diagnóstico Bug 3)
_movement_log: list[dict] = []
_log_lock = threading.Lock()

def get_movement_log() -> list[dict]:
    with _log_lock:
        return list(_movement_log)

def clear_movement_log():
    with _log_lock:
        _movement_log.clear()

def log_vehicle_move(vehicle_id: str, from_id: str, to_id: str, tick: int, dispatch_seq: int):
    with _log_lock:
        _movement_log.append({
            "vehicle_id": vehicle_id,
            "from": from_id,
            "to": to_id,
            "tick": tick,
            "seq": dispatch_seq
        })

class TrafficScheduler:
    """
    Implementa Priority Scheduling para las intersecciones (recursos).
    
    --- Concepto de SO: CPU/Resource Scheduler ---
    Análogamente a cómo un Planificador (Scheduler) del Sistema Operativo decide 
    qué proceso alojar en la CPU basado en políticas de planificación, este orquestador 
    gestiona qué vehículo (proceso) obtiene acceso al semáforo (recurso crítico).
    Utiliza el algoritmo de "Priority Scheduling", garantizando que procesos de 
    máxima prioridad (ej. vehículos de EMERGENCIA con prioridad 0) se despachen primero.
    """
    def __init__(self):
        # _queues actúa como las "Ready Queues" (Colas de listos) multiplicadas por recurso
        # PriorityQueue ordena automáticamente mediante una jerarquía (heap) interna.
        self._queues: dict[str, queue.PriorityQueue] = {}
        
        # Otorga una bandera específica por proceso para simular el cambio de contexto a RUNNING
        self._dispatch_events: dict[str, threading.Event] = {}
        
        # Monitor para proteger la creación y acceso seguro a las estructuras del Planificador
        self._lock = threading.Lock()

        # Bug 3: Control de vehículos despachados este tick para evitar duplicados
        self._dispatched_this_tick: set = set()
        self._current_tick: int = 0
        self._dispatch_seq: int = 0  # Para rastrear orden de despachos

    def enqueue(self, vehicle, intersection_id: str):
        """
        Encola un proceso en la cola de listos (Ready Queue) perteneciente a un recurso.
        """
        with self._lock:
            if intersection_id not in self._queues:
                self._queues[intersection_id] = queue.PriorityQueue()
            if vehicle.vehicle_id not in self._dispatch_events:
                self._dispatch_events[vehicle.vehicle_id] = threading.Event()

        entry = (vehicle.priority, time.time(), id(vehicle), vehicle)
        self._queues[intersection_id].put(entry)

        if hasattr(self, '_deadlock_detector') and self._deadlock_detector:
            self._deadlock_detector.register_vehicle(vehicle.vehicle_id)

    def dispatch_next(self, intersection_id: str):
        """
        Actúa como el Despachador (Dispatcher) en el SO, otorgando el recurso 
        al proceso de máxima jerarquía en la estructura 'heap' de la cola.
        """
        if intersection_id in self._queues:
            try:
                entry = self._queues[intersection_id].get_nowait()
                priority, timestamp, vid, vehicle = entry

                if vehicle.vehicle_id in self._dispatched_this_tick:
                    
                    self.enqueue(vehicle, intersection_id)
                    return

                self._dispatched_this_tick.add(vehicle.vehicle_id)
                self._dispatch_seq += 1
                vehicle._dispatched_at_tick = self._current_tick
                vehicle._dispatch_seq = self._dispatch_seq

                if hasattr(self, '_deadlock_detector') and self._deadlock_detector:
                    self._deadlock_detector.unregister_vehicle(vehicle.vehicle_id)

                self._dispatch_events[vehicle.vehicle_id].set()
            except queue.Empty:
                pass

    def wait_for_dispatch(self, vehicle_id: str):
        """
        Envía coercitivamente al hilo al estado WAITING/BLOCKED.
        Retiene la ejecución (sin consumir ciclos activos de CPU) hasta que el OS le notifica.
        """
        event = self._dispatch_events.get(vehicle_id)
        if event:
            event.wait()
            event.clear()

    def remove_vehicle(self, vehicle_id: str):
        """
        Remueve un vehículo de todas las colas de recursos.
        Usado para rollback cuando se detecta un deadlock.
        """
        with self._lock:
            self._dispatch_events.pop(vehicle_id, None)
            for inter_id in list(self._queues.keys()):
                q = self._queues[inter_id]
                remaining = []
                while not q.empty():
                    try:
                        item = q.get_nowait()
                        if item[3].vehicle_id != vehicle_id:
                            remaining.append(item)
                    except queue.Empty:
                        break
                for item in remaining:
                    q.put(item)

    def get_queue_sizes(self) -> dict:
        """
        Devuelve el tamaño de la cola de espera por cada intersección.
        Usado por el panel de métricas SO en el frontend.
        """
        with self._lock:
            sizes = {}
            for inter_id in self._queues:
                sizes[inter_id] = self._queues[inter_id].qsize()
            return sizes

    def get_queued_vehicles(self, intersection_id: str) -> list:
        """
        Devuelve los IDs de vehículos en cola para una intersección específica.
        Inspecciona la PriorityQueue sin modificarla (drena y reconstruye).
        """
        with self._lock:
            if intersection_id not in self._queues:
                return []
            q = self._queues[intersection_id]
            items = []
            while not q.empty():
                try:
                    items.append(q.get_nowait())
                except queue.Empty:
                    break
            # Re-encolar todo (inspección no destructiva)
            for item in items:
                q.put(item)
            return [item[3].vehicle_id for item in items]
