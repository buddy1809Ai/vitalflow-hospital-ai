"""
styles.py
=========
World-class SaaS Design System & UI/UX Styling for VitalFlow AI.
Minimalist, executive healthcare aesthetics: clean whitespace, modern typography,
subtle borders, refined neutral surfaces, and purposeful accent colors.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Modern Web Typography Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1e293b;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Container Spacing & Layout */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1320px !important;
    }

    /* Professional Top Navigation Bar */
    .saas-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .saas-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .saas-logo-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25);
    }

    .saas-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    .saas-tagline {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 500;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #15803d;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #22c55e;
        border-radius: 50%;
    }

    /* Clean Metric KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .kpi-context {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 6px;
        font-weight: 400;
    }

    /* Purposeful Content Surfaces */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .content-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }

    .content-sub {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 18px;
        line-height: 1.5;
    }

    /* Subtle Notification Strips */
    .info-strip {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        border-radius: 8px;
        padding: 12px 16px;
        color: #334155;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .warning-strip {
        background: #fffbeb;
        border: 1px solid #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        color: #92400e;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .success-strip {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-left: 4px solid #16a34a;
        border-radius: 8px;
        padding: 12px 16px;
        color: #166534;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .danger-strip {
        background: #fef2f2;
        border: 1px solid #fee2e2;
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 12px 16px;
        color: #991b1b;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    /* Minimal Academic Citation Badge */
    .syllabus-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #475569;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Polished Tab Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 16px;
        color: #64748b;
        border: none !important;
        background: transparent;
        transition: all 0.15s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #0f172a;
        background: rgba(255, 255, 255, 0.7);
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #0284c7 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }

    /* Modern Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        border: 1px solid #cbd5e1 !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        border-color: #94a3b8 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    }

    /* Primary Action Button */
    button[kind="primary"] {
        background: #0284c7 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
    }

    button[kind="primary"]:hover {
        background: #0369a1 !important;
        border-color: #0369a1 !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25) !important;
    }

    /* Form Fields & Select Boxes */
    div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #cbd5e1 !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #94a3b8 !important;
    }

    /* Clean Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Radio Navigation in Sidebar */
    div[data-testid="stRadio"] > div {
        gap: 6px !important;
    }

    div[data-testid="stRadio"] label {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        transition: all 0.15s ease;
        margin-bottom: 2px;
        cursor: pointer;
    }

    div[data-testid="stRadio"] label:hover {
        border-color: #0284c7;
        background: #f0f9ff;
    }

    /* Disclaimer Footer */
    .academic-disclaimer {
        font-size: 0.75rem;
        color: #94a3b8;
        border-top: 1px solid #e2e8f0;
        padding-top: 14px;
        margin-top: 30px;
        text-align: center;
        line-height: 1.5;
    }
    </style>
    """
