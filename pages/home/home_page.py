# pages/home/home_page.py
import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

# Use absolute imports instead of relative imports
from config.settings import AppConfig
from components.sidebar import render_main_sidebar
from components.board import render_infinite_board
from components.node_editor import render_node_editor
from core.board_manager import BoardManager


def render_home_page():
    """Render the main home page interface"""

    # Initialize board manager
    if 'board_manager' not in st.session_state:
        st.session_state.board_manager = BoardManager()

    # Main title
    st.title(f"{AppConfig.APP_ICON} {AppConfig.APP_NAME}")
    st.markdown("**Interactive infinite board with draggable nodes and connections**")

    # Create main layout
    col1, col2 = st.columns([3, 1])

    with col1:
        # Main board area
        render_infinite_board()

    with col2:
        # Node editor panel
        render_node_editor()

    # Render sidebar (this will appear in the sidebar)
    render_main_sidebar()

    # Footer
    st.markdown("---")
    st.markdown("**Built with Streamlit** • *Infinite possibilities on an infinite board* 🚀")
