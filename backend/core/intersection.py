from backend.core.traffic_light import TrafficLight

class Intersection:
    """
    Representa un nodo individual dentro de la topología de la ciudad.
    
    Encapsula al recurso crítico (TrafficLight) del sistema operativo simulado.
    Cada intersección es considerada un recurso único e independiente 
    por el cual los procesos (Vehículos) deben competir.
    """
    def __init__(self, intersection_id: str):
        self.id = intersection_id
        # El semáforo es el Recurso (Mutex) incrustado en este nodo.
        self.light = TrafficLight(intersection_id)

    @property
    def state(self) -> str:
        """Devuelve el estado actual de la intersección basado en su semáforo."""
        return self.light.state
