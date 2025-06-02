# src/components/board.py
import streamlit as st
import plotly.graph_objects as go
from core.board_manager import BoardManager


def render_infinite_board():
    """Render the main infinite board component"""

    board_manager = st.session_state.board_manager

    # Create the board visualization
    fig = create_board_figure(board_manager)

    # Display the board - Remove the click event handling for now
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="main_board",
        config={'displayModeBar': False}
    )

    # Alternative: Handle selection through session state
    handle_node_selection(board_manager)


def handle_node_selection(board_manager):
    """Handle node selection through Streamlit widgets"""

    if board_manager.nodes:
        st.subheader("Node Selection")

        node_options = ["None"] + [
            f"{node.title} ({node.id[:8]}...)"
            for node in board_manager.nodes.values()
        ]

        selected_option = st.selectbox(
            "Select a node to edit:",
            options=node_options,
            key="node_selection_board"
        )

        if selected_option != "None":
            # Find the selected node
            for node in board_manager.nodes.values():
                node_display = f"{node.title} ({node.id[:8]}...)"
                if node_display == selected_option:
                    # Clear previous selections
                    for n in board_manager.nodes.values():
                        n.selected = False

                    # Select the current node
                    node.selected = True
                    board_manager.selected_nodes = [node.id]
                    break


def create_board_figure(board_manager: BoardManager):
    """Create the Plotly figure for the board"""

    fig = go.Figure()

    # Add grid
    add_grid_to_figure(fig, board_manager)

    # Add nodes
    add_nodes_to_figure(fig, board_manager)

    # Add connections
    add_connections_to_figure(fig, board_manager)

    # Configure layout
    configure_figure_layout(fig, board_manager)

    return fig


def add_grid_to_figure(fig, board_manager):
    """Add grid lines to the figure"""

    zoom = board_manager.zoom_level
    center_x = board_manager.center_x
    center_y = board_manager.center_y

    grid_spacing = 50 / zoom
    grid_range = 500 / zoom

    # Vertical lines
    for x in range(int(center_x - grid_range), int(center_x + grid_range), int(grid_spacing)):
        fig.add_shape(
            type="line",
            x0=x, y0=center_y - grid_range,
            x1=x, y1=center_y + grid_range,
            line=dict(color="rgba(200,200,200,0.3)", width=1)
        )

    # Horizontal lines
    for y in range(int(center_y - grid_range), int(center_y + grid_range), int(grid_spacing)):
        fig.add_shape(
            type="line",
            x0=center_x - grid_range, y0=y,
            x1=center_x + grid_range, y1=y,
            line=dict(color="rgba(200,200,200,0.3)", width=1)
        )


def add_nodes_to_figure(fig, board_manager):
    """Add nodes to the figure"""

    if not board_manager.nodes:
        return

    # Prepare node data
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_ids = []

    for node in board_manager.nodes.values():
        node_x.append(node.x + node.width / 2)  # Center point
        node_y.append(node.y + node.height / 2)
        node_text.append(node.title)
        node_colors.append(node.color if not node.selected else '#FF0000')
        node_ids.append(node.id)

    # Add scatter plot for nodes
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=30,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        text=node_text,
        textposition="middle center",
        textfont=dict(size=10, color='white'),
        customdata=node_ids,
        name="Nodes",
        hovertemplate="<b>%{text}</b><br>ID: %{customdata}<extra></extra>"
    ))


def add_connections_to_figure(fig, board_manager):
    """Add connections to the figure"""

    for connection in board_manager.connections:
        from_node = board_manager.nodes.get(connection.from_node_id)
        to_node = board_manager.nodes.get(connection.to_node_id)

        if from_node and to_node:
            fig.add_shape(
                type="line",
                x0=from_node.x + from_node.width / 2,
                y0=from_node.y + from_node.height / 2,
                x1=to_node.x + to_node.width / 2,
                y1=to_node.y + to_node.height / 2,
                line=dict(color="rgba(76, 175, 80, 0.8)", width=3)
            )


def configure_figure_layout(fig, board_manager):
    """Configure the figure layout"""

    zoom = board_manager.zoom_level
    center_x = board_manager.center_x
    center_y = board_manager.center_y

    fig.update_layout(
        title="Infinite Node Board",
        showlegend=False,
        height=600,
        xaxis=dict(
            range=[center_x - 400 / zoom, center_x + 400 / zoom],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[center_y - 300 / zoom, center_y + 300 / zoom],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(248,249,250,1)',
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=40, b=0)
    )
