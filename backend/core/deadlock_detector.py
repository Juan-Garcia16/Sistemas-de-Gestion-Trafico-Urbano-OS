import threading
import time
from typing import Callable

from simulation.network import IntersectionNetwork
from core.scheduler import TrafficScheduler


class DeadlockDetector:
    """
    Detecta y resuelve interbloqueos usando timeout y rollback.
    
    --- Concepto de SO: Detección de Deadlock ---
    En sistemas operativos reales, existen algoritmos para detectar deadlocks
    cuando procesos quedan bloqueados esperando recursos que nunca se liberan.
    Este implementa un algoritmo de timeout: si un vehículo espera más de
    MAX_WAIT_TIME, se considera deadlock y se remueve de la cola (rollback).
    
    La resolución de deadlock (remover un proceso de la cola) es análoga a
    terminar un proceso en un SO real para romper el ciclo de espera.
    """
    MAX_WAIT_TIME = 10  # Segundos antes de declarar deadlock

    def __init__(self, scheduler: TrafficScheduler, on_deadlock: Callable):
        """
        Args:
            scheduler: Instancia de TrafficScheduler con las PriorityQueues
            on_deadlock: callback(vehicle_id, intersection_id) cuando se detecta deadlock
        """
        self.scheduler = scheduler
        self.on_deadlock = on_deadlock
        self._running = False
        self._thread = None
        # Registro de timestamps: vehicle_id -> timestamp cuando entró a la cola
        self._vehicle_timestamps: dict[str, float] = {}

    def start(self):
        """Inicia el thread demonio de detección de deadlocks."""
        self._running = True
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Detiene el detector de deadlocks."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def register_vehicle(self, vehicle_id: str):
        """
        Registra cuando un vehículo entra a esperar en una cola.
        Se llama cuando el vehículo hace enqueue en el scheduler.
        """
        self._vehicle_timestamps[vehicle_id] = time.time()

    def unregister_vehicle(self, vehicle_id: str):
        """
        Remueve el vehículo del registro cuando sale de la cola.
        Se llama cuando el vehículo es despachado o completamos su ruta.
        """
        self._vehicle_timestamps.pop(vehicle_id, None)

    def _check_loop(self):
        """Loop de verificación de deadlocks cada segundo."""
        while self._running:
            time.sleep(1)  # Verificar cada segundo
            current_time = time.time()
            to_remove = []

            # Buscar vehículos que han esperado demasiado
            for vehicle_id, timestamp in self._vehicle_timestamps.items():
                if current_time - timestamp > self.MAX_WAIT_TIME:
                    to_remove.append(vehicle_id)

            # Notificar y limpiar los deadlocks detectados
            for vehicle_id in to_remove:
                del self._vehicle_timestamps[vehicle_id]
                # Notificar al callback para loguear en event_log
                self.on_deadlock(vehicle_id, "timeout")