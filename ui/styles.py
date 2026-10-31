"""
styles.py
=========
World-class SaaS Design System for VitalFlow AI.
Guarantees 100% text visibility, high contrast, clean modern typography,
crisp light-themed surfaces, and zero white-on-white or dark-on-dark artifacts.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1340px !important;
    }

    /* ------------------------------------------------------------- */
    /* TOP SaaS HEADER BAR                                           */
    /* ------------------------------------------------------------- */
    .saas-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }

    .saas-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .saas-logo-icon {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff !important;
        font-size: 1.3rem;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
    }

    .saas-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f172a !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    .saas-tagline {
        font-size: 0.82rem;
        color: #64748b !important;
        font-weight: 500;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
    }

    /* ------------------------------------------------------------- */
    /* SIDEBAR STYLING & HIGH-CONTRAST NAVIGATION                    */
    /* ------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Sidebar Radio Item Surfaces */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        gap: 8px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        border-color: #0284c7 !important;
        background-color: #f0f9ff !important;
    }

    /* Radio text visibility - CRITICAL FIX */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label div {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Selected Radio Item Highlighting */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [aria-checked="true"] {
        background-color: #e0f2fe !important;
        border-color: #0284c7 !important;
        box-shadow: 0 1px 4px rgba(2, 132, 199, 0.15) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [aria-checked="true"] p {
        color: #0369a1 !important;
        font-weight: 700 !important;
    }

    /* ------------------------------------------------------------- */
    /* STREAMLIT TABS - HIGH CONTRAST & VISIBILITY                   */
    /* ------------------------------------------------------------- */
    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #e2e8f0 !important;
        padding: 6px 8px !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    button[data-baseweb="tab"] {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 9px 20px !important;
        color: #334155 !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.15s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #0f172a !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Active Tab */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0284c7 !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
    }

    button[data-baseweb="tab"] div,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: inherit !important;
        font-weight: inherit !important;
    }

    /* ------------------------------------------------------------- */
    /* METRIC KPI CARDS                                              */
    /* ------------------------------------------------------------- */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
    }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #475569 !important;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a !important;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }

    .kpi-context {
        font-size: 0.82rem;
        color: #64748b !important;
        margin-top: 6px;
        font-weight: 500;
    }

    /* ------------------------------------------------------------- */
    /* CONTENT SURFACES & CARDS                                      */
    /* ------------------------------------------------------------- */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02);
    }

    .content-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a !important;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }

    .content-sub {
        font-size: 0.86rem;
        color: #475569 !important;
        margin-bottom: 18px;
        line-height: 1.5;
    }

    /* ------------------------------------------------------------- */
    /* FORM CONTROLS, SELECTBOXES & INPUTS                           */
    /* ------------------------------------------------------------- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }

    div[data-baseweb="select"] * {
        color: #0f172a !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="popover"] div {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    div[data-testid="stSlider"] label p,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stRadio"] label p {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    div[data-testid="stCheckbox"] label span {
        color: #0f172a !important;
        font-weight: 500 !important;
    }

    /* ------------------------------------------------------------- */
    /* BUTTONS                                                       */
    /* ------------------------------------------------------------- */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 9px 20px !important;
        transition: all 0.15s ease !important;
    }

    button[kind="primary"] {
        background-color: #0284c7 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3) !important;
    }

    button[kind="primary"]:hover {
        background-color: #0369a1 !important;
        border-color: #0369a1 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
        transform: translateY(-1px);
    }

    button[kind="secondary"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
    }

    button[kind="secondary"]:hover {
        border-color: #94a3b8 !important;
        background-color: #f8fafc !important;
    }

    /* ------------------------------------------------------------- */
    /* EXPANDERS & TABLES                                            */
    /* ------------------------------------------------------------- */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
    }

    div[data-testid="stExpander"] summary {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }

    div[data-testid="stExpander"] summary:hover {
        color: #0284c7 !important;
    }

    div[data-testid="stExpanderDetails"] * {
        color: #1e293b !important;
    }

    /* Streamlit DataFrame & Tables */
    div[data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }

    /* ------------------------------------------------------------- */
    /* PURPOSEFUL NOTIFICATION STRIPS                                */
    /* ------------------------------------------------------------- */
    .info-strip {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-left: 4px solid #0284c7;
        border-radius: 8px;
        padding: 12px 16px;
        color: #0369a1 !important;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .warning-strip {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        color: #92400e !important;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .success-strip {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
        border-radius: 8px;
        padding: 12px 16px;
        color: #166534 !important;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .danger-strip {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 12px 16px;
        color: #991b1b !important;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .syllabus-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #334155 !important;
        font-family: 'JetBrains Mono', monospace;
    }

    .academic-disclaimer {
        font-size: 0.78rem;
        color: #64748b !important;
        border-top: 1px solid #e2e8f0;
        padding-top: 16px;
        margin-top: 32px;
        text-align: center;
        line-height: 1.5;
    }
    </style>
    """
