import streamlit as st

def apply_theme(theme_name="Industrial Dark"):
    """
    Applies custom industrial styling to the Streamlit app based on the selected theme.
    """
    
    # Theme Definitions
    themes = {
        "Industrial Dark": {
            "bg_color": "#0E1117",
            "sec_bg_color": "#262730",
            "text_color": "#FAFAFA",
            "primary": "#4A90E2",
            "border": "#41424C",
            "metric_bg": "rgba(38, 39, 48, 0.9)",
            "bg_image": 'url("app/static/industrial_bg.png")'
        },
        "Light Corporate": {
            "bg_color": "#FFFFFF",
            "sec_bg_color": "#F0F2F6",
            "text_color": "#31333F",
            "primary": "#2D5BFF",
            "border": "#D1D5DB",
            "metric_bg": "#FFFFFF",
            "bg_image": 'none'
        },
        "Midnight Blue": {
            "bg_color": "#0a192f",
            "sec_bg_color": "#112240",
            "text_color": "#ccd6f6",
            "primary": "#64ffda",
            "border": "#233554",
            "metric_bg": "rgba(17, 34, 64, 0.95)",
            "bg_image": 'none'
        }
    }
    
    t = themes.get(theme_name, themes["Industrial Dark"])
    
    # Store theme in session state for other modules (charts)
    st.session_state['theme'] = t

    st.markdown(f"""
        <style>
        /* Main Import */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Roboto+Mono:wght@400;500&display=swap');

        /* Global Theme Overrides */
        :root {{
            --background-color: {t['bg_color']};
            --secondary-background-color: {t['sec_bg_color']};
            --text-color: {t['text_color']};
            --primary-color: {t['primary']};
            --border-color: {t['border']};
        }}

        /* Typography */
        html, body, [class*="css"], div, span, p {{
            font-family: 'Inter', sans-serif;
            color: var(--text-color) !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: {t['text_color']} !important; /* Adapted to theme */
            letter-spacing: -0.5px;
        }}

        code {{
            font-family: 'Roboto Mono', monospace;
        }}

        /* Background Image & Main Container */
        .stApp {{
            background-image: {t['bg_image']};
            background-color: {t['bg_color']};
            background-blend-mode: overlay;
        }}

        /* Metric Cards Industrial Look */
        div[data-testid="stMetric"] {{
            background-color: {t['metric_bg']};
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-color);
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            backdrop-filter: blur(5px);
        }}
        
        div[data-testid="stMetricLabel"] {{
            opacity: 0.7;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: {t['text_color']};
        }}

        div[data-testid="stMetricValue"] {{
            color: var(--text-color);
            font-weight: 600;
        }}

        /* Tables / DataFrames */
        div[class*="stDataFrame"] {{
            border: 1px solid var(--border-color);
        }}
        
        /* Force text color in DataFrames and Tables */
        div[data-testid="stDataFrame"] * {{
            color: var(--text-color) !important;
        }}
        div[data-testid="stTable"] * {{
            color: var(--text-color) !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: var(--secondary-background-color);
            border-right: 1px solid var(--border-color);
        }}

        /* Buttons (Industrial Flat Style) */
        button[kind="secondary"] {{
            border: 1px solid var(--border-color);
            background-color: transparent;
            color: var(--text-color);
            border-radius: 4px;
            transition: all 0.2s;
        }}
        button[kind="secondary"]:hover {{
            border-color: var(--primary-color);
            color: var(--primary-color);
        }}
        
        button[kind="primary"] {{
            background-color: var(--primary-color);
            border: none;
            border-radius: 4px;
            box-shadow: none;
            color: { "#FFFFFF" if theme_name != "Light Corporate" else "#FFFFFF" };
        }}

        /* Alerts/Status styling - Using slightly more opaque backgrounds for better read on light themes */
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        /* Remove Streamlit branding */
        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* PRINT STYLES */
        @media print {{
            /* Hide Sidebar and non-essential UI */
            section[data-testid="stSidebar"] {{ display: none; }}
            header {{ display: none; }}
            button {{ display: none; }}
            .stApp {{
                background-image: none !important;
                background-color: white !important;
            }}
            /* Reset Text Colors for Print */
            html, body, [class*="css"], h1, h2, h3, div, span, p {{
                color: black !important;
                font-family: 'Inter', sans-serif !important;
            }}
            /* Remove dark backgrounds from Cards */
            div[data-testid="stMetric"] {{
                background-color: white !important;
                border: 1px solid #ccc !important;
                box-shadow: none !important;
                backdrop-filter: none;
            }}
            /* Ensure charts printed (Approximation, Plotly canvas sometimes tricky) */
            .main .block-container {{
                max-width: 100%;
                padding: 1rem;
            }}
        }}

        </style>
    """, unsafe_allow_html=True)
