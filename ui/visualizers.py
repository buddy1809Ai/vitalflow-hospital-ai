"""
visualizers.py
==============
High-definition Plotly visualizers for VitalFlow AI.
Guaranteed high contrast, robust type handling, and crisp SaaS styling.
"""

import plotly.graph_objects as go
from typing import Dict, List, Any, Tuple
from data.hospital_network import HOSPITAL_NODES, ROAD_EDGES

def plot_hospital_network(
    a_star_path: List[str] = None,
    greedy_path: List[str] = None,
    blocked_edges: List[Tuple[str, str]] = None
) -> go.Figure:
    """
    Renders an interactive topological graph of Nagpur's Healthcare Transit Network.
    Visualizes A* optimal path vs Greedy Best-First heuristic path with road traffic states.
    """
    if a_star_path is None:
        a_star_path = []
    if greedy_path is None:
        greedy_path = []
    if blocked_edges is None:
        blocked_edges = []

    blocked_set = set(blocked_edges) | set((v, u) for u, v in blocked_edges)
    fig = go.Figure()

    # 1. Base Road Segments
    for u, v, dist, speed in ROAD_EDGES:
        x0, y0 = HOSPITAL_NODES[u]["x"], HOSPITAL_NODES[u]["y"]
        x1, y1 = HOSPITAL_NODES[v]["x"], HOSPITAL_NODES[v]["y"]

        is_blocked = (u, v) in blocked_set
        line_color = "#ef4444" if is_blocked else "#cbd5e1"
        line_width = 3.5 if is_blocked else 2.0
        dash_style = "dot" if is_blocked else "solid"

        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(color=line_color, width=line_width, dash=dash_style),
            hoverinfo="text",
            text=f"Road Link: {u} ↔ {v}<br>Distance: {dist} km | Speed Limit: {speed} km/h{' [ROAD BLOCKED]' if is_blocked else ''}",
            showlegend=False
        ))

    # 2. Greedy Best-First Path (Orange Dash)
    if len(greedy_path) > 1:
        gx, gy = [], []
        for node in greedy_path:
            gx.append(HOSPITAL_NODES[node]["x"])
            gy.append(HOSPITAL_NODES[node]["y"])
        fig.add_trace(go.Scatter(
            x=gx,
            y=gy,
            mode="lines+markers",
            line=dict(color="#f59e0b", width=3.5, dash="dash"),
            marker=dict(size=8, color="#d97706"),
            name="Greedy Best-First (f = h)",
            hoverinfo="name"
        ))

    # 3. A* Optimal Path (Emerald Solid)
    if len(a_star_path) > 1:
        ax, ay = [], []
        for node in a_star_path:
            ax.append(HOSPITAL_NODES[node]["x"])
            ay.append(HOSPITAL_NODES[node]["y"])
        fig.add_trace(go.Scatter(
            x=ax,
            y=ay,
            mode="lines+markers",
            line=dict(color="#059669", width=4.5),
            marker=dict(size=10, color="#047857", symbol="circle"),
            name="A* Optimal Route (f = g + h)",
            hoverinfo="name"
        ))

    # 4. Hospital & Transit Nodes
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for k, v in HOSPITAL_NODES.items():
        node_x.append(v["x"])
        node_y.append(v["y"])
        
        if "AIIMS" in k or "GMC" in k:
            color = "#dc2626"  # Apex Emergency Trauma Center
            size = 18
        elif v.get("trauma_ready", False):
            color = "#0284c7"  # Tertiary Care Center
            size = 14
        else:
            color = "#475569"  # Transit Node / Clinic
            size = 10

        node_color.append(color)
        node_size.append(size)
        node_text.append(
            f"<b>{v['name']}</b><br>"
            f"Type: {v['type']}<br>"
            f"ICU Bed Capacity: {v['icu_beds']}<br>"
            f"Trauma Facility: {'Yes' if v['trauma_ready'] else 'No'}<br>"
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
        textfont=dict(size=11, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        hoverinfo="text",
        hovertext=node_text,
        name="Hospitals & Junctions"
    ))

    fig.update_layout(
        title="Nagpur Healthcare Transit Topology & Dispatch Grid",
        title_font=dict(size=14, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, title="Displacement East-West (km)"),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, title="Displacement North-South (km)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#0f172a")),
        height=480
    )

    return fig


def plot_patient_telemetry(timesteps: List[Dict[str, Any]], patient_name: str) -> go.Figure:
    """
    Renders continuous physiological telemetry (HR, BP, SpO2) safely without TypeErrors.
    """
    if not timesteps:
        return go.Figure()

    times = [str(t.get("time", f"T{i+1}")) for i, t in enumerate(timesteps)]
    hr = [float(t.get("hr", 75)) for t in timesteps]
    sys_bp = [float(t.get("sys_bp", 120)) for t in timesteps]
    dia_bp = [float(t.get("dia_bp", 80)) for t in timesteps]
    spo2 = [float(t.get("spo2", 98)) for t in timesteps]

    fig = go.Figure()

    # Heart Rate
    fig.add_trace(go.Scatter(
        x=times, y=hr,
        name="Heart Rate (bpm)",
        mode="lines+markers",
        line=dict(color="#ef4444", width=2.5),
        marker=dict(size=6)
    ))

    # Systolic BP
    fig.add_trace(go.Scatter(
        x=times, y=sys_bp,
        name="Systolic BP (mmHg)",
        mode="lines+markers",
        line=dict(color="#0284c7", width=2.2),
        marker=dict(size=5)
    ))

    # Diastolic BP
    fig.add_trace(go.Scatter(
        x=times, y=dia_bp,
        name="Diastolic BP (mmHg)",
        mode="lines",
        line=dict(color="#94a3b8", width=1.5, dash="dot")
    ))

    # SpO2
    fig.add_trace(go.Scatter(
        x=times, y=spo2,
        name="SpO2 Saturation (%)",
        mode="lines+markers",
        line=dict(color="#10b981", width=2.5),
        marker=dict(size=6)
    ))

    # Reference threshold lines
    fig.add_hline(y=100, line_dash="dot", line_color="rgba(239, 68, 68, 0.4)", annotation_text="Tachycardia (100 bpm)", annotation_font_size=10)
    fig.add_hline(y=90, line_dash="dot", line_color="rgba(16, 185, 129, 0.4)", annotation_text="Hypoxia Warning (90% SpO2)", annotation_font_size=10)

    fig.update_layout(
        title=f"Continuous Physiological Telemetry: {patient_name}",
        title_font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(title="Time Inspection Interval", gridcolor="#f1f5f9"),
        yaxis=dict(title="Physiological Amplitude", gridcolor="#f1f5f9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#0f172a")),
        height=360
    )

    return fig


def plot_csp_convergence(history: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders the Min-Conflicts local search optimization trajectory.
    """
    if not history:
        return go.Figure()

    steps = [int(h.get("step", i)) for i, h in enumerate(history)]
    conflicts = [int(h.get("conflicts", 0)) for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=steps,
        y=conflicts,
        mode="lines+markers",
        line=dict(color="#0284c7", width=2.5),
        marker=dict(size=5, color="#0369a1"),
        fill="tozeroy",
        fillcolor="rgba(2, 132, 199, 0.08)",
        name="Active Violations"
    ))

    fig.update_layout(
        title="Min-Conflicts Optimization: Conflict Reduction Trajectory",
        title_font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Search Iteration Step", gridcolor="#f1f5f9"),
        yaxis=dict(title="Active Conflicts", gridcolor="#f1f5f9", dtick=1),
        height=300
    )

    return fig


def plot_partial_order_plan(tiers: List[List[Dict[str, Any]]]) -> go.Figure:
    """
    Renders an interactive Gantt timeline for Partial Order Planning.
    """
    if not tiers:
        return go.Figure()

    tasks = []
    start_time = 0

    for tier_idx, tier in enumerate(tiers):
        tier_duration = max((int(t.get("duration_min", 0)) for t in tier), default=0)
        for task in tier:
            tasks.append({
                "Task": str(task.get("name", "Task")),
                "Team": str(task.get("team", "Clinical Team")),
                "Tier": f"Stage {tier_idx+1}",
                "Start": start_time,
                "Duration": int(task.get("duration_min", 0)),
                "Finish": start_time + int(task.get("duration_min", 0))
            })
        start_time += tier_duration

    fig = go.Figure()

    team_colors = {
        "Triage Nursing": "#0284c7",
        "Resus Nurse Alpha": "#0891b2",
        "Blood Bank Tech": "#d946ef",
        "Anesthesiologist": "#8b5cf6",
        "Scrub Nurse": "#059669",
        "Surgical Assistant": "#f59e0b",
        "Trauma Surgeon": "#dc2626",
        "SICU Transport Team": "#475569"
    }

    for t in tasks:
        color = team_colors.get(t["Team"], "#0284c7")
        fig.add_trace(go.Bar(
            y=[t["Task"]],
            x=[t["Duration"]],
            base=[t["Start"]],
            orientation="h",
            name=t["Team"],
            marker=dict(color=color, line=dict(color="#ffffff", width=1.5)),
            hovertext=f"Task: {t['Task']}<br>Assigned Team: {t['Team']}<br>Duration: {t['Duration']} min<br>Phase: {t['Tier']}",
            hoverinfo="text",
            showlegend=False
        ))

    fig.update_layout(
        title="Partial Order Plan: Parallel Multi-Team Resuscitation Protocol",
        title_font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Elapsed Minutes from Patient Arrival", gridcolor="#f1f5f9"),
        yaxis=dict(title="", autorange="reversed", gridcolor="#f1f5f9"),
        height=360
    )

    return fig
