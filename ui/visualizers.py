"""
visualizers.py
==============
Polished Plotly visualizers for VitalFlow AI.
Clean typography, high-contrast palette, and responsive layouts.
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

    # 1. Base Road Network
    for u, v, dist, speed in ROAD_EDGES:
        x0, y0 = HOSPITAL_NODES[u]["x"], HOSPITAL_NODES[u]["y"]
        x1, y1 = HOSPITAL_NODES[v]["x"], HOSPITAL_NODES[v]["y"]

        is_blocked = (u, v) in blocked_set
        line_color = "#f43f5e" if is_blocked else "#e2e8f0"
        line_width = 3.0 if is_blocked else 1.8
        dash_style = "dot" if is_blocked else "solid"

        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(color=line_color, width=line_width, dash=dash_style),
            hoverinfo="text",
            text=f"Road: {u} ↔ {v}<br>Distance: {dist} km | Speed Limit: {speed} km/h{' (ROAD BLOCKED)' if is_blocked else ''}",
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
            name="Greedy Best-First Route (f = h)",
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
            color = "#dc2626"  # Apex Trauma Center
            size = 18
        elif v.get("trauma_ready", False):
            color = "#0284c7"  # Tertiary Care
            size = 14
        else:
            color = "#64748b"  # Transit Outpost
            size = 10

        node_color.append(color)
        node_size.append(size)
        node_text.append(
            f"<b>{v['name']}</b><br>"
            f"Classification: {v['type']}<br>"
            f"ICU Bed Capacity: {v['icu_beds']}<br>"
            f"Trauma Facility: {'Yes' if v['trauma_ready'] else 'No'}<br>"
            f"Grid Position: ({v['x']}, {v['y']})"
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
        textfont=dict(size=10, color="#334155", family="Inter"),
        hoverinfo="text",
        hovertext=node_text,
        name="Hospitals & Junctions"
    ))

    fig.update_layout(
        title="Urban Healthcare Transit Network Topology (Nagpur)",
        title_font=dict(size=14, color="#0f172a", family="Inter"),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, title="Displacement East-West (km)"),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, title="Displacement North-South (km)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, family="Inter")),
        height=480
    )

    return fig


def plot_patient_telemetry(timesteps: List[Dict[str, Any]], patient_name: str) -> go.Figure:
    """
    Renders an interactive physiological telemetry stream (HR, BP, SpO2, Shock Index).
    """
    times = [t["time"] for t in timesteps]
    hr = [t["hr"] for t in timesteps]
    sys_bp = [t["sys_bp"] for t in timesteps]
    dia_bp = [t["dia_bp"] for t in timesteps]
    spo2 = [t["spo2"] for t in timesteps]

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

    # Reference guideline lines
    fig.add_hline(y=100, line_dash="dot", line_color="rgba(239, 68, 68, 0.3)", annotation_text="Tachycardia (100 bpm)", annotation_font_size=10)
    fig.add_hline(y=90, line_dash="dot", line_color="rgba(16, 185, 129, 0.3)", annotation_text="Hypoxia Caution (90% SpO2)", annotation_font_size=10)

    fig.update_layout(
        title=f"Continuous Physiological Telemetry — {patient_name}",
        title_font=dict(size=13, color="#0f172a", family="Inter"),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(title="Inspection Window", gridcolor="#f1f5f9"),
        yaxis=dict(title="Amplitude / Physiological Value", gridcolor="#f1f5f9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, family="Inter")),
        height=360
    )

    return fig


def plot_csp_convergence(history: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders the Min-Conflicts local search optimization trajectory.
    """
    steps = [h["step"] for h in history]
    conflicts = [h["conflicts"] for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=steps,
        y=conflicts,
        mode="lines+markers",
        line=dict(color="#0284c7", width=2.5),
        marker=dict(size=5, color="#0369a1"),
        fill="tozeroy",
        fillcolor="rgba(2, 132, 199, 0.08)",
        name="Active Constraint Violations"
    ))

    fig.update_layout(
        title="Min-Conflicts Optimization: Conflict Reduction Curve",
        title_font=dict(size=13, color="#0f172a", family="Inter"),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Search Iteration Step", gridcolor="#f1f5f9"),
        yaxis=dict(title="Total Violations", gridcolor="#f1f5f9", dtick=1),
        height=300
    )

    return fig


def plot_partial_order_plan(tiers: List[List[Dict[str, Any]]]) -> go.Figure:
    """
    Renders an interactive Gantt timeline for Partial Order Planning.
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
        "Triage Nursing": "#0284c7",
        "Resus Nurse Alpha": "#0891b2",
        "Blood Bank Tech": "#d946ef",
        "Anesthesiologist": "#8b5cf6",
        "Scrub Nurse": "#059669",
        "Surgical Assistant": "#f59e0b",
        "Trauma Surgeon": "#dc2626",
        "SICU Transport Team": "#64748b"
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
        title="Partial Order Plan: Parallel Multi-Team Surgical Timeline",
        title_font=dict(size=13, color="#0f172a", family="Inter"),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(title="Elapsed Time (Minutes from Arrival)", gridcolor="#f1f5f9"),
        yaxis=dict(title="", autorange="reversed", gridcolor="#f1f5f9"),
        height=360
    )

    return fig
