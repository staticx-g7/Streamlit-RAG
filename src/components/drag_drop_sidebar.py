# src/components/drag_drop_sidebar.py
import streamlit as st
from config.node_types import NodeType, NODE_TYPE_CONFIG
from config.settings import AppConfig
from core.board_manager import BoardManager


def render_drag_drop_sidebar():
    """Render drag-and-drop sidebar with node palette"""

    with st.sidebar:
        st.header("🎨 Node Palette")

        board_manager = st.session_state.board_manager

        # Node creation section
        render_node_palette()

        st.divider()

        # Board controls
        render_board_controls(board_manager)

        st.divider()

        # Statistics
        render_board_stats(board_manager)


def render_node_palette():
    """Render draggable node palette"""

    st.subheader("🔧 Drag to Create")
    st.markdown("*Click to add nodes to the board*")

    # Create draggable node buttons for each type
    for node_type, config in NODE_TYPE_CONFIG.items():
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"<div style='font-size: 24px; text-align: center;'>{config['icon']}</div>",
                        unsafe_allow_html=True)

        with col2:
            if st.button(
                    config['display_name'],
                    key=f"create_{node_type.value}",
                    help=f"Click to add {config['display_name']} node",
                    use_container_width=True
            ):
                add_node_to_board(node_type.value, config)


def add_node_to_board(node_type: str, config: dict):
    """Add a new node to the board"""
    from core.node import Node
    import random

    board_manager = st.session_state.board_manager

    # Create node at random position
    new_node = Node(
        x=random.randint(50, 300),
        y=random.randint(50, 300),
        node_type=node_type,
        title=config['display_name'],
        color=config['color']
    )

    # Add default ports
    for i in range(config['default_ports']['inputs']):
        new_node.add_input_port(f"Input {i + 1}")
    for i in range(config['default_ports']['outputs']):
        new_node.add_output_port(f"Output {i + 1}")

    board_manager.add_node(new_node)
    st.success(f"✅ Added {config['display_name']}!")
    st.rerun()


def render_board_controls(board_manager: BoardManager):
    """Render board control buttons"""

    st.subheader("🎛️ Controls")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 Sample", help="Add sample nodes", use_container_width=True):
            add_sample_nodes(board_manager)
            st.success("Sample nodes added!")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear", help="Clear all nodes", use_container_width=True):
            board_manager.nodes.clear()
            board_manager.connections.clear()
            board_manager.selected_nodes.clear()
            st.success("Board cleared!")
            st.rerun()

    # Auto-layout button
    if st.button("🔄 Auto Layout", help="Automatically arrange nodes", use_container_width=True):
        auto_layout_nodes(board_manager)
        st.success("Nodes arranged!")
        st.rerun()

    # Export/Import
    st.markdown("**💾 Data**")

    if st.button("📤 Export", help="Export board", use_container_width=True):
        export_data = board_manager.export_board_data()
        st.download_button(
            label="⬇️ Download JSON",
            data=export_data,
            file_name=f"flow_board_{board_manager.get_timestamp()}.json",
            mime="application/json",
            use_container_width=True
        )


def auto_layout_nodes(board_manager: BoardManager):
    """Automatically arrange nodes in a grid layout"""
    if not board_manager.nodes:
        return

    nodes = list(board_manager.nodes.values())
    cols = int(len(nodes) ** 0.5) + 1

    for i, node in enumerate(nodes):
        row = i // cols
        col = i % cols
        node.x = col * 200 + 50
        node.y = row * 150 + 50


def add_sample_nodes(board_manager: BoardManager):
    """Add sample nodes for demonstration"""
    from core.node import Node

    sample_data = [
        {"x": 100, "y": 100, "type": "input", "title": "Data Source"},
        {"x": 350, "y": 100, "type": "process", "title": "Transform"},
        {"x": 600, "y": 100, "type": "output", "title": "Result"},
        {"x": 225, "y": 250, "type": "filter", "title": "Filter"},
        {"x": 475, "y": 250, "type": "analytics", "title": "Analytics"}
    ]

    for data in sample_data:
        config = NODE_TYPE_CONFIG[NodeType(data["type"])]
        node = Node(
            x=data["x"], y=data["y"],
            node_type=data["type"],
            title=data["title"],
            color=config['color']
        )

        # Add ports
        for i in range(config['default_ports']['inputs']):
            node.add_input_port(f"Input {i + 1}")
        for i in range(config['default_ports']['outputs']):
            node.add_output_port(f"Output {i + 1}")

        board_manager.add_node(node)


def render_board_stats(board_manager: BoardManager):
    """Render board statistics"""

    st.subheader("📊 Stats")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nodes", len(board_manager.nodes))
        st.metric("Connections", len(board_manager.connections))

    with col2:
        if board_manager.selected_nodes:
            st.metric("Selected", len(board_manager.selected_nodes))
        else:
            st.metric("Selected", 0)

        if board_manager.nodes:
            node_types = [node.node_type for node in board_manager.nodes.values()]
            most_common = max(set(node_types), key=node_types.count)
            st.metric("Common", most_common.title())
