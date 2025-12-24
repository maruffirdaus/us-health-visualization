import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_risk_percentage_by_age(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(f"##### {CONDITION_LABELS[selected_condition]} Risk Percentage by Age")

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    cols = st.columns([3, 2])

    with cols[0].container(border=True):
        _plot_risk_percentage_by_age(df_prepared)

    with cols[1]:
        highest = df_prepared.loc[df_prepared["Risk Percentage (%)"].idxmax()]
        lowest = df_prepared.loc[df_prepared["Risk Percentage (%)"].idxmin()]

        st.markdown(
            f"This chart presents the **percentage distribution of {CONDITION_LABELS[selected_condition]} risk across different age groups**, with values ranging from {lowest['Risk Percentage (%)']}% in {lowest['Age Category']} to {highest['Risk Percentage (%)']}% in {highest['Age Category']}."
        )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_counts = df_cases.groupby("AgeCategory", as_index=False)[
        selected_condition
    ].count()

    age_order = [
        "Age 18 to 24",
        "Age 25 to 29",
        "Age 30 to 34",
        "Age 35 to 39",
        "Age 40 to 44",
        "Age 45 to 49",
        "Age 50 to 54",
        "Age 55 to 59",
        "Age 60 to 64",
        "Age 65 to 69",
        "Age 70 to 74",
        "Age 75 to 79",
        "Age 80 or older",
    ]

    df_final = pd.DataFrame({"AgeCategory": age_order})
    df_final = df_final.merge(
        df_counts, left_on="AgeCategory", right_on="AgeCategory", how="left"
    ).fillna(0)

    total_cases = df_final[selected_condition].sum()

    df_final["Risk Percentage (%)"] = (
        df_final[selected_condition] / total_cases * 100
    ).round(2)

    df_final.rename(columns={"AgeCategory": "Age Category"}, inplace=True)

    return df_final


def _plot_risk_percentage_by_age(df: pd.DataFrame):
    chart = (
        alt.Chart(df)
        .mark_arc(outerRadius=120)
        .encode(
            theta=alt.Theta("Risk Percentage (%):Q", stack=True),
            color=alt.Color("Age Category:N", legend=alt.Legend(title="Age Category")),
            order=alt.Order("Risk Percentage (%):Q", sort="descending"),
            tooltip=[
                "Age Category",
                alt.Tooltip("Risk Percentage (%):Q", format=".2f"),
            ],
        )
        .properties(
            title="",
            height=350,
        )
    )

    st.altair_chart(chart)
