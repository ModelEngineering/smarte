import pandas as pd


UNNAMED = "Unnamed:"
INDEX = "index"


def cleanDf(df, others=None):
    """
    Eliminates suprious columns in a dataframe.
    
    Parameters
    ----------
    df: DataFrame
    others: list-str (other column substrings)
    
    Returns
    -------
    DataFrame
    """
    new_df = df.copy()
    if others is None:
        others = []
    delete_stgs = list(others)
    delete_stgs.extend([UNNAMED, INDEX])
    columns = list(new_df.columns)
    for column in columns:
        for stg in delete_stgs:
            if stg in column:
                if column in new_df.columns:
                    del new_df[column]
    return new_df
