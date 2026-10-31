"""
search_planner.py
=================
Implementation of Classical Heuristic & Optimal State-Space Graph Search Algorithms:
- A* Search (f(n) = g(n) + h(n))
- Greedy Best-First Search (f(n) = h(n))
- Dijkstra's Algorithm (f(n) = g(n))

Directly maps to AI Lab Syllabus:
- Practical 3: Shortest Path Using Greedy Best-First Search
- Practical 4: Optimal Path Using A* Search
- Practical 9: State-Space Search Planning (Forward Search)
"""

import math
import heapq
from typing import Dict, List, Tuple, Optional, Any
from data.hospital_network import HOSPITAL_NODES, get_network_graph

def euclidean_distance(node_a: str, node_b: str) -> float:
    """Calculates straight-line Euclidean distance heuristic h(n) in kilometers."""
    pos_a = (HOSPITAL_NODES[node_a]["x"], HOSPITAL_NODES[node_a]["y"])
    pos_b = (HOSPITAL_NODES[node_b]["x"], HOSPITAL_NODES[node_b]["y"])
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.hypot(dx, dy)

def manhattan_distance(node_a: str, node_b: str) -> float:
    """Calculates L1 Manhattan distance heuristic h(n) in kilometers."""
    pos_a = (HOSPITAL_NODES[node_a]["x"], HOSPITAL_NODES[node_a]["y"])
    pos_b = (HOSPITAL_NODES[node_b]["x"], HOSPITAL_NODES[node_b]["y"])
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

def heuristic_time_cost(node: str, goal: str, heuristic_type: str = "euclidean", assumed_max_speed_kmh: float = 60.0) -> float:
    """
    Computes an admissible heuristic h(n) in units of travel time (minutes).
    Admissibility condition: h(n) <= h*(n) [never overestimates true cost to goal].
    Dividing straight-line distance by the maximum possible theoretical speed ensures admissibility.
    """
    if heuristic_type == "manhattan":
        dist = manhattan_distance(node, goal)
    else:
        dist = euclidean_distance(node, goal)
    
    # Convert distance to lower-bound minutes at max emergency speed
    return round((dist / assumed_max_speed_kmh) * 60.0, 2)


def a_star_search(
    start: str,
    goal: str,
    graph: Dict[str, Dict[str, float]],
    heuristic_type: str = "euclidean"
) -> Dict[str, Any]:
    """
    Executes A* Search: f(n) = g(n) + h(n).
    Guarantees shortest path if heuristic h(n) is admissible and consistent.
    """
    # Priority Queue elements: (f_score, counter, current_node)
    counter = 0
    start_h = heuristic_time_cost(start, goal, heuristic_type)
    pq = [(start_h, counter, start)]
    
    g_score: Dict[str, float] = {node: float('inf') for node in graph}
    g_score[start] = 0.0
    
    f_score: Dict[str, float] = {node: float('inf') for node in graph}
    f_score[start] = start_h
    
    parent: Dict[str, Optional[str]] = {start: None}
    visited_order: List[Dict[str, Any]] = []
    closed_set = set()
    peak_frontier = 1

    while pq:
        current_f, _, current = heapq.heappop(pq)
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        h_val = heuristic_time_cost(current, goal, heuristic_type)
        g_val = g_score[current]
        
        visited_order.append({
            "step": len(visited_order) + 1,
            "node": current,
            "display_name": HOSPITAL_NODES[current]["name"],
            "g": round(g_val, 2),
            "h": round(h_val, 2),
            "f": round(current_f, 2),
            "explanation": f"Evaluated {HOSPITAL_NODES[current]['name']} with f(n) = g({g_val:.1f}m) + h({h_val:.1f}m) = {current_f:.1f}m"
        })
        
        if current == goal:
            # Reconstruct path
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            return {
                "algorithm": "A* Search",
                "success": True,
                "path": path,
                "total_cost_minutes": round(g_score[goal], 2),
                "nodes_expanded": len(visited_order),
                "peak_frontier_size": peak_frontier,
                "visited_order": visited_order,
                "closed_set": list(closed_set),
                "optimality": "Guaranteed Optimal (f = g + h, admissible heuristic)"
            }
        
        for neighbor, weight in graph[current].items():
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                h_n = heuristic_time_cost(neighbor, goal, heuristic_type)
                f_n = tentative_g + h_n
                f_score[neighbor] = f_n
                
                counter += 1
                heapq.heappush(pq, (f_n, counter, neighbor))
                peak_frontier = max(peak_frontier, len(pq))
                
    return {
        "algorithm": "A* Search",
        "success": False,
        "path": [],
        "total_cost_minutes": 0.0,
        "nodes_expanded": len(visited_order),
        "peak_frontier_size": peak_frontier,
        "visited_order": visited_order,
        "closed_set": list(closed_set),
        "optimality": "No Path Found (Network Disconnected)"
    }


def greedy_best_first_search(
    start: str,
    goal: str,
    graph: Dict[str, Dict[str, float]],
    heuristic_type: str = "euclidean"
) -> Dict[str, Any]:
    """
    Executes Greedy Best-First Search: f(n) = h(n).
    Always expands the node that appears closest to the goal according to heuristic.
    Does NOT guarantee an optimal shortest path because it ignores accumulated cost g(n).
    """
    counter = 0
    start_h = heuristic_time_cost(start, goal, heuristic_type)
    pq = [(start_h, counter, start)]
    
    parent: Dict[str, Optional[str]] = {start: None}
    visited_order: List[Dict[str, Any]] = []
    closed_set = set()
    peak_frontier = 1

    # Keep track of actual g_score along the chosen greedy tree
    g_score: Dict[str, float] = {node: float('inf') for node in graph}
    g_score[start] = 0.0

    while pq:
        current_h, _, current = heapq.heappop(pq)
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        g_val = g_score[current]
        
        visited_order.append({
            "step": len(visited_order) + 1,
            "node": current,
            "display_name": HOSPITAL_NODES[current]["name"],
            "g": round(g_val, 2),
            "h": round(current_h, 2),
            "f": round(current_h, 2),
            "explanation": f"Greedy choice: {HOSPITAL_NODES[current]['name']} based solely on h(n) = {current_h:.1f}m"
        })
        
        if current == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            return {
                "algorithm": "Greedy Best-First Search",
                "success": True,
                "path": path,
                "total_cost_minutes": round(g_score[goal], 2),
                "nodes_expanded": len(visited_order),
                "peak_frontier_size": peak_frontier,
                "visited_order": visited_order,
                "closed_set": list(closed_set),
                "optimality": "Suboptimal / Heuristic-driven (f = h only, ignores path cost g)"
            }
        
        for neighbor, weight in graph[current].items():
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + weight
            if neighbor not in parent or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                h_n = heuristic_time_cost(neighbor, goal, heuristic_type)
                
                counter += 1
                heapq.heappush(pq, (h_n, counter, neighbor))
                peak_frontier = max(peak_frontier, len(pq))

    return {
        "algorithm": "Greedy Best-First Search",
        "success": False,
        "path": [],
        "total_cost_minutes": 0.0,
        "nodes_expanded": len(visited_order),
        "peak_frontier_size": peak_frontier,
        "visited_order": visited_order,
        "closed_set": list(closed_set),
        "optimality": "No Path Found"
    }


def dijkstra_search(
    start: str,
    goal: str,
    graph: Dict[str, Dict[str, float]]
) -> Dict[str, Any]:
    """
    Executes Dijkstra's Uniform Cost Search: f(n) = g(n), h(n) = 0.
    Guarantees optimal path but explores blindly in concentric circles.
    """
    counter = 0
    pq = [(0.0, counter, start)]
    
    g_score: Dict[str, float] = {node: float('inf') for node in graph}
    g_score[start] = 0.0
    
    parent: Dict[str, Optional[str]] = {start: None}
    visited_order: List[Dict[str, Any]] = []
    closed_set = set()
    peak_frontier = 1

    while pq:
        current_g, _, current = heapq.heappop(pq)
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        
        visited_order.append({
            "step": len(visited_order) + 1,
            "node": current,
            "display_name": HOSPITAL_NODES[current]["name"],
            "g": round(current_g, 2),
            "h": 0.0,
            "f": round(current_g, 2),
            "explanation": f"Dijkstra evaluated {HOSPITAL_NODES[current]['name']} with g(n) = {current_g:.1f}m (uninformed)"
        })
        
        if current == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            return {
                "algorithm": "Dijkstra (Uniform Cost Search)",
                "success": True,
                "path": path,
                "total_cost_minutes": round(g_score[goal], 2),
                "nodes_expanded": len(visited_order),
                "peak_frontier_size": peak_frontier,
                "visited_order": visited_order,
                "closed_set": list(closed_set),
                "optimality": "Guaranteed Optimal (f = g only, zero heuristic)"
            }
            
        for neighbor, weight in graph[current].items():
            if neighbor in closed_set:
                continue
                
            tentative_g = current_g + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                counter += 1
                heapq.heappush(pq, (tentative_g, counter, neighbor))
                peak_frontier = max(peak_frontier, len(pq))

    return {
        "algorithm": "Dijkstra",
        "success": False,
        "path": [],
        "total_cost_minutes": 0.0,
        "nodes_expanded": len(visited_order),
        "peak_frontier_size": peak_frontier,
        "visited_order": visited_order,
        "closed_set": list(closed_set),
        "optimality": "No Path Found"
    }


def compare_search_algorithms(
    start: str,
    goal: str,
    traffic_multiplier: float = 1.0,
    blocked_edges: List[Tuple[str, str]] = None,
    heuristic_type: str = "euclidean"
) -> Dict[str, Any]:
    """
    Executes A*, Greedy Best-First, and Dijkstra simultaneously on the same network
    to produce comprehensive benchmark metrics.
    """
    graph = get_network_graph(traffic_multiplier=traffic_multiplier, blocked_edges=blocked_edges)
    
    a_star_res = a_star_search(start, goal, graph, heuristic_type=heuristic_type)
    greedy_res = greedy_best_first_search(start, goal, graph, heuristic_type=heuristic_type)
    dijkstra_res = dijkstra_search(start, goal, graph)
    
    return {
        "start": start,
        "goal": goal,
        "traffic_multiplier": traffic_multiplier,
        "blocked_edges": blocked_edges or [],
        "heuristic_type": heuristic_type,
        "results": {
            "A* Search": a_star_res,
            "Greedy Best-First": greedy_res,
            "Dijkstra": dijkstra_res
        }
    }
