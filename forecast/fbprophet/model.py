import streamlit as st
import pandas as pd
from prophet import Prophet


@st.experimental_singleton
class ProphetModel:
    @staticmethod
    def predict(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        st1, st2 = st.columns(2)
        params = {
            "growth": kwargs.get("growth", "linear"),
            "interval_width": kwargs.get("interval_width", 0.95),
        }
        # st.write(params)
        st.write(kwargs)
        if "cap" in kwargs:
            df["cap"] = float(kwargs.get("cap"))
        period = kwargs.get("period", 7)

        # -- train model
        m = Prophet(**params)
        m.fit(df)

        future = m.make_future_dataframe(periods=period)
        if "cap" in kwargs:
            future["cap"] = float(kwargs.get("cap"))
        forecast = m.predict(future)

        # -- display output
        cols = ["ds", "yhat", "yhat_lower", "yhat_upper"]

        temp_ = forecast.copy()
        temp_["ds"] = temp_["ds"].apply(lambda x: x.strftime("%Y-%m-%d"))
        st.write(f"future={period}days")
        st.write(temp_[cols])

        fig1 = m.plot(forecast)
        fig2 = m.plot_components(forecast)

        from prophet.plot import plot_plotly, plot_components_plotly

        st1.markdown("> forecasts")
        st1.plotly_chart(plot_plotly(m, forecast, trend=True), use_container_width=True)
        st2.markdown("> forecast components")
        st2.plotly_chart(plot_components_plotly(m, forecast), use_container_width=True)

        # -- download results
        from forecast.utils import get_table_download_link

        st.markdown(get_table_download_link(forecast), unsafe_allow_html=True)

        st.success("Forecast completed ✨")

        return df
