import altair as alt
import pandas as pd
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_cases_by_physical_activities(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(
        f"##### {CONDITION_LABELS[selected_condition]} Case Distribution by Physical Activities"
    )

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    cols = st.columns([3, 2])

    with cols[0].container(border=True):
        _plot_cases_by_physical_activities(df_prepared)

    with cols[1]:
        physical_activities_labels = {
            "Yes": "physically active",
            "No": "physically inactive",
        }

        df_sorted = df_prepared.sort_values(by="Number of Cases", ascending=False)

        st.markdown(
            f"This chart shows the **distribution of {CONDITION_LABELS[selected_condition]} cases by physical activity status**, comparing individuals who are physically active with those who are not. <mark>A higher number of cases is observed among {physical_activities_labels[df_sorted.iloc[0]['Physically Active']]} individuals ({df_sorted.iloc[0]['Number of Cases']}) compared with {physical_activities_labels[df_sorted.iloc[1]['Physically Active']]} individuals ({df_sorted.iloc[1]['Number of Cases']})</mark>, highlighting a difference in case counts between the two activity groups.",
            unsafe_allow_html=True,
        )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_cases.rename(columns={"PhysicalActivities": "Physically Active"}, inplace=True)
    df_cases.rename(columns={selected_condition: "Number of Cases"}, inplace=True)

    df_counts = (
        df_cases.groupby("Physically Active", as_index=False)["Number of Cases"]
        .count()
        .reset_index()
    )

    return df_counts


def _plot_cases_by_physical_activities(df: pd.DataFrame):
    chart = (
        alt.Chart(df)
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
            title="",
            height=350,
        )
        .interactive()
    )

    st.altair_chart(chart)
