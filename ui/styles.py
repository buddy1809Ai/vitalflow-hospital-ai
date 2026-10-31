"""
styles.py
=========
Custom CSS and Design System for VitalFlow AI.
Injects a modern, premium SaaS visual aesthetic with dark/light harmony,
clean typography, elevated card surfaces, and glowing status pills.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }

    /* Top Hero Header Card */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #1e293b 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 50%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #94a3b8;
        margin-top: 6px;
        font-weight: 400;
        line-height: 1.5;
    }

    .hero-badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    .hero-pill.live {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.4);
        color: #34d399;
    }

    .hero-pill.academic {
        background: rgba(99, 102, 241, 0.18);
        border-color: rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
    }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }

    .metric-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.1;
    }

    .metric-sub {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 500;
        margin-top: 6px;
    }

    /* Glassmorphic Section Cards */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }

    .section-header {
        font-size: 1.18rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .section-desc {
        font-size: 0.86rem;
        color: #64748b;
        margin-bottom: 16px;
    }

    /* Status Alert Strips */
    .alert-strip-red {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px 16px;
        color: #991b1b;
        font-size: 0.88rem;
        font-weight: 500;
        margin-bottom: 14px;
    }

    .alert-strip-green {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 12px 16px;
        color: #065f46;
        font-size: 0.88rem;
        font-weight: 500;
        margin-bottom: 14px;
    }

    .alert-strip-blue {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 12px 16px;
        color: #1e40af;
        font-size: 0.88rem;
        font-weight: 500;
        margin-bottom: 14px;
    }

    /* Algorithm Comparison Pills */
    .algo-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        background: #e2e8f0;
        color: #334155;
    }

    .algo-tag.optimal {
        background: #dcfce7;
        color: #166534;
    }

    .algo-tag.heuristic {
        background: #fef3c7;
        color: #92400e;
    }

    /* Streamlit Tabs Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1f5f9;
        padding: 6px 8px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 8px 16px;
        color: #475569;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.6);
        color: #0f172a;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    </style>
    """
