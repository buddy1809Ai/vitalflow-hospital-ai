"""
components.py
=============
Clean, professional UI components for VitalFlow AI.
Ensures 100% reliable HTML rendering without markdown code block escaping.
"""

import streamlit as st
import textwrap
from typing import Dict, List, Any

def render_html(html_str: str):
    """
    Renders HTML safely in Streamlit by stripping leading indentation.
    Prevents markdown parsers from mistaking indented HTML for <pre><code> blocks.
    """
    clean_html = textwrap.dedent(html_str).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

def render_top_header():
    """Renders the executive SaaS top navigation bar."""
    render_html("""
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
    """)

def render_kpi_cards(metrics: List[Dict[str, str]]):
    """Renders a balanced, responsive row of executive KPI metric cards."""
    cols = st.columns(len(metrics))
    for i, col in enumerate(cols):
        m = metrics[i]
        with col:
            render_html(f"""
            <div class="kpi-card">
                <div class="kpi-label">{m.get('label', 'Metric')}</div>
                <div class="kpi-value">{m.get('value', '0')}</div>
                <div class="kpi-context">{m.get('context', '')}</div>
            </div>
            """)

def render_banner(message: str, level: str = "info"):
    """Renders a clean, purposeful notification strip."""
    class_map = {
        "info": "info-strip",
        "warning": "warning-strip",
        "success": "success-strip",
        "danger": "danger-strip"
    }
    cls_name = class_map.get(level, "info-strip")
    render_html(f"""
    <div class="{cls_name}">
        {message}
    </div>
    """)

def render_syllabus_pill(practical_id: str, title: str):
    """Renders a discreet syllabus reference tag."""
    render_html(f"""
    <div style="margin-bottom: 14px;">
        <span class="syllabus-pill">{practical_id}: {title}</span>
    </div>
    """)

def render_academic_disclaimer():
    """Renders the standard academic simulation disclaimer."""
    render_html("""
    <div class="academic-disclaimer">
        <strong>Academic Demonstration Note:</strong> VitalFlow AI is an educational platform illustrating classical and heuristic AI algorithms (A*, CSP, Reflex Agents, Horn Logic, POP) on simulated urban hospital datasets. Not for real clinical emergency dispatch or diagnostic use.
    </div>
    """)
