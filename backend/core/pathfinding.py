from collections import deque

def plan_route(start: str, end: str, network) -> list[str]:
    """
    BFS simple para encontrar la ruta más corta entre dos intersecciones.
    
    --- Concepto de SO: Pathfinding como algoritmo de planificación ---
    En un sistema operativo real, un proceso necesita conocer la ruta óptima
    para acceder a recursos. Aquí usamos BFS (Breadth-First Search) que
    garantiza encontrar el camino más corto en grafos sin peso.
    
    Args:
        start: ID de la intersección inicial
        end: ID de la intersección destino
        network: IntersectionNetwork con la topología del sistema
    
    Returns:
        Lista de IDs de intersección desde start hasta end (inclusive).
        Retorna lista vacía si no hay ruta disponible.
    """
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        current, path = queue.popleft()
        
        neighbors = network.get_neighbors(current)
        for neighbor in neighbors:
            neighbor_id = neighbor.id
            
            if neighbor_id == end:
                return path + [neighbor_id]
            
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))
    
    return []