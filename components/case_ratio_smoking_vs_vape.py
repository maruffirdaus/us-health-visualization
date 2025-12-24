import pandas as pd
import plotly.express as px
import streamlit as st

from constants.conditions import CONDITION_LABELS


def render_case_ratio_smoking_vs_vape(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    st.markdown(
        f"##### {CONDITION_LABELS[selected_condition]} Case Ratio: Traditional Smoking vs Vape/E-Cig Use"
    )

    df_prepared = _prepare_data_frame(df, selected_condition, selected_state)

    with st.container(border=True):
        _plot_case_ratio_smoking_vs_vape(df_prepared, selected_condition)

    smoker_labels = {
        "Never smoked": "never smokers",
        "Former smoker": "former smokers",
        "Current smoker": "current smokers",
    }

    e_cig_labels = {
        "Never used e-cigarettes in my entire life": "never e-cigarette users",
        "Not at all (right now)": "non-current e-cigarette users",
        "Use them every day": "daily e-cigarette users",
        "Use them some days": "occasional e-cigarette users",
    }

    highest = df_prepared.loc[df_prepared["Case Ratio (%)"].idxmax()]

    st.markdown(
        f"This chart shows the **{CONDITION_LABELS[selected_condition]} case ratio across traditional smoking statuses, further grouped by vape or e-cigarette usage**. Within each smoking category, case ratios vary across vape usage groups, with <mark>the highest observed value occurring among {smoker_labels[highest['Traditional Smoker Status']]} and {e_cig_labels[highest['Vape/E-Cig Usage']]} at approximately {highest['Case Ratio (%)']}%</mark>. Overall, the chart highlights differences in {CONDITION_LABELS[selected_condition]} case ratios across combinations of smoking and vape use behaviors.",
        unsafe_allow_html=True,
    )


def _prepare_data_frame(
    df: pd.DataFrame, selected_condition: str, selected_state: str | None
):
    df_copy = df.copy()

    if selected_state is not None:
        df_copy = df_copy[df_copy["State"] == selected_state]

    df_copy["SmokerStatus"] = df_copy["SmokerStatus"].apply(_simplify_smoker_status)

    df_copy.rename(columns={selected_condition: "Total Population"}, inplace=True)
    df_copy.rename(columns={"SmokerStatus": "Traditional Smoker Status"}, inplace=True)
    df_copy.rename(columns={"ECigaretteUsage": "Vape/E-Cig Usage"}, inplace=True)

    df_pop = df_copy.groupby(
        ["Traditional Smoker Status", "Vape/E-Cig Usage"], as_index=False
    )["Total Population"].count()

    df_copy.rename(columns={"Total Population": "Number of Cases"}, inplace=True)

    df_cases = df_copy[df_copy["Number of Cases"] == "Yes"]
    df_counts = df_cases.groupby(
        ["Traditional Smoker Status", "Vape/E-Cig Usage"], as_index=False
    )["Number of Cases"].count()

    df_risk = df_pop.merge(
        df_counts, on=["Traditional Smoker Status", "Vape/E-Cig Usage"], how="left"
    ).fillna(0)
    df_risk["Case Ratio (%)"] = (
        df_risk["Number of Cases"] / df_risk["Total Population"] * 100
    ).round(2)

    return df_risk


def _plot_case_ratio_smoking_vs_vape(df: pd.DataFrame, selected_condition: str):
    smoker_order = [
        "Never smoked",
        "Former smoker",
        "Current smoker",
    ]

    fig = px.bar(
        df,
        x="Traditional Smoker Status",
        y="Case Ratio (%)",
        color="Vape/E-Cig Usage",
        barmode="group",
        category_orders={"Traditional Smoker Status": smoker_order},
        title="",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Traditional Smoker Status",
        yaxis_title=f"{CONDITION_LABELS[selected_condition]} Case Ratio (%)",
        legend_title="Vape/E-Cig Usage",
    )

    st.plotly_chart(fig, height=350)


def _simplify_smoker_status(status):
    if "Current" in status:
        return "Current smoker"
    elif "Former" in status:
        return "Former smoker"
    elif "Never" in status:
        return "Never smoked"
    return status
