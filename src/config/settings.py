# src/config/settings.py
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AppConfig:
    """Application configuration settings"""

    APP_NAME: str = "Node-Based Streamlit App"
    APP_ICON: str = "🔗"
    VERSION: str = "1.0.0"

    # Board settings
    DEFAULT_ZOOM: float = 1.0
    MIN_ZOOM: float = 0.1
    MAX_ZOOM: float = 5.0
    GRID_SPACING: int = 50

    # Node settings
    DEFAULT_NODE_SIZE: int = 20
    NODE_COLORS: Dict[str, str] = field(default_factory=lambda: {
        'input': '#4CAF50',
        'process': '#2196F3',
        'output': '#FF9800',
        'filter': '#9C27B0',
        'analytics': '#F44336'
    })

    # UI settings
    SIDEBAR_WIDTH: int = 300
    BOARD_HEIGHT: int = 600
