"""
components.py
=============
Reusable UI widgets, alert containers, metric panels, and academic callouts.
"""

import streamlit as st
from typing import Dict, Any, List

def render_hero_banner():
    """Renders the top executive command center banner."""
    st.markdown("""
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <h1 class="hero-title">VITALFLOW AI</h1>
                <p class="hero-subtitle">
                    Autonomous Hospital Operations & Emergency Logistics Command System<br>
                    <span style="color: #cbd5e1; font-size: 0.86rem;">
                        Multi-Agent Decision Support & State-Space Optimization Engine
                    </span>
                </p>
            </div>
            <div style="text-align: right; margin-top: 4px;">
                <span class="hero-pill live">● SYSTEM OPERATIONAL</span>
                <span class="hero-pill academic">B.Tech AI & DS Minor Project</span>
            </div>
        </div>
        <div class="hero-badge-row">
            <span class="hero-pill">⚡ A* vs Greedy Search (P3, P4, P9)</span>
            <span class="hero-pill">🩺 Model-Based Reflex Telemetry (P1, P2)</span>
            <span class="hero-pill">🧩 CSP Min-Conflicts Duty (P5)</span>
            <span class="hero-pill">⚖️ Propositional Triage Logic (P7, P8)</span>
            <span class="hero-pill">⏱️ Partial Order Planning (P10)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_row(metrics: List[Dict[str, str]]):
    """Renders a responsive row of SaaS metric cards."""
    cols = st.columns(len(metrics))
    for i, col in enumerate(cols):
        m = metrics[i]
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{m.get('title', 'Metric')}</div>
                <div class="metric-value">{m.get('value', '0')}</div>
                <div class="metric-sub">{m.get('sub', '')}</div>
            </div>
            """, unsafe_allow_html=True)

def render_alert_strip(message: str, level: str = "blue"):
    """Renders a custom colored alert strip."""
    cls_map = {
        "red": "alert-strip-red",
        "green": "alert-strip-green",
        "blue": "alert-strip-blue"
    }
    cls_name = cls_map.get(level, "alert-strip-blue")
    st.markdown(f"""
    <div class="{cls_name}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def render_syllabus_badge(practical_num: int, practical_title: str, ai_concept: str):
    """Displays an academic citation badge linking directly to the syllabus."""
    st.markdown(f"""
    <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 10px 14px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;">
        <div>
            <strong style="color: #1e293b; font-size: 0.85rem;">Syllabus Mapping: Practical {practical_num}</strong>
            <span style="color: #64748b; font-size: 0.82rem; margin-left: 8px;">{practical_title}</span>
        </div>
        <span class="algo-tag optimal">{ai_concept}</span>
    </div>
    """, unsafe_allow_html=True)
