import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def plot_cases_by_sleep_hours(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases.rename(columns={"SleepHours": "Sleep Hours"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = df_cases.groupby("Sleep Hours", as_index=False)[
        "Number of Cases"
    ].count()

    chart = (
        alt.Chart(df_counts)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Sleep Hours:Q", title="Sleep Hours", scale=alt.Scale(domain=[0, 24])
            ),
            y=alt.Y("Number of Cases:Q", title="Number of Cases"),
            tooltip=["Sleep Hours", "Number of Cases"],
        )
        .properties(
            title=f"{CONDITION_LABELS[selected_condition]} Case Distribution by Sleep Hours",
            height=400,
        )
        .interactive()
    )

    st.altair_chart(chart)
