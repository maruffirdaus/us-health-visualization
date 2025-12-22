import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def plot_cases_by_physical_activities(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases.rename(columns={"PhysicalActivities": "Physically Active"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = df_cases.groupby("Physically Active", as_index=False)[
        "Number of Cases"
    ].count()

    chart = (
        alt.Chart(df_counts)
        .mark_bar()
        .encode(
            x=alt.X(
                "Physically Active:N", sort=["No", "Yes"], title="Physically Active"
            ),
            y=alt.Y("Number of Cases:Q", title="Number of Cases"),
            color=alt.Color("Physically Active:N"),
            tooltip=["Physically Active", "Number of Cases"],
        )
        .properties(
            title=f"{CONDITION_LABELS[selected_condition]} Case Distribution by Physical Activities",
            height=350,
        )
        .interactive()
    )

    st.altair_chart(chart)
