"""
visualizers.py
==============
Interactive Plotly visualizations for VitalFlow AI:
- Spatial Transit Network & Pathfinding Graph
- ICU Telemetry Multi-Parameter Strip Chart
- CSP Min-Conflicts Convergence Curve
- Partial Order Planning Task Execution Stages
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Tuple
from data.hospital_network import HOSPITAL_NODES, ROAD_EDGES

def plot_hospital_network(
    a_star_path: List[str] = None,
    greedy_path: List[str] = None,
    blocked_edges: List[Tuple[str, str]] = None
) -> go.Figure:
    """
    Renders an interactive topological graph of the Nagpur Healthcare Transit Network.
    Highlights A* optimal path vs Greedy Best-First heuristic path.
    """
    if a_star_path is None:
        a_star_path = []
    if greedy_path is None:
        greedy_path = []
    if blocked_edges is None:
        blocked_edges = []

    blocked_set = set(blocked_edges) | set((v, u) for u, v in blocked_edges)

    fig = go.Figure()

    # 1. Plot Base Road Segments
    for u, v, dist, speed in ROAD_EDGES:
        x0, y0 = HOSPITAL_NODES[u]["x"], HOSPITAL_NODES[u]["y"]
        x1, y1 = HOSPITAL_NODES[v]["x"], HOSPITAL_NODES[v]["y"]

        is_blocked = (u, v) in blocked_set
        line_color = "#ef4444" if is_blocked else "#cbd5e1"
        line_width = 3 if is_blocked else 1.8
        dash_style = "dot" if is_blocked else "solid"

        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(color=line_color, width=line_width, dash=dash_style),
            hoverinfo="text",
            text=f"Road: {u} ↔ {v}<br>Dist: {dist} km | Base Speed: {speed} km/h{' (ROAD CLOSED)' if is_blocked else ''}",
            showlegend=False
        ))

    # 2. Plot Greedy Path (if present)
    if len(greedy_path) > 1:
        gx, gy = [], []
        for node in greedy_path:
            gx.append(HOSPITAL_NODES[node]["x"])
            gy.append(HOSPITAL_NODES[node]["y"])
        fig.add_trace(go.Scatter(
            x=gx,
            y=gy,
            mode="lines+markers",
            line=dict(color="#f59e0b", width=4, dash="dash"),
            marker=dict(size=8, color="#f59e0b"),
            name="Greedy Best-First Route (f=h)",
            hoverinfo="name"
        ))

    # 3. Plot A* Path (if present)
    if len(a_star_path) > 1:
        ax, ay = [], []
        for node in a_star_path:
            ax.append(HOSPITAL_NODES[node]["x"])
            ay.append(HOSPITAL_NODES[node]["y"])
        fig.add_trace(go.Scatter(
            x=ax,
            y=ay,
            mode="lines+markers",
            line=dict(color="#10b981", width=5),
            marker=dict(size=10, color="#059669", symbol="circle"),
            name="A* Optimal Route (f=g+h)",
            hoverinfo="name"
        ))

    # 4. Plot Hospital Nodes
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for k, v in HOSPITAL_NODES.items():
        node_x.append(v["x"])
        node_y.append(v["y"])
        
        # Color coding by category
        if "AIIMS" in k or "GMC" in k:
            color = "#dc2626"  # Apex Apex
            size = 18
        elif v.get("trauma_ready", False):
            color = "#2563eb"  # Trauma Ready
            size = 14
        else:
            color = "#64748b"  # Transit outpost
            size = 11

        node_color.append(color)
        node_size.append(size)
        node_text.append(
            f"<b>{v['name']}</b><br>"
            f"Type: {v['type']}<br>"
            f"ICU Beds: {v['icu_beds']}<br>"
            f"Trauma Ready: {'Yes' if v['trauma_ready'] else 'No'}<br>"
            f"Grid Coord: ({v['x']}, {v['y']})"
        )

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color="#ffffff")
        ),
        text=[k for k in HOSPITAL_NODES.keys()],
        textposition="top center",
        textfont=dict(size=10, color="#1e293b", family="Plus Jakarta Sans"),
        hoverinfo="text",
        hovertext=node_text,
        name="Medical Facilities & Intersections"
    ))

    fig.update_layout(
        title="Nagpur Urban Healthcare Transit Network Topology",
        title_font=dict(size=15, color="#0f172a"),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e2e8f0", zeroline=True, zerolinecolor="#94a3b8", title="East-West Displacement (km)"),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", zeroline=True, zerolinecolor="#94a3b8", title="North-South Displacement (km)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520
    )

    return fig


def plot_patient_telemetry(timesteps: List[Dict[str, Any]], patient_name: str) -> go.Figure:
    """
    Renders a clinical multi-parameter telemetry strip chart showing HR, BP, SpO2, and Shock Index trends.
    """
    times = [t["time"] for t in timesteps]
    hr = [t["hr"] for t in timesteps]
    sys_bp = [t["sys_bp"] for t in timesteps]
    dia_bp = [t["dia_bp"] for t in timesteps]
    spo2 = [t["spo2"] for t in timesteps]
    shock_index = [round(t["hr"] / max(t["sys_bp"], 1), 2) for t in timesteps]

    fig = go.Figure()

    # Heart Rate trace
    fig.add_trace(go.Scatter(
        x=times, y=hr,
        name="Heart Rate (bpm)",
        mode="lines+markers",
        line=dict(color="#ef4444", width=3),
        marker=dict(size=7)
    ))

    # Blood Pressure traces
    fig.add_trace(go.Scatter(
        x=times, y=sys_bp,
        name="Systolic BP (mmHg)",
        mode="lines+markers",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=times, y=dia_bp,
        name="Diastolic BP (mmHg)",
        mode="lines",
        line=dict(color="#93c5fd", width=1.8, dash="dot")
    ))

    # SpO2 trace
    fig.add_trace(go.Scatter(
        x=times, y=spo2,
        name="SpO2 Saturation (%)",
        mode="lines+markers",
        line=dict(color="#10b981", width=3),
        marker=dict(size=7)
    ))

    # Shock Index trace (Secondary axis or scaled)
    fig.add_trace(go.Scatter(
        x=times, y=[si * 100 for si in shock_index],
        name="Shock Index (x100)",
        mode="lines+markers",
        line=dict(color="#8b5cf6", width=2, dash="dash"),
        marker=dict(size=6),
        hovertext=[f"Shock Index: {si}" for si in shock_index]
    ))

    # Danger Zones / Reference threshold lines
    fig.add_hline(y=100, line_dash="dot", line_color="rgba(239, 68, 68, 0.4)", annotation_text="Tachycardia Threshold (100 bpm)")
    fig.add_hline(y=90, line_dash="dot", line_color="rgba(16, 185, 129, 0.4)", annotation_text="Hypoxia Warning (90% SpO2)")

    fig.update_layout(
        title=f"Continuous Physiological Telemetry Stream: {patient_name}",
        title_font=dict(size=14, color="#0f172a"),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(title="Time Inspection Window", gridcolor="#e2e8f0"),
        yaxis=dict(title="Physiological Amplitude / Scale", gridcolor="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380
    )

    return fig


def plot_csp_convergence(history: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders the Min-Conflicts local search optimization trajectory.
    Visualizes how the algorithm drives total constraint violations down to zero.
    """
    steps = [h["step"] for h in history]
    conflicts = [h["conflicts"] for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=steps,
        y=conflicts,
        mode="lines+markers",
        line=dict(color="#6366f1", width=3),
        marker=dict(size=6, color="#4338ca"),
        name="Active Constraint Violations",
        fill="tozeroy",
        fillcolor="rgba(99, 102, 241, 0.1)"
    ))

    fig.update_layout(
        title="Min-Conflicts Local Search: Constraint Violation Reduction Trajectory",
        title_font=dict(size=14, color="#0f172a"),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Iteration / Evaluation Step", gridcolor="#e2e8f0"),
        yaxis=dict(title="Total Active Conflicts", gridcolor="#e2e8f0", dtick=1),
        height=320
    )

    return fig


def plot_partial_order_plan(tiers: List[List[Dict[str, Any]]]) -> go.Figure:
    """
    Renders an interactive Gantt / Phase execution chart for Partial Order Planning.
    Demonstrates how parallel medical steps execute concurrently.
    """
    tasks = []
    start_time = 0

    for tier_idx, tier in enumerate(tiers):
        tier_duration = max(t["duration_min"] for t in tier)
        for task in tier:
            tasks.append({
                "Task": task["name"],
                "Team": task["team"],
                "Tier": f"Stage {tier_idx+1}",
                "Start": start_time,
                "Duration": task["duration_min"],
                "Finish": start_time + task["duration_min"]
            })
        start_time += tier_duration

    fig = go.Figure()

    team_colors = {
        "Triage Nursing": "#3b82f6",
        "Resus Nurse Alpha": "#06b6d4",
        "Blood Bank Tech": "#ec4899",
        "Anesthesiologist": "#8b5cf6",
        "Scrub Nurse": "#10b981",
        "Surgical Assistant": "#f59e0b",
        "Trauma Surgeon": "#ef4444",
        "SICU Transport Team": "#64748b"
    }

    for t in tasks:
        color = team_colors.get(t["Team"], "#6366f1")
        fig.add_trace(go.Bar(
            y=[t["Task"]],
            x=[t["Duration"]],
            base=[t["Start"]],
            orientation="h",
            name=t["Team"],
            marker=dict(color=color, line=dict(color="#ffffff", width=1.5)),
            hovertext=f"Task: {t['Task']}<br>Assigned Team: {t['Team']}<br>Execution: {t['Start']}m - {t['Finish']}m ({t['Duration']} min)<br>Phase: {t['Tier']}",
            hoverinfo="text",
            showlegend=False
        ))

    fig.update_layout(
        title="Partial Order Plan: Multi-Team Parallel Trauma Resuscitation Timeline",
        title_font=dict(size=14, color="#0f172a"),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Elapsed Resuscitation Timeline (Minutes from Arrival)", gridcolor="#e2e8f0"),
        yaxis=dict(title="", autorange="reversed", gridcolor="#e2e8f0"),
        height=380
    )

    return fig
