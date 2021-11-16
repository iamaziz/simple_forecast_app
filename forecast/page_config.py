import datetime
from datetime import date

import streamlit as st


def APP_PAGE_HEADER():
    st.set_page_config(
        page_title="Simple Forecaster",
        page_icon=":camel:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    hide_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_style, unsafe_allow_html=True)
    HEADER()


def HEADER():
    st_ = st.columns(3)
    st_[0].markdown("> ## Simple Time-Series Forecast")
    today = date.today()

    st_[1].image(
        "./assets/logo.png",
        caption=f"{today.strftime('%B %d, %Y')}",
        use_column_width=True,
    )
