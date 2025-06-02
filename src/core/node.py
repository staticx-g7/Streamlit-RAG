# src/core/node.py
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


@dataclass
class NodePort:
    """Represents an input or output port on a node"""
    id: str
    name: str
    port_type: str  # 'input' or 'output'
    data_type: str = 'any'
    connected_to: List[str] = field(default_factory=list)


@dataclass
class Node:
    """Enhanced Node class with proper structure"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    x: float = 0.0
    y: float = 0.0
    node_type: str = "process"
    title: str = "New Node"
    description: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Port management
    input_ports: List[NodePort] = field(default_factory=list)
    output_ports: List[NodePort] = field(default_factory=list)

    # Visual properties
    width: float = 150.0
    height: float = 80.0
    color: str = "#2196F3"
    selected: bool = False

    def add_input_port(self, name: str, data_type: str = 'any') -> NodePort:
        """Add an input port to the node"""
        port = NodePort(
            id=str(uuid.uuid4()),
            name=name,
            port_type='input',
            data_type=data_type
        )
        self.input_ports.append(port)
        return port

    def add_output_port(self, name: str, data_type: str = 'any') -> NodePort:
        """Add an output port to the node"""
        port = NodePort(
            id=str(uuid.uuid4()),
            name=name,
            port_type='output',
            data_type=data_type
        )
        self.output_ports.append(port)
        return port

    def get_port_by_id(self, port_id: str) -> Optional[NodePort]:
        """Get a port by its ID"""
        for port in self.input_ports + self.output_ports:
            if port.id == port_id:
                return port
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary for serialization"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'node_type': self.node_type,
            'title': self.title,
            'description': self.description,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'input_ports': [
                {
                    'id': port.id,
                    'name': port.name,
                    'port_type': port.port_type,
                    'data_type': port.data_type,
                    'connected_to': port.connected_to
                }
                for port in self.input_ports
            ],
            'output_ports': [
                {
                    'id': port.id,
                    'name': port.name,
                    'port_type': port.port_type,
                    'data_type': port.data_type,
                    'connected_to': port.connected_to
                }
                for port in self.output_ports
            ],
            'width': self.width,
            'height': self.height,
            'color': self.color
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """Create node from dictionary"""
        node = cls(
            id=data['id'],
            x=data['x'],
            y=data['y'],
            node_type=data['node_type'],
            title=data['title'],
            description=data.get('description', ''),
            data=data.get('data', {}),
            width=data.get('width', 150.0),
            height=data.get('height', 80.0),
            color=data.get('color', '#2196F3')
        )

        # Restore ports
        for port_data in data.get('input_ports', []):
            port = NodePort(**port_data)
            node.input_ports.append(port)

        for port_data in data.get('output_ports', []):
            port = NodePort(**port_data)
            node.output_ports.append(port)

        return node
