# src/core/connection.py
from dataclasses import dataclass
from typing import Dict, Any
import uuid


@dataclass
class Connection:
    """Represents a connection between two nodes"""

    id: str = None
    from_node_id: str = ""
    from_port_id: str = ""
    to_node_id: str = ""
    to_port_id: str = ""

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """Convert connection to dictionary"""
        return {
            'id': self.id,
            'from_node_id': self.from_node_id,
            'from_port_id': self.from_port_id,
            'to_node_id': self.to_node_id,
            'to_port_id': self.to_port_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Connection':
        """Create connection from dictionary"""
        return cls(**data)
