## Data Quality Test

This respository presents an example of an application for performing some data analysis and data cleaning.
It's desigend to receive files on a daily basis and pass them through 3 modules.

### Processing Modules 
- File Check Module: Responsible of validating the integrity of the file itself. Checking that the expected extension is correct, that the file is not empty, and that this same file hasn't been processed before.

- Data Quality Check Module: Data exploration is performed and rows that will not be part of the final dataset (due to the existence of null values) will be separated from the final data. After this, data cleaning starts, removing junk characters, splitting data into new columns and formatting columns into specific data types.

- Output Files Module: Saves the output into three files:
    * .out -> Containing the cleaned data 
    * .bad -> Containing the bad data 
    * .json -> Containing metadata related to the .bad file