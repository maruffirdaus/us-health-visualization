import streamlit as st

from components.case_percentage_by_general_health import \
    render_case_percentage_by_general_health
from components.case_proportion_by_sex_age import \
    render_case_proportion_by_sex_age
from components.case_ratio_smoking_vs_vape import \
    render_case_ratio_smoking_vs_vape
from components.cases_by_physical_activities import \
    render_cases_by_physical_activities
from components.cases_by_sleep_hours import render_cases_by_sleep_hours
from components.risk_percentage_by_age import render_risk_percentage_by_age
from components.smoking_alcohol_interaction import \
    render_smoking_alcohol_interaction
from components.us_map import render_us_map
from constants.conditions import CONDITION_LABELS
from services.data_loader import load_data

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

df = load_data("data/heart_2022_no_nans.csv")

st.set_page_config(page_title="U.S. Health Visualization", page_icon="♥️", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# ♥️ U.S. Health Visualization")
st.markdown(
    """
An interactive exploration of how lifestyle choices and personal health indicators vary across the U.S. population.

🔗 Data source: https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease
"""
)

st.markdown("## 2022 Overview 📅")

title_col, selector_col = st.columns([3, 2], vertical_alignment="center")

with title_col:
    st.markdown("### Health Conditions Across the U.S.")
with selector_col:
    selected_condition = st.selectbox(
        "Select condition:",
        options=list(CONDITION_LABELS.keys()),
        format_func=lambda x: CONDITION_LABELS[x],
        label_visibility="collapsed",
    )

st.markdown(
    f"This view shows a national overview of {CONDITION_LABELS[selected_condition]} in the United States for 2022. **Select a state** to view state-level trends and visualizations."
)

render_us_map(df, selected_condition)

selected_state = st.session_state.selected_state

st.markdown(f"#### Overview by Variables - {selected_state or 'All U.S.'}")
st.markdown(f"View key health metrics for {selected_state or 'All U.S'}.")

render_risk_percentage_by_age(df, selected_condition, selected_state)
render_case_proportion_by_sex_age(df, selected_condition, selected_state)
render_cases_by_sleep_hours(df, selected_condition, selected_state)
render_smoking_alcohol_interaction(df, selected_condition, selected_state)
render_case_ratio_smoking_vs_vape(df, selected_condition, selected_state)
render_case_percentage_by_general_health(df, selected_condition, selected_state)
render_cases_by_physical_activities(df, selected_condition, selected_state)
