# src/config/node_types.py
from enum import Enum
from typing import Dict

class NodeType(Enum):
    INPUT = "input"
    PROCESS = "process"
    OUTPUT = "output"
    FILTER = "filter"
    ANALYTICS = "analytics"

NODE_TYPE_CONFIG = {
    NodeType.INPUT: {
        'display_name': 'Data Input',
        'icon': '📥',
        'color': '#4CAF50',
        'default_ports': {'outputs': 1, 'inputs': 0}
    },
    NodeType.PROCESS: {
        'display_name': 'Process',
        'icon': '⚙️',
        'color': '#2196F3',
        'default_ports': {'outputs': 1, 'inputs': 1}
    },
    NodeType.OUTPUT: {
        'display_name': 'Output',
        'icon': '📤',
        'color': '#FF9800',
        'default_ports': {'outputs': 0, 'inputs': 1}
    },
    NodeType.FILTER: {
        'display_name': 'Filter',
        'icon': '🔍',
        'color': '#9C27B0',
        'default_ports': {'outputs': 1, 'inputs': 1}
    },
    NodeType.ANALYTICS: {
        'display_name': 'Analytics',
        'icon': '📊',
        'color': '#F44336',
        'default_ports': {'outputs': 1, 'inputs': 1}
    }
}
