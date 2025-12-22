import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def plot_smoking_alcohol_interaction(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_copy = df.copy()

    if selected_state is not None:
        df_copy = df_copy[df_copy["State"] == selected_state]

    df_copy["SmokerStatus"] = df_copy["SmokerStatus"].apply(_simplify_smoker_status)

    df_copy.rename(columns={selected_condition: "Total Population"}, inplace=True)
    df_copy.rename(columns={"AlcoholDrinkers": "Alcohol Drinkers"}, inplace=True)
    df_copy.rename(columns={"SmokerStatus": "Smoker Status"}, inplace=True)

    df_pop = df_copy.groupby(["Alcohol Drinkers", "Smoker Status"], as_index=False)[
        "Total Population"
    ].count()

    df_copy.rename(columns={"Total Population": "Number of Cases"}, inplace=True)

    df_cases = df_copy[df_copy["Number of Cases"] == "Yes"]
    df_counts = df_cases.groupby(["Alcohol Drinkers", "Smoker Status"], as_index=False)[
        "Number of Cases"
    ].count()

    df_risk = df_pop.merge(
        df_counts, on=["Alcohol Drinkers", "Smoker Status"], how="left"
    ).fillna(0)
    df_risk["Case Ratio (%)"] = (
        df_risk["Number of Cases"] / df_risk["Total Population"] * 100
    ).round(2)

    color_scale = alt.Scale(scheme="orangered")

    chart = (
        alt.Chart(df_risk)
        .mark_circle(opacity=0.8)
        .encode(
            x=alt.X(
                "Smoker Status:N",
                title="Smoker Status",
                sort=["Never smoked", "Former smoker", "Current smoker"],
            ),
            y=alt.Y("Alcohol Drinkers:N", title="Alcohol Drinkers"),
            size=alt.Size(
                "Case Ratio (%):Q",
                title=f"{CONDITION_LABELS[selected_condition]} Ratio (%)",
                scale=alt.Scale(range=[100, 2000]),
            ),
            color=alt.Color(
                "Case Ratio (%):Q",
                scale=color_scale,
                legend=alt.Legend(
                    title=f"{CONDITION_LABELS[selected_condition]} Case Ratio (%)"
                ),
            ),
            tooltip=[
                "Smoker Status",
                "Alcohol Drinkers",
                "Total Population",
                "Number of Cases",
                "Case Ratio (%)",
            ],
        )
        .properties(
            title=f"Smoking & Alcohol Interaction: {CONDITION_LABELS[selected_condition]} Risk",
            height=350,
        )
        .interactive()
    )

    st.altair_chart(chart)


def _simplify_smoker_status(status):
    if "Current" in status:
        return "Current smoker"
    elif "Former" in status:
        return "Former smoker"
    elif "Never" in status:
        return "Never smoked"
    return status
