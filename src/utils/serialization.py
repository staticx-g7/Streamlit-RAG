# src/utils/serialization.py
import json
from typing import Any, Dict
from datetime import datetime

def serialize_datetime(obj: Any) -> str:
    """Serialize datetime objects to ISO format"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def safe_json_dumps(data: Dict[str, Any], indent: int = 2) -> str:
    """Safely serialize data to JSON with datetime handling"""
    return json.dumps(data, indent=indent, default=serialize_datetime)

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """Safely deserialize JSON string"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

def validate_node_data(data: Dict[str, Any]) -> bool:
    """Validate node data structure"""
    required_fields = ['id', 'x', 'y', 'node_type', 'title']
    return all(field in data for field in required_fields)

def validate_connection_data(data: Dict[str, Any]) -> bool:
    """Validate connection data structure"""
    required_fields = ['from_node_id', 'to_node_id']
    return all(field in data for field in required_fields)
