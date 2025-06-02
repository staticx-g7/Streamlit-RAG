# app.py
import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import home page
from pages.home.home_page import render_home_page


def main():
    """Main application entry point"""

    # Configure page
    st.set_page_config(
        page_title="Node-Based Streamlit App",
        page_icon="🔗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Render home page
    render_home_page()


if __name__ == "__main__":
    main()
