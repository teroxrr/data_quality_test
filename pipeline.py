import pandas as pd

def find_null(df: pd.DataFrame, columns: list):
    """Find row numbers in the dataframe "df", corresponding to null values contained in the columns passed 
    in the list like "columns" argument.
    Store the row numbers as a new entry in the "BAD_SUMMARY" dictionary"""
    
    # Iterate over columns
    for column in columns:
        # Find row numbers corresponding to null values
        null_rows = list(df[df[column].isnull()].index)
        # Store row numbers
        if len(null_rows) > 0:
            BAD_SUMMARY[f"null_{column}"] = null_rows


# Dictionary to hold record of excluded rows
BAD_SUMMARY = {}
