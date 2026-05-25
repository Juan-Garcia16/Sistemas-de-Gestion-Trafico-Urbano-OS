import threading
import time
import random
import queue as queue_module
from config import TRAFFIC_LIGHT_YELLOW_DURATION, VEHICLE_SPAWN_INTERVAL, VEHICLE_MAX_FLEET, VEHICLE_MAX_LIFETIME, MAX_DISPATCH_PER_INTERSECTION_PER_TICK
from simulation.network import IntersectionNetwork
from core.scheduler import TrafficScheduler
from core.vehicle import Vehicle, Priority

class SimulationEngine:
    """
    Motor central de simulación.

    --- Concepto de SO: Main Kernel Loop / Hardware Clock ---
    Actúa de modo equivalente al 'Tick' de reloj de hardware que genera interrupciones
    periódicas. Este Motor es el núcleo (Kernel) que despierta en cada tick temporal
    para coordinar los recursos físicos (semáforos) y ceder el control al
    planificador (Scheduler) en el momento índice.
    """
    def __init__(self, network: IntersectionNetwork, scheduler: TrafficScheduler, broadcast_func=None):
        self.network = network
        self.scheduler = scheduler

        self._stop_event = threading.Event()
        self._tick_thread = None

        # --- Concepto de SO: Tabla de Procesos (Process Table) ---
        self.active_vehicles: dict[str, Vehicle] = {}

        self._light_timers = {node.id: 0 for node in self.network.get_all()}
        self._broadcast_func = broadcast_func

        self._tick_count = 0
        self._vehicle_counter = 0

        # --- Concepto de SO: Spawn de procesos (kernel fork) ---
        self._spawn_interval = VEHICLE_SPAWN_INTERVAL
        self._spawn_timer = 0
        self._max_vehicles = VEHICLE_MAX_FLEET
        self._edge_nodes = self._compute_edge_nodes()

    def _compute_edge_nodes(self):
        corners = ["intersection_0_0", "intersection_0_2", "intersection_2_0", "intersection_2_2"]
        edges = ["intersection_0_1", "intersection_1_0", "intersection_1_2", "intersection_2_1"]
        return corners + edges

    def start(self):
        if self._tick_thread is None or not self._tick_thread.is_alive():
            self._stop_event.clear()
            self._tick_thread = threading.Thread(target=self._loop, daemon=True)
            self._tick_thread.start()

    def stop(self):
        self._stop_event.set()
        if self._tick_thread:
            self._tick_thread.join(timeout=2.0)

    def _spawn_vehicle(self):
        if len(self.active_vehicles) >= self._max_vehicles:
            return

        start = random.choice(self._edge_nodes)
        vid = f"veh-{self._vehicle_counter}"
        self._vehicle_counter += 1

        priority = random.choices([Priority.NORMAL, Priority.HIGH], weights=[80, 20])[0]

        vehicle = Vehicle(vid, start, self.network, priority, self.scheduler)
        self.active_vehicles[vid] = vehicle
        vehicle.start()

    def _loop(self):
        while not self._stop_event.is_set():
            self._tick_count += 1
            self.scheduler._current_tick = self._tick_count
            self.scheduler._dispatched_this_tick.clear()
            dispatched_this_tick = set()

            for inter in self.network.get_all():
                light = inter.light

                with light._lock:
                    if light.state == "FAULT":
                        q = self.scheduler._queues.get(inter.id)
                        q_size = q.qsize() if q else 0
                        
                        dispatched_this_tick.add(inter.id)
                        if q_size > 0:
                            self.scheduler.dispatch_next(inter.id)
                        continue

                    self._light_timers[inter.id] += 1
                    timer = self._light_timers[inter.id]

                    current_red_time = light.red_time

                    if light.state == "RED" and timer >= current_red_time:
                        light.state = "GREEN"
                        self._light_timers[inter.id] = 0
                        if inter.id not in dispatched_this_tick:
                            q = self.scheduler._queues.get(inter.id)
                            q_size = q.qsize() if q else 0
                            
                            self.scheduler.dispatch_next(inter.id)
                            dispatched_this_tick.add(inter.id)
                            if q_size > 1:
                                for _ in range(q_size - 1):
                                    self.scheduler.dispatch_next(inter.id)

                    elif light.state == "YELLOW" and timer >= TRAFFIC_LIGHT_YELLOW_DURATION:
                        light.state = "RED"
                        self._light_timers[inter.id] = 0

                    elif light.state == "GREEN" and timer >= light.green_time:
                        light.state = "YELLOW"
                        self._light_timers[inter.id] = 0

                    elif light.state == "GREEN" and inter.id not in dispatched_this_tick:
                        q = self.scheduler._queues.get(inter.id)
                        q_size = q.qsize() if q else 0
                        
                        self.scheduler.dispatch_next(inter.id)
                        dispatched_this_tick.add(inter.id)
                        if q_size > 1:
                            for _ in range(q_size - 1):
                                self.scheduler.dispatch_next(inter.id)

            self._spawn_timer += 1
            if self._spawn_timer >= self._spawn_interval:
                self._spawn_timer = 0
                self._spawn_vehicle()

            if self._broadcast_func:
                snapshot = self.state_snapshot()
                state = {
                    "type": "STATE_UPDATE",
                    "intersections": snapshot.get("intersections", []),
                    "vehicles": snapshot.get("vehicles", []),
                    "alerts": [],
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                try:
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._broadcast_func(state))
                    loop.close()
                except Exception:
                    pass

            time.sleep(1.0)

    def add_vehicle(self, vehicle_id: str, start_intersection: str, priority: Priority, route_path: list[str] | None = None):
        vehicle = Vehicle(vehicle_id, start_intersection, self.network, priority, self.scheduler, route_path)
        self.active_vehicles[vehicle_id] = vehicle
        vehicle.start()

    def state_snapshot(self) -> dict:
        def _coords(inter_id: str) -> dict:
            parts = inter_id.split("_")
            return {"x": int(parts[1]), "y": int(parts[2])}

        queue_vehicles = {}
        for inter in self.network.get_all():
            queue_vehicles[inter.id] = []

        for v_id, v in self.active_vehicles.items():
            if v.status == "WAITING" and v.queued_at:
                q_list = queue_vehicles.get(v.queued_at)
                if q_list is not None:
                    q_list.append(v_id)

        intersections_state = []
        for inter in self.network.get_all():
            mutex_owner = None
            for v_id, v in self.active_vehicles.items():
                if v.status == "MOVING" and v.current_intersection == inter.id:
                    mutex_owner = v_id
                    break

            intersections_state.append({
                "id": inter.id,
                "state": inter.light.state,
                "position": _coords(inter.id),
                "queue_size": len(queue_vehicles.get(inter.id, [])),
                "queued_vehicles": queue_vehicles.get(inter.id, []),
                "mutex_owner": mutex_owner,
                "mutex_locked": mutex_owner is not None
            })

        vehicles_state = []
        done_vehicles = []
        for v_id, v in list(self.active_vehicles.items()):
            if v.status == "DONE":
                done_vehicles.append(v_id)
                continue
            vehicles_state.append({
                "id": v.vehicle_id,
                "status": v.status,
                "position": _coords(v.current_intersection),
                "priority": v.priority.name,
                "current_intersection": v.current_intersection,
                "visited": getattr(v, '_visited_count', 0),
                "route": getattr(v, 'route_path', None)
            })

        for v_id in done_vehicles:
            self.active_vehicles.pop(v_id, None)

        return {
            "intersections": intersections_state,
            "vehicles": vehicles_state,
            "tick": self._tick_count
        }