import threading
import random
import time
from typing import Callable

import config
from simulation.network import IntersectionNetwork


class FaultHandler:
    """
    Simula fallos aleatorios en semáforos (interrupciones del sistema operativo).
    
    --- Concepto de SO: Interrupciones ---
    Este handler emula el comportamiento de una interrupción de hardware/software.
    Cuando ocurre un fallo (interrupción), el semáforo deja de funcionar normalmente
    y el sistema debe manejar la situación (en este caso, auto-recuperación).
    
    Los callbacks on_fault y on_restore permiten notificar al frontend via WebSocket.
    """
    
    def __init__(self, network: IntersectionNetwork, on_fault: Callable, on_restore: Callable):
        """
        Args:
            network: Instancia de TrafficNetwork con las intersecciones
            on_fault: callback(intersection_id) llamado cuando ocurre un fallo
            on_restore: callback(intersection_id) llamado cuando se recupera
        """
        self.network = network
        self.on_fault = on_fault
        self.on_restore = on_restore
        self._running = False
        self._thread = None

    def start(self):
        """Inicia el thread demonio que genera fallos aleatorios."""
        self._running = True
        self._thread = threading.Thread(target=self._fault_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Detiene el handler de fallos."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _fault_loop(self):
        """Loop principal que genera fallos en intervalos aleatorios."""
        while self._running:
            # Esperar intervalo aleatorio entre FAULT_MIN_INTERVAL y FAULT_MAX_INTERVAL
            sleep_time = random.uniform(config.FAULT_MIN_INTERVAL, config.FAULT_MAX_INTERVAL)
            time.sleep(sleep_time)
            
            if not self._running:
                break

            # Elegir una intersección aleatoria para fallar
            nodes = list(self.network.nodes.values())
            if not nodes:
                continue

            intersection = random.choice(nodes)
            intersection.light.trigger_fault()

            # Notificar fault (el callback hace broadcast via WebSocket)
            self.on_fault(intersection.id)

            # Auto-recuperación después de FAULT_RECOVERY_TIME segundos
            time.sleep(config.FAULT_RECOVERY_TIME)
            intersection.light.restore()
            self.on_restore(intersection.id)