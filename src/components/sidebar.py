# src/components/sidebar.py
import streamlit as st
from core.board_manager import BoardManager  # Changed from ..core.board_manager
from config.node_types import NodeType, NODE_TYPE_CONFIG  # Changed from ..config.node_types
from config.settings import AppConfig


def render_main_sidebar():
    """Render the main application sidebar for the home page"""

    with st.sidebar:
        st.header("🎛️ Board Controls")

        # Get board manager
        board_manager = st.session_state.board_manager

        # View controls section
        render_view_controls(board_manager)

        st.divider()

        # Node creation section
        render_node_creation(board_manager)

        st.divider()

        # Board actions section
        render_board_actions(board_manager)

        st.divider()

        # Quick stats
        render_quick_stats(board_manager)


def render_view_controls(board_manager: BoardManager):
    """Render view control widgets"""

    st.subheader("🔍 View Controls")

    # Zoom control
    new_zoom = st.slider(
        "Zoom Level",
        min_value=AppConfig.MIN_ZOOM,
        max_value=AppConfig.MAX_ZOOM,
        value=board_manager.zoom_level,
        step=0.1,
        key="zoom_slider"
    )

    if new_zoom != board_manager.zoom_level:
        board_manager.zoom_level = new_zoom

    # Pan controls in a compact grid
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️", key="pan_left", help="Pan Left"):
            board_manager.center_x -= 50
    with col2:
        if st.button("🎯", key="reset_view", help="Reset View"):
            board_manager.center_x = 0.0
            board_manager.center_y = 0.0
            board_manager.zoom_level = AppConfig.DEFAULT_ZOOM
    with col3:
        if st.button("➡️", key="pan_right", help="Pan Right"):
            board_manager.center_x += 50

    col4, col5, col6 = st.columns(3)
    with col4:
        st.write("")  # Empty space
    with col5:
        if st.button("⬆️", key="pan_up", help="Pan Up"):
            board_manager.center_y += 50
    with col6:
        st.write("")  # Empty space

    col7, col8, col9 = st.columns(3)
    with col7:
        st.write("")  # Empty space
    with col8:
        if st.button("⬇️", key="pan_down", help="Pan Down"):
            board_manager.center_y -= 50
    with col9:
        st.write("")  # Empty space


def render_node_creation(board_manager: BoardManager):
    """Render node creation interface"""

    st.subheader("➕ Create Node")

    # Node type selection with icons
    node_type_options = {
        f"{config['icon']} {config['display_name']}": node_type.value
        for node_type, config in NODE_TYPE_CONFIG.items()
    }

    selected_display = st.selectbox(
        "Node Type",
        options=list(node_type_options.keys()),
        key="node_type_select"
    )

    selected_type = node_type_options[selected_display]

    # Position inputs in columns
    col1, col2 = st.columns(2)
    with col1:
        x_pos = st.number_input("X", value=0.0, key="node_x", step=10.0)
    with col2:
        y_pos = st.number_input("Y", value=0.0, key="node_y", step=10.0)

    # Node title
    node_title = st.text_input(
        "Title",
        value=NODE_TYPE_CONFIG[NodeType(selected_type)]['display_name'],
        key="node_title"
    )

    # Create button
    if st.button("Create Node", key="create_node", type="primary"):
        from core.node import Node  # Line 122: Changed from ..core.node import Node

        new_node = Node(
            x=x_pos,
            y=y_pos,
            node_type=selected_type,
            title=node_title,
            color=NODE_TYPE_CONFIG[NodeType(selected_type)]['color']
        )

        # Add default ports based on node type
        config = NODE_TYPE_CONFIG[NodeType(selected_type)]
        for i in range(config['default_ports']['inputs']):
            new_node.add_input_port(f"Input {i + 1}")
        for i in range(config['default_ports']['outputs']):
            new_node.add_output_port(f"Output {i + 1}")

        board_manager.add_node(new_node)
        st.success(f"✅ Created {node_title}!")
        st.rerun()


def render_board_actions(board_manager: BoardManager):
    """Render board-level actions"""

    st.subheader("🔧 Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 Sample", key="add_samples", help="Add sample nodes"):
            add_sample_nodes(board_manager)
            st.success("Sample nodes added!")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear", key="clear_board", help="Clear all nodes"):
            board_manager.nodes.clear()
            board_manager.connections.clear()
            board_manager.selected_nodes.clear()
            st.success("Board cleared!")
            st.rerun()

    # Export/Import
    st.markdown("**💾 Data Management**")

    # Export
    if st.button("📤 Export", key="export_board", help="Export board data"):
        export_data = board_manager.export_board_data()
        st.download_button(
            label="Download JSON",
            data=export_data,
            file_name=f"node_board_{board_manager.get_timestamp()}.json",
            mime="application/json",
            key="download_export"
        )

    # Import
    uploaded_file = st.file_uploader(
        "📥 Import",
        type=['json'],
        key="import_file",
        help="Import board data"
    )
    if uploaded_file is not None:
        try:
            board_manager.import_board_data(uploaded_file)
            st.success("✅ Board imported!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Import failed: {str(e)}")


def render_quick_stats(board_manager: BoardManager):
    """Render quick statistics"""

    st.subheader("📊 Quick Stats")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nodes", len(board_manager.nodes))
        st.metric("Selected", len(board_manager.selected_nodes))

    with col2:
        st.metric("Connections", len(board_manager.connections))
        if board_manager.nodes:
            node_types = [node.node_type for node in board_manager.nodes.values()]
            most_common = max(set(node_types), key=node_types.count)
            st.metric("Common Type", most_common.title())


def add_sample_nodes(board_manager: BoardManager):
    """Add sample nodes for demonstration"""
    from core.node import Node

    sample_nodes_data = [
        {"x": 0, "y": 0, "type": "input", "title": "Data Source"},
        {"x": 200, "y": 0, "type": "process", "title": "Transform"},
        {"x": 400, "y": 0, "type": "output", "title": "Result"},
        {"x": 100, "y": 150, "type": "filter", "title": "Filter"},
        {"x": 300, "y": -150, "type": "analytics", "title": "Analytics"}
    ]

    for node_data in sample_nodes_data:
        node = Node(
            x=node_data["x"],
            y=node_data["y"],
            node_type=node_data["type"],
            title=node_data["title"],
            color=NODE_TYPE_CONFIG[NodeType(node_data["type"])]['color']
        )

        # Add default ports
        config = NODE_TYPE_CONFIG[NodeType(node_data["type"])]
        for i in range(config['default_ports']['inputs']):
            node.add_input_port(f"Input {i + 1}")
        for i in range(config['default_ports']['outputs']):
            node.add_output_port(f"Output {i + 1}")

        board_manager.add_node(node)

    # Add some sample connections
    nodes = list(board_manager.nodes.values())
    if len(nodes) >= 3:
        # Connect first three nodes in sequence
        board_manager.add_connection(
            nodes[0].id, nodes[0].output_ports[0].id if nodes[0].output_ports else "",
            nodes[1].id, nodes[1].input_ports[0].id if nodes[1].input_ports else ""
        )
        board_manager.add_connection(
            nodes[1].id, nodes[1].output_ports[0].id if nodes[1].output_ports else "",
            nodes[2].id, nodes[2].input_ports[0].id if nodes[2].input_ports else ""
        )
