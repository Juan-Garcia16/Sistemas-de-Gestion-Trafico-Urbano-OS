import threading
import time

class TrafficLight:
    """
    Representa un semáforo como recurso compartido del Sistema Operativo.
    Esta clase encapsula una sección crítica (la intersección) a la que los vehículos
    (hilos/procesos) intentan acceder de forma concurrente, garantizando el aislamiento
    y previniendo inconsistencias de estado.
    """
    def __init__(self, intersection_id: str, green_time: int = 10, red_time: int = 10):
        self.id = intersection_id
        self.state = "RED"
        self.green_time = green_time
        self.red_time = red_time
        
        self.semaphore = threading.Semaphore(1)
        self.fault_event = threading.Event()
        self._lock = threading.Lock()
        
        self._occupied_by: str | None = None
        self._fault_blocked: list = []
        self._was_faulty = False
        self._force_release_event = threading.Event()

    def acquire(self, vehicle_id: str, timeout: float = 5.0) -> bool:
        """
        Un vehículo (hilo) intenta acceder al recurso compartido.
        Representa la primitiva P() o Wait() en la teoría de semáforos de Dijkstra.
        """
        with self._lock:
            if self.state == "FAULT":
                self._fault_blocked.append(vehicle_id)
                return False
        
        acquired = self.semaphore.acquire(timeout=timeout)
        if not acquired:
            with self._lock:
                if vehicle_id in self._fault_blocked:
                    self._fault_blocked.remove(vehicle_id)
            return False
        
        with self._lock:
            self._occupied_by = vehicle_id
            if vehicle_id in self._fault_blocked:
                self._fault_blocked.remove(vehicle_id)
        return True

    def release(self):
        """
        El vehículo sale de la intersección.
        Representa la primitiva V() o Signal() en la teoría de semáforos.
        """
        with self._lock:
            if self.state == "FAULT":
                return
            was_faulty = self._was_faulty
            self._occupied_by = None
            self._was_faulty = False
        
        if was_faulty:
            # Si el recurso fue restaurado tras un fallo, restore() ya liberó el semáforo.
            # Retornamos de inmediato para evitar liberar por duplicado.
            return
        
        try:
            self.semaphore.release()
        except ValueError:
            pass

    def trigger_fault(self):
        """
        Rutina para inyectar una interrupción en el sistema (ej. sensor dañado).
        """
        with self._lock:
            self.state = "FAULT"
            self._was_faulty = True
        
        self.fault_event.set()
        self._force_release_event.set()

    def restore(self):
        with self._lock:
            self.state = "GREEN"
            self._was_faulty = True
            self._occupied_by = None
        
        self.fault_event.clear()
        self._force_release_event.clear()
        
        try:
            self.semaphore.release()
        except ValueError:
            pass

    def get_blocked_vehicles(self) -> list:
        """Retorna la lista de vehículos bloqueados tratando de adquirir durante FAULT."""
        with self._lock:
            return list(self._fault_blocked)