import streamlit as st
import pandas as pd
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState

st.title("🎈 My new app")
st.write(
    "Let's start building a userjourney flow"
)
# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=['xls', 'xlsx'])

if uploaded_file:
    # Load data from uploaded Excel file
    xlsx = pd.ExcelFile(uploaded_file)
    nodes_df = pd.read_excel(xlsx, 'Nodes')
    edges_df = pd.read_excel(xlsx, 'Edges')

    # Convert Timestamp columns to string if they exist
    for column in nodes_df.columns:
        if nodes_df[column].dtype == 'datetime64[ns]':
            nodes_df[column] = nodes_df[column].astype(str)
    
    for column in edges_df.columns:
        if edges_df[column].dtype == 'datetime64[ns]':
            edges_df[column] = edges_df[column].astype(str)

    # Create nodes
    nodes = []
    for index, row in nodes_df.iterrows():
        node = StreamlitFlowNode(
            id=str(row['id']),
            pos=(row['pos_x'], row['pos_y']),
            data={'content': row['content']},
            node_type=row['node_type'],
            source_position=row.get('source_position'),
            target_position=row.get('target_position')
        )
        nodes.append(node)

    # Create edges
    edges = []
    for index, row in edges_df.iterrows():
        edge = StreamlitFlowEdge(
            id=row['id'],
            source=str(row['source']),
            target=str(row['target']),
            animated=bool(row['animated'])
        )
        edges.append(edge)

    # Create flow state
    state = StreamlitFlowState(nodes, edges)

    # Render flow diagram in Streamlit
    streamlit_flow(
        'minimap_controls_flow',
        state,
        fit_view=True,
        show_minimap=True,
        show_controls=True,
        hide_watermark=True
    )
else:
    st.warning("Please upload an Excel file to proceed.")
