import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def plot_case_proportion_by_sex_age(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases["AgeCategory"] = df_cases["AgeCategory"].apply(_simplify_age)
    df_cases.rename(columns={"AgeCategory": "Age Category"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = df_cases.groupby(["Age Category", "Sex"], as_index=False)[
        "Number of Cases"
    ].count()

    simple_age_order = ["<45 Years", "45-64 Years", "65-79 Years", ">=80 Years"]
    color_scale = alt.Scale(domain=["Male", "Female"], range=["#1f77b4", "#ff7f0e"])

    chart = (
        alt.Chart(df_counts)
        .mark_bar()
        .encode(
            y=alt.Y("Age Category:N", sort=simple_age_order, title="Age Category"),
            x=alt.X(
                "Number of Cases:Q",
                stack="normalize",
                axis=alt.Axis(
                    title=f"{CONDITION_LABELS[selected_condition]} Case Proportion (%)",
                    format=".0%",
                ),
            ),
            color=alt.Color("Sex:N", scale=color_scale, legend=alt.Legend(title="Sex")),
            tooltip=[
                "Age Category",
                "Sex",
                alt.Tooltip("Number of Cases:Q", title="Number of Cases"),
            ],
        )
        .properties(
            title=f"{CONDITION_LABELS[selected_condition]} Case Proportion by Sex Across Age Categories",
            height=300,
        )
        .interactive()
    )

    st.altair_chart(chart)


def _simplify_age(age_category):
    if age_category in [
        "Age 18 to 24",
        "Age 25 to 29",
        "Age 30 to 34",
        "Age 35 to 39",
        "Age 40 to 44",
    ]:
        return "<45 Years"
    elif age_category in [
        "Age 45 to 49",
        "Age 50 to 54",
        "Age 55 to 59",
        "Age 60 to 64",
    ]:
        return "45-64 Years"
    elif age_category in ["Age 65 to 69", "Age 70 to 74", "Age 75 to 79"]:
        return "65-79 Years"
    elif age_category == "Age 80 or older":
        return ">=80 Years"
    return age_category
