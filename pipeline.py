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

def remove_bad_rows(df: pd.DataFrame):
    """Remove from the dataset the rows contained in the "BAD_SUMMARY" dictionary"""
    
    # Create empty set to store row numbers
    rows_to_exclude = set()
    for key in BAD_SUMMARY:
        # Add row numbers to set
        rows_to_exclude.update(BAD_SUMMARY[key])
    
    # Create "bad" dataframe
    bad = df.iloc[list(rows_to_exclude)]
    
    # Remove rows from dataset
    updated_df = df.drop(rows_to_exclude)
    
    return updated_df, bad


# Dictionary to hold record of excluded rows
BAD_SUMMARY = {}
