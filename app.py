# app.py
import streamlit as st
import sys
from pathlib import Path

# MUST BE FIRST: Configure page before any other Streamlit commands
st.set_page_config(
    page_title="Node-Based Streamlit App",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import home page
from pages.home.home_page import render_home_page


def main():
    """Main application entry point"""

    # Render home page (no page config here)
    render_home_page()


if __name__ == "__main__":
    main()
