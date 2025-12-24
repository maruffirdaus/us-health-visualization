import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_cases_by_sleep_hours(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(
        f"##### {CONDITION_LABELS[selected_condition]} Case Distribution by Sleep Hours"
    )

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    with st.container(border=True):
        _plot_cases_by_sleep_hours(df_prepared)

    highest = df_prepared.loc[df_prepared["Number of Cases"].idxmax()]

    st.markdown(
        f"This chart shows the **distribution of {CONDITION_LABELS[selected_condition]} cases across different sleep durations**, illustrating how the number of reported cases varies by sleep hours. <mark>The highest recorded count occurs at {highest['Sleep Hours']:0.0f} hours with {highest['Number of Cases']:0.0f} cases</mark>, while other sleep durations show differing case levels across the range.",
        unsafe_allow_html=True,
    )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases.rename(columns={"SleepHours": "Sleep Hours"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = (
        df_cases.groupby("Sleep Hours", as_index=False)["Number of Cases"]
        .count()
        .reset_index()
    )

    return df_counts


def _plot_cases_by_sleep_hours(df: pd.DataFrame):
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Sleep Hours:Q", title="Sleep Hours", scale=alt.Scale(domain=[0, 24])
            ),
            y=alt.Y("Number of Cases:Q", title="Number of Cases"),
            tooltip=["Sleep Hours", "Number of Cases"],
        )
        .properties(
            title="",
            height=350,
        )
        .interactive()
    )

    st.altair_chart(chart)
