import logging
import json
import os
import pandas as pd
import re


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

def data_quality_check(df: pd.DataFrame):
    """This module executes the following tasks:
        - Find and remove rows that have null values in essential columns
        - Remove junk characters from specific columns
        - Process phone column, splitting it into two new columns. Cast it as integer.
    """

    find_null(df, ["name", "phone", "location"])
    df, bad = remove_bad_rows(df)
    df["address"] = df["address"].apply(remove_junk_chars)
    df["reviews_list"] = df["reviews_list"].apply(remove_junk_chars)
    out = clean_phone(df)

    return out, bad

def output_files(out_df, bad_df):
    """Write to files the output of the process:
        - FILE_NAME.out -> All clean records
        - FILE_NAME.bad -> All bad records
        - FILE_NAME_bad_metadata.json -> Metadata corresponding to the .bad file
    """
    # Write FILE_NAME.out file
    out_df.to_csv(F"output/{FILE_NAME}.out")
    print(f"Saved file {FILE_NAME}.out")

    # Write FILE_NAME.bad file
    bad_df.to_csv(F"output/{FILE_NAME}.bad")
    print(f"Saved file {FILE_NAME}.bad")

    # Write FILE_NAME_bad_metadata.json file
    with open(F"output/{FILE_NAME}_bad_metadata.json", "w") as outfile:
        json.dump(BAD_SUMMARY, outfile)
    print(f"Saved file {FILE_NAME}_bad_metadata.json")

def file_check():
    """Checks for the following errors related to the input file:
        - Wrong extension (it must be .csv)
        - The file is empty
        - The file was already processed
    """
    # Check extension
    if extension != "csv":
        logging.warning('The file extension should be ".csv". Aborting processing.')
        return 1

    # Check if file is empty
    if os.stat(f"input/{file}").st_size == 0:
        logging.warning("The file is empty. Aborting processing.")
        return 1

    # Check if file was already processed
    if os.path.exists(f"output/{FILE_NAME}.out"):
        logging.warning("The file was already processed. Aborting processing.")
        return 1
    
    return 0

# Columns that will be preserved from the dataset
COLUMNS = [
    "url", "address", "name", "rate", 
    "votes", "phone", "location", "rest_type", 
    "dish_liked", "cuisines", "reviews_list"
]

# Dictionary to hold record of excluded rows
BAD_SUMMARY = {}

# File naming
file = "data_file_20210527182730.csv"
extension = file.split(".")[-1]
FILE_NAME = file.split(".")[0]

# Run file_check module
if file_check() == 0:

    # Read file
    print(f"Processing file {file} ...")
    raw = pd.read_csv(f"input/{file}", header=0, usecols=COLUMNS)

    # Run data_quality_check module
    out, bad = data_quality_check(raw)

    # Run output_files module
    print("Saving files...")
    output_files(out, bad)    

    print("PROCESS COMPLETED SUCCESFULLY!")