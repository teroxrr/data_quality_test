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

def remove_junk_chars(string_data: str):
    """Remove junk characters"""

    clean = string_data.replace("\\n", "")
    clean = re.sub(r"[^a-zA-Z0-9/.]+", ' ', clean)
    return clean


def numeric_phone(phone: str):
    """Remove non numeric characters from phone number"""

    if type(phone) == str:
        numeric = ''.join(e for e in phone if e.isnumeric())
        return numeric


def clean_phone(df: pd.DataFrame):
    """Split phone column into two columns. Clean phone numbers. Cast columns to integer"""

    # Split "phone" column by line break ("\n")
    split_phone = df["phone"].str.split("\n", n=1, expand=True)
    # Create new columns
    df["phone_1"] = split_phone[0]
    df["phone_2"] = split_phone[1]
    # Drop original phone column
    df.drop(columns=["phone"], inplace=True)

    # Clean phone columns
    df["phone_1"] = df["phone_1"].apply(numeric_phone)
    df["phone_2"] = df["phone_2"].apply(numeric_phone)

    # Cast phone columns to integer
    df["phone_1"] = pd.to_numeric(df["phone_1"], errors='coerce').astype('Int64')
    df["phone_2"] = pd.to_numeric(df["phone_2"], errors='coerce').astype('Int64')

    return df



# Dictionary to hold record of excluded rows
BAD_SUMMARY = {}
