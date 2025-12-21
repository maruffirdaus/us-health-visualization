import streamlit as st

from components.us_map import render_us_map
from constants.conditions import CONDITION_LABELS
from services.data_loader import load_data

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

df = load_data("data/heart_2022_no_nans.csv")

st.set_page_config(page_title="US Health Visualization", page_icon="♥️", layout="wide")

st.markdown("# ♥️ US Health Visualization")
st.markdown(
    """
An interactive exploration of how lifestyle choices and personal health indicators vary across the U.S. population.

🔗 Data source: https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease
"""
)

col1, col2 = st.columns([3, 2], vertical_alignment="center")

with col1:
    st.markdown("## 2022 Overview")
with col2:
    selected_col = st.selectbox(
        "Select condition:",
        options=list(CONDITION_LABELS.keys()),
        format_func=lambda x: CONDITION_LABELS[x],
        label_visibility="collapsed",
    )

st.markdown("### Health Conditions Across the US")
st.markdown(
    f"This view shows the **number of people with {CONDITION_LABELS[selected_col]}** across the United States in 2022, providing a national overview. **Click on a state** to explore data and charts specific to that state."
)

with st.container(border=True):
    render_us_map(df, selected_col)

selected_state = st.session_state.selected_state

st.markdown(f"#### Overview by Variables - {selected_state or 'All US'}")
