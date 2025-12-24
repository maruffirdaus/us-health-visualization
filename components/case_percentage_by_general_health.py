import pandas as pd
import plotly.express as px
import streamlit as st

from constants.conditions import CONDITION_LABELS

_general_health_order = ["Poor", "Fair", "Good", "Very Good", "Excellent"]


def render_case_percentage_by_general_health(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(
        f"##### {CONDITION_LABELS[selected_condition]} Case Percentage by General Health"
    )

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    cols = st.columns([3, 2])

    with cols[0].container(border=True):
        _plot_case_percentage_by_general_health(df_prepared)

    with cols[1]:
        df_sorted = df_prepared.sort_values(
            by="Case Percentage (%)", ascending=False
        ).head(2)

        st.markdown(
            f"This chart shows **the percentage distribution of {CONDITION_LABELS[selected_condition]} cases across general health categories**, where the categories themselves represent overall health status ranging from Poor to Excellent. <mark>The largest share of cases is observed in the {df_sorted.iloc[0]['General Health']} category at approximately {df_sorted.iloc[0]['Case Percentage (%)']}%, followed by {df_sorted.iloc[1]['General Health']} with {df_sorted.iloc[1]['Case Percentage (%)']}%</mark>, while other health categories account for smaller proportions of cases.",
            unsafe_allow_html=True,
        )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_cases = df[df[selected_condition] == "Yes"]

    if selected_state is not None:
        df_cases = df_cases[df_cases["State"] == selected_state]

    df_counts = df_cases.groupby("GeneralHealth", as_index=False)[
        selected_condition
    ].count()

    df_final = pd.DataFrame({"GeneralHealth": _general_health_order})
    df_final = df_final.merge(
        df_counts, left_on="GeneralHealth", right_on="GeneralHealth", how="left"
    ).fillna(0)

    total_cases = df_final[selected_condition].sum()

    df_final["Case Percentage (%)"] = (
        df_final[selected_condition] / total_cases * 100
    ).round(2)

    df_final.rename(columns={"GeneralHealth": "General Health"}, inplace=True)

    return df_final


def _plot_case_percentage_by_general_health(df: pd.DataFrame):
    fig = px.pie(
        df,
        values="Case Percentage (%)",
        names="General Health",
        category_orders={"General Health": _general_health_order},
        title="",
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent")

    st.plotly_chart(fig, height=350)
