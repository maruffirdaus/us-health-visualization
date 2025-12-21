import pandas as pd
import plotly.express as px
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_us_map(df: pd.DataFrame, selected_col: str):
    count_df = (
        df[df[selected_col] == "Yes"]
        .groupby(["State", "StateCode"])
        .size()
        .reset_index(name=selected_col)
    )

    fig = px.choropleth(
        count_df,
        locations="StateCode",
        locationmode="USA-states",
        color=selected_col,
        scope="usa",
        hover_name="State",
        hover_data={"StateCode": False, selected_col: True},
        labels={selected_col: CONDITION_LABELS[selected_col]},
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
