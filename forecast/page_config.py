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
    today = date.today()
    st_ = st.columns(2)
    st_[0].markdown("## Simple Time-Series Forecasting")
    st_[0].markdown("By [Aziz Alto](https://twitter.com/AzizAlto) on 11-14-2021")
    st_[0].caption(f"Today is {today.strftime('%B %d, %Y')}")

    review = """
    > _"Facebook's Prophet package aims to provide a simple, automated approach to prediction of a large number of different time series. The package employs an easily interpreted, three component additive model whose Bayesian posterior is sampled using STAN. In contrast to some other approaches, the user of Prophet might hope for good performance without tweaking a lot of parameters. Instead, hyper-parameters control how likely those parameters are a priori, and the Bayesian sampling tries to sort things out when data arrives.
    Judged by popularity, this is surely a good idea. Facebook's prophet package has been downloaded 13,698,928 times according to pepy. It tops the charts, or at least the one I compiled here where hundreds of Python time series packages were ranked by monthly downloads. Download numbers are easily gamed and deceptive but nonetheless, the Prophet package is surely the most popular standalone Python library for automated time series analysis."_

    continue reading [here](https://www.microprediction.com/blog/prophet).
    """

    st_[1].caption(f"For now - based fbprophet forecaster only.",)
    st_[1].image(
        "./assets/logo.png",
        use_column_width=True,
    )
    with st_[1].expander("about the model"):
        st.markdown(review, unsafe_allow_html=True)
    st.markdown("---")
