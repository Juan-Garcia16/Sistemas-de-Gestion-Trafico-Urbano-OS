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
        # Estados posibles: RED | GREEN | YELLOW | FAULT
        self.state = "RED"
        self.green_time = green_time
        self.red_time = red_time  # Duración independiente de la fase roja del semáforo
        
        # --- Concepto de SO: Semáforo Mutex ---
        # Un Semáforo inicializado en 1 actúa como una cerradura de exclusión mutua (Mutex).
        # Esto asegura que únicamente un vehículo (hilo) pueda ocupar el recurso 
        # (intersección) en un momento dado, evitando una condición de carrera (choque).
        self.semaphore = threading.Semaphore(1)
        
        # --- Concepto de SO: Manejo de Interrupciones ---
        # threading.Event se usa de forma análoga a una interrupción de hardware/software.
        # Permite despertar o notificar inmediatamente a todos los procesos bloqueados
        # de que ha ocurrido un fallo abrupto en el sistema.
        self.fault_event = threading.Event()
        
        # --- Concepto de SO: Monitor ---
        # Un Lock interno para proteger estrictamente las variables de estado (ej. self.state)
        # cuando hilos independientes (ej. manejador de interrupciones vs el motor de simulación)
        # intentan leer o escribir sobre ellas.
        self._lock = threading.Lock()

    def acquire(self, vehicle_id: str, timeout: float = 5.0) -> bool:
        """
        Un vehículo (hilo) intenta acceder al recurso compartido.
        Representa la primitiva P() o Wait() en la teoría de semáforos de Dijkstra.
        """
        # El timeout actúa como un mecanismo preventivo nativo frente a interbloqueos (deadlocks).
        # Si no logra entrar en el tiempo estipulado, retrocede.
        acquired = self.semaphore.acquire(timeout=timeout)
        if not acquired:
            # Reportamos fallo de adquisición al no poder tomar la cerradura,
            # previniendo que el proceso se quede colgado eternamente.
            return False
        return True

    def release(self):
        """
        El vehículo sale de la intersección.
        Representa la primitiva V() o Signal() en la teoría de semáforos.
        """
        self.semaphore.release()

    def trigger_fault(self):
        """
        Rutina para inyectar una interrupción en el sistema (ej. sensor dañado).
        """
        with self._lock: # Uso de _lock para garantizar atomicidad de la escritura
            self.state = "FAULT"
        
        # Se envía la señal; interrumpe el flujo normal notificando el problema
        self.fault_event.set()

    def restore(self):
        """
        Rutina de servicio de interrupción (ISR - Interrupt Service Routine) 
        para reanudar la operativa normal.
        """
        with self._lock:
            self.state = "RED"
        
        # Restablece la bandera a nivel procesador/hilo
        self.fault_event.clear()
