# Data Quality Test

This respository presents an example of a pipeline application for performing some data analysis and data cleaning.
It's desigend to receive files on a daily basis and pass them through 3 modules.

## Processing Modules 
- File Check Module: Responsible of validating the integrity of the file itself. Checking that the expected extension is correct, that the file is not empty, and that this same file hasn't been processed before.

- Data Quality Check Module: Data exploration is performed and rows that will not be part of the final dataset (due to the existence of null values) will be separated from the final data. After this, data cleaning starts, removing junk characters, splitting data into new columns and formatting columns into specific data types.

- Output Files Module: Saves the output into three files:
    * .out -> Containing the cleaned data 
    * .bad -> Containing the bad data 
    * .json -> Containing metadata related to the .bad file

### Dependencies
- pandas

## Running the pipeline

The files to be processed are expected to be inside de folder `input`. 

To start the pipeline, simply run the following command, adding the name of the file to process:
    
    /data_quality_test> $ python pipeline.py <file_to_process>

Once the pipeline runs successfully, the processed files will be saved into the folder `output`

## Examples of runs

### - Successful run
        /data_quality_test> $ python pipeline.py data_file_20210528182844.csv
        Processing file data_file_20210528182844.csv ...
        Saving files...
        Saved file data_file_20210528182844.out
        Saved file data_file_20210528182844.bad
        Saved file data_file_20210528182844_bad_metadata.json
        PROCESS COMPLETED SUCCESSFULLY!

### - File was already processed 
        /data_quality_test> $ python pipeline.py data_file_20210527182730.csv 
        WARNING:root:The file was already processed. Aborting processing.

### - Wrong file extension
        /data_quality_test> $ python pipeline.py data_file_20210527182730.txt
        WARNING:root:The file extension should be ".csv". Aborting processing.
