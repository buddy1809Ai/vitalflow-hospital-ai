"""
hospital_network.py
===================
Nagpur Urban Healthcare & Emergency Transit Network Graph.
Provides spatial coordinates, edge distances, dynamic traffic multipliers,
and hospital facility metadata for routing algorithms (A*, Greedy Best-First, Dijkstra).
"""

from typing import Dict, List, Tuple, Any

# Node specifications: name -> (x, y, display_name, node_type, beds_available)
# Coordinates scaled in an intuitive Cartesian grid (km scale relative to Nagpur Zero Mile)
HOSPITAL_NODES: Dict[str, Dict[str, Any]] = {
    "Sitabuldi": {
        "x": 0.0,
        "y": 0.0,
        "name": "Sitabuldi Central Junction",
        "type": "Transit Hub & Quick Response Outpost",
        "icu_beds": 8,
        "trauma_ready": True
    },
    "Dharampeth": {
        "x": -2.2,
        "y": 0.8,
        "name": "Dharampeth Health Clinic Cluster",
        "type": "Primary / Secondary Care",
        "icu_beds": 12,
        "trauma_ready": False
    },
    "Ramdaspeth": {
        "x": -1.2,
        "y": -1.4,
        "name": "Ramdaspeth Multi-Specialty Hub (Care Hospital)",
        "type": "Private Tertiary Hospital",
        "icu_beds": 34,
        "trauma_ready": True
    },
    "Dhantoli": {
        "x": 0.4,
        "y": -1.8,
        "name": "Dhantoli Critical Care Zone",
        "type": "Super Specialty Trauma",
        "icu_beds": 28,
        "trauma_ready": True
    },
    "GMC_Nagpur": {
        "x": 1.5,
        "y": -2.6,
        "name": "GMC Nagpur (Govt. Medical College & Hospital)",
        "type": "Level-1 Trauma Apex Hospital",
        "icu_beds": 65,
        "trauma_ready": True
    },
    "Medical_Square": {
        "x": 2.0,
        "y": -1.9,
        "name": "Super Specialty Hospital (SSH) Square",
        "type": "Tertiary Referral Center",
        "icu_beds": 42,
        "trauma_ready": True
    },
    "Chhatrapati_Sq": {
        "x": -1.0,
        "y": -4.2,
        "name": "Chhatrapati Square Outpost",
        "type": "Highway Emergency Outpost",
        "icu_beds": 6,
        "trauma_ready": False
    },
    "Wardha_Road": {
        "x": 0.2,
        "y": -5.5,
        "name": "Wardha Road Arterial Link",
        "type": "Arterial Corridor",
        "icu_beds": 0,
        "trauma_ready": False
    },
    "Airport_Metro": {
        "x": 0.5,
        "y": -7.5,
        "name": "Dr. Babasaheb Ambedkar Airport Station Link",
        "type": "Rapid Transit Node",
        "icu_beds": 10,
        "trauma_ready": False
    },
    "New_Khapri": {
        "x": 0.8,
        "y": -9.8,
        "name": "New Khapri Junction",
        "type": "Suburban Transit Node",
        "icu_beds": 4,
        "trauma_ready": False
    },
    "MIHAN": {
        "x": 1.4,
        "y": -12.2,
        "name": "MIHAN Health City Hub",
        "type": "Specialized Healthcare SEZ",
        "icu_beds": 40,
        "trauma_ready": True
    },
    "AIIMS_Nagpur": {
        "x": 2.5,
        "y": -13.8,
        "name": "AIIMS Nagpur (Apex Institute)",
        "type": "National Apex Medical Institute",
        "icu_beds": 90,
        "trauma_ready": True
    },
    "Alexis_Mankapur": {
        "x": -0.8,
        "y": 4.5,
        "name": "Alexis / Max Hospital (Mankapur)",
        "type": "North Zone Multi-Specialty",
        "icu_beds": 32,
        "trauma_ready": True
    },
    "Sadkar_Trauma": {
        "x": 2.2,
        "y": 3.8,
        "name": "Kamptee Road Emergency Outpost",
        "type": "Emergency First-Response Bay",
        "icu_beds": 14,
        "trauma_ready": False
    }
}

# Bidirectional Road Segments: (nodeA, nodeB, physical_distance_km, base_speed_kmh)
ROAD_EDGES: List[Tuple[str, str, float, float]] = [
    ("Sitabuldi", "Dharampeth", 2.6, 40.0),
    ("Sitabuldi", "Ramdaspeth", 2.0, 35.0),
    ("Sitabuldi", "Dhantoli", 1.9, 30.0),
    ("Sitabuldi", "Sadkar_Trauma", 4.5, 45.0),
    ("Sitabuldi", "Alexis_Mankapur", 4.8, 42.0),
    ("Dharampeth", "Ramdaspeth", 2.4, 38.0),
    ("Ramdaspeth", "Dhantoli", 1.6, 30.0),
    ("Ramdaspeth", "Chhatrapati_Sq", 3.2, 45.0),
    ("Dhantoli", "GMC_Nagpur", 1.8, 32.0),
    ("Dhantoli", "Medical_Square", 2.1, 35.0),
    ("GMC_Nagpur", "Medical_Square", 1.1, 28.0),
    ("GMC_Nagpur", "Wardha_Road", 3.4, 40.0),
    ("Chhatrapati_Sq", "Wardha_Road", 1.9, 48.0),
    ("Wardha_Road", "Airport_Metro", 2.3, 50.0),
    ("Airport_Metro", "New_Khapri", 2.7, 55.0),
    ("New_Khapri", "MIHAN", 2.8, 55.0),
    ("MIHAN", "AIIMS_Nagpur", 2.2, 60.0),
    ("Medical_Square", "Wardha_Road", 3.8, 38.0),
    ("Alexis_Mankapur", "Sadkar_Trauma", 3.2, 40.0),
    # Urban Arterial Bypass Corridors (Nagpur Outer Ring Road & Manish Nagar Link)
    ("Chhatrapati_Sq", "Airport_Metro", 3.1, 42.0),    # Manish Nagar - Airport Underpass
    ("Chhatrapati_Sq", "MIHAN", 6.8, 55.0),            # Outer Ring Road Expressway
    ("Medical_Square", "Airport_Metro", 4.4, 40.0)     # Somalwada Arterial Link
]

def get_network_graph(traffic_multiplier: float = 1.0, blocked_edges: List[Tuple[str, str]] = None) -> Dict[str, Dict[str, float]]:
    """
    Constructs an adjacency dictionary where weights represent travel time in minutes.
    Cost = (Distance / Effective_Speed) * 60
    """
    if blocked_edges is None:
        blocked_edges = []

    # Normalize blocked pairs for bidirectional lookup
    blocked_set = set()
    for u, v in blocked_edges:
        blocked_set.add((u, v))
        blocked_set.add((v, u))

    graph: Dict[str, Dict[str, float]] = {node: {} for node in HOSPITAL_NODES}

    for u, v, dist_km, speed_kmh in ROAD_EDGES:
        if (u, v) in blocked_set:
            continue
        
        effective_speed = max(10.0, speed_kmh / traffic_multiplier)
        time_minutes = round((dist_km / effective_speed) * 60.0, 2)

        graph[u][v] = time_minutes
        graph[v][u] = time_minutes

    return graph
