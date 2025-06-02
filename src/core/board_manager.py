# src/core/board_manager.py
from typing import Dict, List, Optional
import json
from datetime import datetime
from .node import Node  # This relative import is fine within the same package
from .connection import Connection


class BoardManager:
    """Manages the overall state of the node board"""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.connections: List[Connection] = []
        self.selected_nodes: List[str] = []

        # View state
        self.center_x: float = 0.0
        self.center_y: float = 0.0
        self.zoom_level: float = 1.0

    def add_node(self, node: Node) -> str:
        """Add a node to the board"""
        self.nodes[node.id] = node
        return node.id

    def remove_node(self, node_id: str) -> bool:
        """Remove a node and its connections"""
        if node_id not in self.nodes:
            return False

        # Remove connections
        self.connections = [
            conn for conn in self.connections
            if conn.from_node_id != node_id and conn.to_node_id != node_id
        ]

        # Remove node
        del self.nodes[node_id]

        # Remove from selection
        if node_id in self.selected_nodes:
            self.selected_nodes.remove(node_id)

        return True

    def add_connection(self, from_node_id: str, from_port_id: str,
                       to_node_id: str, to_port_id: str) -> Optional[Connection]:
        """Add a connection between nodes"""
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return None

        connection = Connection(
            from_node_id=from_node_id,
            from_port_id=from_port_id,
            to_node_id=to_node_id,
            to_port_id=to_port_id
        )

        self.connections.append(connection)
        return connection

    def export_board_data(self) -> str:
        """Export board data as JSON string"""
        export_data = {
            'nodes': {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            'connections': [conn.to_dict() for conn in self.connections],
            'view_state': {
                'center_x': self.center_x,
                'center_y': self.center_y,
                'zoom_level': self.zoom_level
            },
            'exported_at': datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)

    def import_board_data(self, uploaded_file):
        """Import board data from uploaded file"""
        import_data = json.load(uploaded_file)

        # Clear existing data
        self.nodes.clear()
        self.connections.clear()
        self.selected_nodes.clear()

        # Import nodes
        for node_id, node_data in import_data.get('nodes', {}).items():
            node = Node.from_dict(node_data)
            self.nodes[node_id] = node

        # Import connections
        for conn_data in import_data.get('connections', []):
            connection = Connection.from_dict(conn_data)
            self.connections.append(connection)

        # Import view state
        view_state = import_data.get('view_state', {})
        self.center_x = view_state.get('center_x', 0.0)
        self.center_y = view_state.get('center_y', 0.0)
        self.zoom_level = view_state.get('zoom_level', 1.0)

    def get_timestamp(self) -> str:
        """Get current timestamp for file naming"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')
