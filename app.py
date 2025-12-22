import streamlit as st

from components.case_percentage_by_general_health import \
    plot_case_percentage_by_general_health
from components.case_proportion_by_sex_age import \
    plot_case_proportion_by_sex_age
from components.case_ratio_smoking_vs_vape import \
    plot_case_ratio_smoking_vs_vape
from components.cases_by_physical_activities import \
    plot_cases_by_physical_activities
from components.cases_by_sleep_hours import plot_cases_by_sleep_hours
from components.risk_percentage_by_age import plot_risk_percentage_by_age
from components.smoking_alcohol_interaction import \
    plot_smoking_alcohol_interaction
from components.us_map import plot_us_map
from constants.conditions import CONDITION_LABELS
from services.data_loader import load_data

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

df = load_data("data/heart_2022_no_nans.csv")

st.set_page_config(page_title="U.S. Health Visualization", page_icon="♥️", layout="wide")

st.markdown("# ♥️ U.S. Health Visualization")
st.markdown(
    """
An interactive exploration of how lifestyle choices and personal health indicators vary across the U.S. population.

🔗 Data source: https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease
"""
)

st.markdown("## 2022 Overview 📅")

cols = st.columns([3, 2], vertical_alignment="center")

with cols[0]:
    st.markdown("### Health Conditions Across the U.S.")
with cols[1]:
    selected_condition = st.selectbox(
        "Select condition:",
        options=list(CONDITION_LABELS.keys()),
        format_func=lambda x: CONDITION_LABELS[x],
        label_visibility="collapsed",
    )

st.markdown(
    f"This view shows the **number of people with {CONDITION_LABELS[selected_condition]}** across the United States in 2022, providing a national overview. **Click on a state** to explore data and charts specific to that state."
)

with st.container(border=True):
    plot_us_map(df, selected_condition)

selected_state = st.session_state.selected_state

st.markdown(f"#### Overview by Variables - {selected_state or 'All U.S.'}")
st.markdown(
    f"View key metrics for {selected_state or 'All U.S'}. Click on any state to see its data in detail, or view the data for the entire country."
)

cols = st.columns([2, 3])

with cols[0].container(border=True):
    plot_risk_percentage_by_age(df, selected_condition, selected_state)
with cols[1].container(border=True):
    plot_case_proportion_by_sex_age(df, selected_condition, selected_state)

with st.container(border=True):
    plot_cases_by_sleep_hours(df, selected_condition, selected_state)

cols = st.columns(2)

with cols[0].container(border=True):
    plot_smoking_alcohol_interaction(df, selected_condition, selected_state)

with cols[1].container(border=True):
    plot_case_ratio_smoking_vs_vape(df, selected_condition, selected_state)

cols = st.columns(2)

with cols[0].container(border=True):
    plot_case_percentage_by_general_health(df, selected_condition, selected_state)

with cols[1].container(border=True):
    plot_cases_by_physical_activities(df, selected_condition, selected_state)
