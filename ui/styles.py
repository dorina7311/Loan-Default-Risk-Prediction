import streamlit as st
from ui.config.settings import COLORS

def apply_global_styles():
    st.markdown(f"""
    <style>
        :root {{
            --primary-color: {COLORS['primary']};
            --success-color: {COLORS['success']};
            --warning-color: {COLORS['warning']};
            --danger-color: {COLORS['danger']};
            --dark-danger: {COLORS['dark_danger']};
            --bg-color: {COLORS['background']};
            --text-color: {COLORS['text']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: {COLORS['text']};
        }}
        
        .main {{
            padding: 2rem 1rem;
            background: white;
        }}
        
        [data-testid="stMetric"] {{
            background: linear-gradient(135deg, #f5f9fc 0%, #e8f1f8 100%) !important;
            padding: 1.5rem !important;
            border-radius: 12px !important;
            border-left: 5px solid {COLORS['primary']} !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }}
        
        [data-testid="stMetric"] > div {{
            color: #000000 !important;
        }}
        
        [data-testid="stMetric"] > div:first-child {{
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #1f3a56 !important;
        }}
        
        [data-testid="stMetric"] > div:nth-child(2) {{
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #000000 !important;
        }}
        
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12) !important;
            border-left-color: #1557a0 !important;
        }}
        
        .header-main {{
            text-align: center;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, #1557a0 100%);
            color: white;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header-main h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }}
        
        .header-main p {{
            font-size: 1.1rem;
            opacity: 0.95;
            font-weight: 300;
        }}
        
        .subheader {{
            color: {COLORS['primary']};
            font-size: 1.5rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {COLORS['background']};
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid {COLORS['border']};
            margin: 1rem 0;
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            border-color: {COLORS['primary']};
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 1rem 0;
            text-align: center;
            width: 100%;
        }}
        
        .risk-badge-low {{
            background-color: {COLORS['success']};
            color: white;
        }}
        
        .risk-badge-medium {{
            background-color: {COLORS['warning']};
            color: white;
        }}
        
        .risk-badge-high {{
            background-color: {COLORS['danger']};
            color: white;
        }}
        
        .risk-badge-very-high {{
            background-color: {COLORS['dark_danger']};
            color: white;
        }}
        
        [data-testid="stForm"] {{
            background: {COLORS['background']};
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
        }}

        /* Form labels - make visible */
        .stTextInput label, .stSelectbox label {{
            color: #000000 !important;
            font-weight: 700;
        }}
        
        [data-testid="stNumberInput"] label {{
            color: #000000 !important;
            font-weight: 700;
        }}
        
        [data-testid="stFormSubmitButton"] button {{
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, #1557a0 100%);
            color: white;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        [data-testid="stFormSubmitButton"] button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}
        
        [data-testid="stFormSubmitButton"] button:active {{
            transform: translateY(0);
        }}
        
        .stButton > button {{
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .info-box {{
            background: #e8f4f8;
            border-left: 4px solid {COLORS['primary']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .warning-box {{
            background: #fff3e0;
            border-left: 4px solid {COLORS['warning']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .danger-box {{
            background: #ffebee;
            border-left: 4px solid {COLORS['danger']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .sidebar {{
            background: linear-gradient(180deg, {COLORS['primary']} 0%, #1557a0 100%);
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #f5f7fa 0%, #e9ecef 100%);
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {COLORS['primary']};
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS['primary']};
            margin-top: 0.5rem;
        }}
        
        .divider {{
            border-top: 2px solid {COLORS['border']};
            margin: 2rem 0;
        }}
        
        [data-testid="stTabs"] {{
            background: transparent;
        }}
        
        [data-testid="stExpander"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}
        
        .prose {{
            line-height: 1.6;
            color: #444;
        }}
        
        @media (max-width: 640px) {{
            .header-main h1 {{
                font-size: 1.8rem;
            }}
            
            .header-main {{
                padding: 1.5rem 1rem;
            }}
            
            [data-testid="stMetric"] {{
                margin-bottom: 1rem;
            }}
        }}
        
        hr {{
            border: none;
            border-top: 2px solid {COLORS['border']};
            margin: 2rem 0;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str = ""):
    col = st.columns([1])[0]
    with col:
        st.markdown(f"""
        <div class="header-main">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)

def render_info_box(text: str):
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)

def render_warning_box(text: str):
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)

def render_danger_box(text: str):
    st.markdown(f'<div class="danger-box">{text}</div>', unsafe_allow_html=True)

def render_risk_badge(risk_level: str, probability: float):
    badge_class = f"risk-badge risk-badge-{risk_level.lower().replace('_', '-')}"
    st.markdown(f"""
    <div class="{badge_class}">
        {risk_level.replace('_', ' ')} - {probability:.1%}
    </div>
    """, unsafe_allow_html=True)
