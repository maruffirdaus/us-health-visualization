import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_case_proportion_by_sex_age(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(
        f"##### {CONDITION_LABELS[selected_condition]} Case Proportion by Sex Across Age Categories"
    )

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    with st.container(border=True):
        _plot_case_proportion_by_sex_age(df_prepared, selected_condition)

    pivot = df_prepared.pivot(
        index="Age Category", columns="Sex", values="Number of Cases"
    ).reset_index()
    pivot["Total"] = pivot["Male"] + pivot["Female"]
    pivot["Male %"] = pivot["Male"] / pivot["Total"] * 100
    pivot["Female %"] = pivot["Female"] / pivot["Total"] * 100
    pivot["Imbalance"] = (pivot["Male %"] - pivot["Female %"]).abs()

    most_imbalanced = pivot.loc[pivot["Imbalance"].idxmax()]
    dominant_sex = (
        "Male" if most_imbalanced["Male %"] > most_imbalanced["Female %"] else "Female"
    )

    most_balanced = pivot.loc[pivot["Imbalance"].idxmin()]

    st.markdown(
        f"This chart shows the **proportion of {CONDITION_LABELS[selected_condition]} cases by sex across different age categories**, highlighting how male and female case shares vary as age increases. <mark>In {most_imbalanced['Age Category']}, {dominant_sex} accounts for a larger proportion ({most_imbalanced[f'{dominant_sex} %']:.2f}%), while {most_balanced['Age Category']} shows a more even distribution between sexes</mark>, indicating that sex-related differences in {CONDITION_LABELS[selected_condition]} cases may change across age groups.",
        unsafe_allow_html=True,
    )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases["AgeCategory"] = df_cases["AgeCategory"].apply(_simplify_age)
    df_cases.rename(columns={"AgeCategory": "Age Category"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = (
        df_cases.groupby(["Age Category", "Sex"], as_index=False)["Number of Cases"]
        .count()
        .reset_index()
    )

    return df_counts


def _plot_case_proportion_by_sex_age(df: pd.DataFrame, selected_condition: str):
    simple_age_order = ["<45 Years", "45-64 Years", "65-79 Years", ">=80 Years"]

    color_scale = alt.Scale(domain=["Male", "Female"], range=["#1f77b4", "#ff7f0e"])

    chart = (
        alt.Chart(df)
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
            title="",
            height=350,
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
