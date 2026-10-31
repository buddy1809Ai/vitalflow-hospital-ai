"""
components.py
=============
Clean, professional UI components for VitalFlow AI.
Designed for clarity, usability, and executive SaaS presentation.
"""

import streamlit as st
from typing import Dict, List, Any

def render_top_header():
    """Renders the executive SaaS top navigation bar."""
    st.markdown("""
    <div class="saas-header">
        <div class="saas-brand">
            <div class="saas-logo-icon">V</div>
            <div>
                <div class="saas-title">VitalFlow AI</div>
                <div class="saas-tagline">Autonomous Hospital Operations & Emergency Logistics Platform</div>
            </div>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            <span>Simulation Mode Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_cards(metrics: List[Dict[str, str]]):
    """Renders a balanced, responsive row of executive KPI metric cards."""
    cols = st.columns(len(metrics))
    for i, col in enumerate(cols):
        m = metrics[i]
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{m.get('label', 'Metric')}</div>
                <div class="kpi-value">{m.get('value', '0')}</div>
                <div class="kpi-context">{m.get('context', '')}</div>
            </div>
            """, unsafe_allow_html=True)

def render_banner(message: str, level: str = "info"):
    """Renders a clean, purposeful notification strip."""
    class_map = {
        "info": "info-strip",
        "warning": "warning-strip",
        "success": "success-strip",
        "danger": "danger-strip"
    }
    cls_name = class_map.get(level, "info-strip")
    st.markdown(f"""
    <div class="{cls_name}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def render_syllabus_pill(practical_id: str, title: str):
    """Renders a discreet syllabus reference tag."""
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <span class="syllabus-pill">{practical_id}: {title}</span>
    </div>
    """, unsafe_allow_html=True)

def render_academic_disclaimer():
    """Renders the standard academic simulation disclaimer."""
    st.markdown("""
    <div class="academic-disclaimer">
        <strong>Academic Demonstration Note:</strong> VitalFlow AI is an educational project illustrating classical and heuristic AI algorithms (A*, CSP, Reflex Agents, Horn-Clause Logic, POP) on simulated urban hospital datasets. Not for clinical diagnostic use.
    </div>
    """, unsafe_allow_html=True)
