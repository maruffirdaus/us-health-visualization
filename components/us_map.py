import pandas as pd
import plotly.express as px
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_us_map(df: pd.DataFrame, selected_condition: str):
    df_prepared = _prepare_data_frame(df, selected_condition)

    with st.container(border=True):
        _plot_us_map(df_prepared, selected_condition)

    highest = df_prepared.loc[df_prepared[selected_condition].idxmax()]
    lowest = df_prepared.loc[df_prepared[selected_condition].idxmin()]

    st.markdown(
        f"This map shows the **total number of {CONDITION_LABELS[selected_condition]} cases** across the United States, with <mark>{highest['State']} reporting the highest count ({highest[selected_condition]}) and {lowest['State']} the lowest ({lowest[selected_condition]})</mark>.",
        unsafe_allow_html=True,
    )


def _prepare_data_frame(df: pd.DataFrame, selected_condition: str):
    df_counts = (
        df[df[selected_condition] == "Yes"]
        .groupby(["State", "StateCode"])
        .size()
        .reset_index(name=selected_condition)
    )

    return df_counts


def _plot_us_map(df: pd.DataFrame, selected_condition: str):
    fig = px.choropleth(
        df,
        locations="StateCode",
        locationmode="USA-states",
        color=selected_condition,
        scope="usa",
        hover_name="State",
        hover_data={"StateCode": False, selected_condition: True},
        labels={selected_condition: CONDITION_LABELS[selected_condition]},
        color_continuous_scale="Reds",
    )

    fig.update_layout(geo=dict(showlakes=True, lakecolor="rgb(255,255,255)"))

    fig.update_coloraxes(colorbar_title="")

    event = st.plotly_chart(
        fig, use_container_width=True, on_select="rerun", selection_mode="points"
    )

    if len(event.selection["points"]) > 0:
        selected_state = event.selection["points"][0]["hovertext"]
        st.session_state.selected_state = selected_state
    else:
        st.session_state.selected_state = None
