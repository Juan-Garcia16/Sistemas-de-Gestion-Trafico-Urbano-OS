from config import TRAFFIC_LIGHT_DEFAULT_GREEN, TRAFFIC_LIGHT_DEFAULT_RED
from core.intersection import Intersection

class IntersectionNetwork:
    """
    Grafo que representa la topología conectada de las intersecciones.
    
    --- Concepto de SO: Resource Allocation Graph (RAG) ---
    En la teoría de Sistemas Operativos, un Grafo de Asignación de Recursos (RAG)
    es un grafo dirigido donde los vértices representan recursos o procesos, y
    las aristas indican quién posee o quién solicita qué. 
    
    Esta clase IntersectionNetwork conforma la base estática de los "Recursos" 
    disponibles. Conocer la adyacencia exacta será fundamental en pasos posteriores
    para el Algoritmo de Detección de Deadlocks, al rastrear ciclos cuando un
    vehículo (Proceso) retiene una intersección (Recurso) y pide la siguiente, 
    formando la estructura clásica de grafos de espera o "Wait-for graphs".
    """
    def __init__(self):
        # Nodos del sistema: identifcador -> Instancia Intersection (Recurso)
        self.nodes: dict[str, Intersection] = {}
        # Lista de adyacencia de la red de recursos
        self.adjacency_list: dict[str, list[str]] = {}

    def add_intersection(self, intersection_id: str, green_time: int = TRAFFIC_LIGHT_DEFAULT_GREEN, red_time: int = TRAFFIC_LIGHT_DEFAULT_RED):
        """Inicializa un nuevo recurso en el grafo del sistema."""
        if intersection_id not in self.nodes:
            self.nodes[intersection_id] = Intersection(intersection_id, green_time, red_time)
            self.adjacency_list[intersection_id] = []

    def connect(self, id1: str, id2: str, bidirectional: bool = True):
        """Define rutas válidas (conexiones) entre recursos de la red."""
        if id1 in self.nodes and id2 in self.nodes:
            if id2 not in self.adjacency_list[id1]:
                self.adjacency_list[id1].append(id2)
            if bidirectional and id1 not in self.adjacency_list[id2]:
                self.adjacency_list[id2].append(id1)

    def get_neighbors(self, intersection_id: str) -> list[Intersection]:
        """Obtiene las intersecciones adyacentes a un nodo dado."""
        if intersection_id in self.adjacency_list:
            return [self.nodes[n_id] for n_id in self.adjacency_list[intersection_id]]
        return []

    def get_all(self) -> list[Intersection]:
        """Retorna todos los recursos (nodos) de la red."""
        return list(self.nodes.values())
