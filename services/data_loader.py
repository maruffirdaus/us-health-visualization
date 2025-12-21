import pandas as pd
import streamlit as st

from constants.us_states import STATE_NAME_TO_CODE


@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df["StateCode"] = df["State"].map(STATE_NAME_TO_CODE)
    return df
