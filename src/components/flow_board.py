# src/components/flow_board.py
import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from core.board_manager import BoardManager
from uuid import uuid4


def render_flow_board():
    """Render the main flow board with drag-drop functionality"""

    board_manager = st.session_state.board_manager

    # Initialize flow state if it doesn't exist
    if 'flow_state' not in st.session_state:
        flow_nodes, flow_edges = convert_to_flow_format(board_manager)
        st.session_state.flow_state = StreamlitFlowState(
            nodes=flow_nodes,
            edges=flow_edges
        )

    # Update flow state with current board data
    update_flow_state(board_manager)

    # Create the flow diagram
    st.markdown("### 🗂️ Interactive Flow Board")
    st.markdown("*Drag nodes around, connect them, and build your workflow*")

    # Flow component container
    with st.container():
        if st.session_state.flow_state.nodes:
            # Render the flow diagram
            st.session_state.flow_state = streamlit_flow(
                "main_flow",
                st.session_state.flow_state
            )

            # Handle flow interactions
            handle_flow_interactions(st.session_state.flow_state, board_manager)

        else:
            # Empty state
            render_empty_state()


def update_flow_state(board_manager: BoardManager):
    """Update flow state with current board data"""

    flow_nodes, flow_edges = convert_to_flow_format(board_manager)

    # Update nodes and edges
    st.session_state.flow_state.nodes = flow_nodes
    st.session_state.flow_state.edges = flow_edges


def convert_to_flow_format(board_manager: BoardManager):
    """Convert board nodes and connections to flow format"""

    flow_nodes = []
    flow_edges = []

    # Convert nodes using the correct position format
    for node in board_manager.nodes.values():
        flow_node = StreamlitFlowNode(
            id=node.id,
            pos=(node.x, node.y),  # Use pos for position
            data={'content': f"{get_node_icon(node.node_type)} {node.title}"},
            node_type='default',
            source_position='right',
            target_position='left',
            style={
                'background': node.color,
                'color': 'white',
                'border': '2px solid #ffffff' if node.selected else '1px solid #cccccc',
                'borderRadius': '8px',
                'padding': '10px',
                'fontSize': '12px',
                'fontWeight': '500',
                'minWidth': '120px',
                'textAlign': 'center'
            },
            draggable=True,
            selectable=True
        )
        flow_nodes.append(flow_node)

    # Convert connections
    for connection in board_manager.connections:
        flow_edge = StreamlitFlowEdge(
            id=connection.id,
            source=connection.from_node_id,
            target=connection.to_node_id,
            edge_type='smoothstep',
            style={
                'stroke': '#4CAF50',
                'strokeWidth': 3
            },
            animated=True,
            marker_end={'type': 'arrow', 'color': '#4CAF50'}
        )
        flow_edges.append(flow_edge)

    return flow_nodes, flow_edges


def get_node_icon(node_type: str) -> str:
    """Get icon for node type"""
    from config.node_types import NodeType, NODE_TYPE_CONFIG

    try:
        return NODE_TYPE_CONFIG[NodeType(node_type)]['icon']
    except:
        return "⚙️"


def handle_flow_interactions(flow_state, board_manager: BoardManager):
    """Handle interactions from the flow diagram with safe attribute access"""

    # Update node positions from flow state with safe attribute access
    for flow_node in flow_state.nodes:
        node_id = flow_node.id
        if node_id in board_manager.nodes:
            # Try different position attribute names based on version
            if hasattr(flow_node, 'pos'):
                # Version with 'pos' attribute
                board_manager.nodes[node_id].x = flow_node.pos[0]
                board_manager.nodes[node_id].y = flow_node.pos[1]
            elif hasattr(flow_node, 'position'):
                # Version with 'position' attribute
                board_manager.nodes[node_id].x = flow_node.position['x']
                board_manager.nodes[node_id].y = flow_node.position['y']
            elif hasattr(flow_node, 'data') and 'position' in flow_node.data:
                # Position stored in data
                board_manager.nodes[node_id].x = flow_node.data['position']['x']
                board_manager.nodes[node_id].y = flow_node.data['position']['y']

    # Handle new connections
    current_edge_ids = {conn.id for conn in board_manager.connections}

    for flow_edge in flow_state.edges:
        if flow_edge.id not in current_edge_ids:
            # New connection created
            from core.connection import Connection
            new_connection = Connection(
                id=flow_edge.id,
                from_node_id=flow_edge.source,
                to_node_id=flow_edge.target
            )
            board_manager.connections.append(new_connection)


def render_empty_state():
    """Render empty state when no nodes exist"""

    st.markdown("""
    <div style='text-align: center; padding: 100px 20px; color: #666;'>
        <h2>🎨 Welcome to Your Flow Board!</h2>
        <p style='font-size: 18px; margin: 20px 0;'>
            Start building your workflow by adding nodes from the sidebar
        </p>
        <p style='font-size: 14px;'>
            • Click on node types in the sidebar to add them<br>
            • Drag nodes around to position them<br>
            • Connect nodes by dragging from output to input ports<br>
            • Use the controls to organize and manage your flow
        </p>
    </div>
    """, unsafe_allow_html=True)
