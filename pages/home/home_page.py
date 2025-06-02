# pages/home/home_page.py
import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from config.settings import AppConfig
from components.drag_drop_sidebar import render_drag_drop_sidebar
from components.flow_board import render_flow_board
from core.board_manager import BoardManager


def render_home_page():
    """Render the main home page interface with full screen drag-drop board"""

    # Initialize board manager
    if 'board_manager' not in st.session_state:
        st.session_state.board_manager = BoardManager()


    # Custom CSS for full screen experience
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }

        .stSidebar {
            background-color: #f8f9fa;
        }

        .drag-node {
            padding: 8px 12px;
            margin: 4px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            cursor: grab;
            text-align: center;
            font-weight: 500;
            transition: transform 0.2s ease;
        }

        .drag-node:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .flow-container {
            height: calc(100vh - 100px);
            border: 2px dashed #e0e0e0;
            border-radius: 12px;
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main title (compact)
    st.markdown(f"# {AppConfig.APP_ICON} {AppConfig.APP_NAME}")

    # Render drag-drop sidebar
    render_drag_drop_sidebar()

    # Main flow board (full screen)
    render_flow_board()
