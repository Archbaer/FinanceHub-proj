import streamlit as st

def apply_dark_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stSidebar {
        background-color: #262730;
    }
    
    .stSelectbox > div > div {
        background-color: #262730;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border: 1px solid #4a4a4a;
    }
    
    .stButton > button {
        background-color: #0052cc;
        color: #ffffff;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #0066ff;
    }
    
    .stDataFrame {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #ffffff;
    }
    
    .stMetric {
        background-color: #262730;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #4a4a4a;
    }
    
    .stMetric > div {
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff;
    }
    
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #4a4a4a;
        padding: 10px;
        border-radius: 5px;
        color: #ffffff;
    }
    
    .stSelectbox label {
        color: #ffffff;
    }
    
    .stTextInput label {
        color: #ffffff;
    }
    
    .element-container {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_light_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)

def render_theme_toggle():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Theme toggle in top navigation
    if st.session_state.dark_mode:
        apply_dark_theme()
    else:
        apply_light_theme()

def render_top_nav_toggle():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()