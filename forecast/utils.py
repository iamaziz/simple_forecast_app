from datetime import datetime

import pandas as pd


def get_table_download_link(df: pd.DataFrame) -> str:
    """Generates a link for download the `df` locally as a csv file.

    Args:
        df: the dataframe to download

    Returns:
        href link
    """
    import base64

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="data_{datetime.now()}.csv">download</a>'


def filter_df(df: pd.DataFrame, filter_: str) -> pd.DataFrame:
    """Takes a dataframe and a `filter_` keyword, returns all the rows that contain the value `filter_` in any column

    Args:
        df: pandas dataframe
        filter_: the string to search in the dataframe

    Returns:
        filtered dataframe
    """
    import numpy as np

    mask = np.column_stack(
        [df[col].astype(str).str.contains(filter_, na=False) for col in df]
    )
    filtered_df = df.loc[mask.any(axis=1)]
    return filtered_df
