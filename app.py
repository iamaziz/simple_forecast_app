from forecast.page_config import APP_PAGE_HEADER

import streamlit as st
import pandas as pd

APP_PAGE_HEADER()


class InputData:
    @classmethod
    def get_data(cls) -> pd.DataFrame:
        """
        Datasets sources:
           avg_daily_air_temp_celsius_helsinki:  http://shorturl.at/gBR06

        Returns:

        """
        sample = st.selectbox(
            "Sample datasets",
            options=["", "sample1", "sample2", "avg_daily_air_temp_celsius_helsinki"],
        )
        if sample:
            file_ = f"data/{sample}.csv"
            return pd.read_csv(file_)

        uploaded_data = cls.read_file()
        if uploaded_data is not None:
            return uploaded_data

    @classmethod
    def read_file(cls):
        global DATE_FORMATTER

        file_ = st.file_uploader("Upload your dataset (csv file)")
        if not file_:
            st.stop()

        if file_:
            sep = st.selectbox("column sep", options=[",", ";", "|"])
            df = pd.read_csv(file_, sep=sep)

            cols = df.columns.tolist()

            # -- choose date/target columns
            st1, st3, st2 = st.columns(3)
            date_col = st1.selectbox(
                "Date column (x-axis / index)", options=[""] + cols
            )
            st.session_state.date_formatter = st2.text_input(
                "Optional: Date format e.g. %Y-%m-%d"
            )
            target = st3.selectbox(
                "Target column (y-axis / target variable)", options=[""] + cols
            )

            # -- display
            if date_col and target:
                df = df[[date_col, target]]
                return df
            st.write(df)
            st.stop()

        return file_

    @classmethod
    def preprocess_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ["ds", "y"]
        # -- date column
        try:
            date_formatter = (
                st.session_state.date_formatter
                if "date_formatter" in st.session_state
                else None
            )
            if date_formatter:
                st.write("hello")
                st.stop()
                df["ds"] = pd.to_datetime(
                    df["ds"], format=st.session_state.date_formatter
                )
            else:
                df["ds"] = pd.to_datetime(df["ds"]).dt.date
        except:
            st.error("Date column is not in correct format")
            st.write(df["ds"])
            st.stop()
        # -- target column
        df["y"] = df["y"].apply(lambda x: float(str(x).replace(",", "")))
        df["y"] = df["y"].astype(float)

        return df


class PredictionApp:
    @staticmethod
    def run_prediction(df: pd.DataFrame) -> pd.DataFrame:
        # -- prepare data and user input

        st1, st2 = st.columns(2)
        st1.write(df)
        st2.line_chart(df.set_index("ds"))

        segmented_df = PredictionApp.split_df_by_date(df)

        # -- future date picker
        n = segmented_df.shape[0]
        future = st.slider("Number of days to predict", 7, n * 2, value=int(n / 2))

        params = PredictionApp.user_input_model_params()
        run = st.button("Run")
        PredictionApp.display_prophet_docs()

        if not run:
            return

        # -- run prediction
        with st.spinner("running prediction engine .."):
            from forecast.fbprophet.model import ProphetModel

            model = ProphetModel()
            pred = model.predict(segmented_df, period=future, **params)
            return pred

    @staticmethod
    def split_df_by_date(df: pd.DataFrame) -> pd.DataFrame:
        # -- split dataframe by date
        st.caption("Choose the target fitting period")
        st1, st2 = st.columns(2)

        from_ = st1.date_input(
            "from", min_value=df.ds.min(), max_value=df.ds.max(), value=df.ds.min()
        )
        to_ = st2.date_input(
            "to", min_value=df.ds.min(), max_value=df.ds.max(), value=df.ds.max()
        )
        ix1 = df.index[df.ds == from_][0]
        ix2 = df.index[df.ds == to_][0]
        new_df = PredictionApp._displayed_segmented_dataframe(df, from_=ix1, to_=ix2)

        new_df.reset_index(inplace=True)
        st1.write(f"{new_df['ds'].min()}")
        st2.write(f"{new_df['ds'].max()}")
        return new_df

    @classmethod
    def _displayed_segmented_dataframe(
        cls, df: pd.DataFrame, from_: int, to_: int
    ) -> pd.DataFrame:
        df = df.set_index("ds")
        df_ = df[from_ : to_ + 1]
        st.line_chart(df_)
        return df_

    @classmethod
    def user_input_model_params(cls):
        raw_params = st.text_input(
            "Model params. Type param name and its value e.g. growth=logistic"
        )

        if raw_params:
            in_params = [x.strip() for x in raw_params.split(",")]
            params = {}
            for param in in_params:
                k, v = param.split("=")
                params[k] = float(v) if v.isdigit() else v

            if "growth" in params and params["growth"] == "logistic":
                cap = st.text_input("cap")
                if cap:
                    params["cap"] = float(cap)
                else:
                    st.warning("Cap is required for logistic growth")
                    st.stop()
            st.write("Your input params:")
            st.write(params)
            return params
        return {}

    @classmethod
    def display_prophet_docs(cls):
        from prophet import Prophet

        with st.expander("View model params"):

            st.write(Prophet.__doc__)
            st.markdown(
                "> more details: [visit](https://facebook.github.io/prophet/)",
                unsafe_allow_html=True,
            )


def app():
    data = InputData.get_data()
    data = InputData.preprocess_data(data)

    PredictionApp.run_prediction(data)


if __name__ == "__main__":
    app()
