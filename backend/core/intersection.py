from core.traffic_light import TrafficLight

class Intersection:
    """
    Representa un nodo individual dentro de la topología de la ciudad.
    
    Encapsula al recurso crítico (TrafficLight) del sistema operativo simulado.
    Cada intersección es considerada un recurso único e independiente 
    por el cual los procesos (Vehículos) deben competir.
    """
    def __init__(self, intersection_id: str, green_time: int = 10, red_time: int = 10):
        self.id = intersection_id
        self.light = TrafficLight(intersection_id, green_time, red_time)

    @property
    def state(self) -> str:
        """Devuelve el estado actual de la intersección basado en su semáforo."""
        return self.light.state
