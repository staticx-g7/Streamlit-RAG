# src/components/node_editor.py
import streamlit as st
from core.board_manager import BoardManager


def render_node_editor():
    """Render the node editor panel"""

    board_manager = st.session_state.board_manager

    st.subheader("📝 Node Editor")

    if not board_manager.nodes:
        st.info("No nodes available. Create some nodes to get started!")
        return

    # Node selection
    if board_manager.selected_nodes:
        selected_id = board_manager.selected_nodes[0]
        selected_node = board_manager.nodes[selected_id]

        st.success(f"Selected: **{selected_node.title}**")

        # Node properties
        with st.expander("🔧 Properties", expanded=True):
            # Editable title
            new_title = st.text_input(
                "Title",
                value=selected_node.title,
                key="edit_node_title"
            )
            if new_title != selected_node.title:
                selected_node.title = new_title
                st.rerun()

            # Position
            col1, col2 = st.columns(2)
            with col1:
                new_x = st.number_input(
                    "X Position",
                    value=selected_node.x,
                    step=10.0,
                    key="edit_node_x"
                )
            with col2:
                new_y = st.number_input(
                    "Y Position",
                    value=selected_node.y,
                    step=10.0,
                    key="edit_node_y"
                )

            if new_x != selected_node.x or new_y != selected_node.y:
                selected_node.x = new_x
                selected_node.y = new_y
                st.rerun()

        # Node actions
        with st.expander("⚡ Actions"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🗑️ Delete", key="delete_node"):
                    board_manager.remove_node(selected_id)
                    st.success("Node deleted!")
                    st.rerun()

            with col2:
                if st.button("📋 Duplicate", key="duplicate_node"):
                    from ..core.node import Node

                    new_node = Node(
                        x=selected_node.x + 50,
                        y=selected_node.y + 50,
                        node_type=selected_node.node_type,
                        title=selected_node.title + " (Copy)",
                        color=selected_node.color
                    )

                    # Copy ports
                    for port in selected_node.input_ports:
                        new_node.add_input_port(port.name, port.data_type)
                    for port in selected_node.output_ports:
                        new_node.add_output_port(port.name, port.data_type)

                    board_manager.add_node(new_node)
                    st.success("Node duplicated!")
                    st.rerun()

        # Connection info
        node_connections = [
            conn for conn in board_manager.connections
            if conn.from_node_id == selected_id or conn.to_node_id == selected_id
        ]

        if node_connections:
            with st.expander(f"🔗 Connections ({len(node_connections)})"):
                for i, conn in enumerate(node_connections):
                    if conn.from_node_id == selected_id:
                        target_node = board_manager.nodes.get(conn.to_node_id)
                        if target_node:
                            st.write(f"→ {target_node.title}")
                    else:
                        source_node = board_manager.nodes.get(conn.from_node_id)
                        if source_node:
                            st.write(f"← {source_node.title}")

    else:
        # Node selection dropdown
        node_options = {
            f"{node.title} ({node.node_type})": node.id
            for node in board_manager.nodes.values()
        }

        selected_display = st.selectbox(
            "Select Node",
            options=["None"] + list(node_options.keys()),
            key="node_selector"
        )

        if selected_display != "None":
            selected_id = node_options[selected_display]
            board_manager.selected_nodes = [selected_id]
            board_manager.nodes[selected_id].selected = True

            # Clear other selections
            for node_id, node in board_manager.nodes.items():
                if node_id != selected_id:
                    node.selected = False

            st.rerun()
