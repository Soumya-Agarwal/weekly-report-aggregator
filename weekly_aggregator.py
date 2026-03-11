#This project helps - Combining weekly reports from multiple CSV files 

import pandas as pd #For Data Manipulation
from pathlib import Path #pathlib for file handling
import logging # To track issues without print statements

#configures how logs look

logging.basicConfig( 
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s' #every log line will show: `timestamp - level - message`
)

logger = logging.getLogger(__name__) #creates logger for this file - like an object 

#Define path for input folder, output_report and log_file

INPUT_FOLDER = Path("input_files")
OUTPUT_FILE = Path("consolidated_report.xlsx")
LOG_FILE = Path("data_quality_log.txt")

def main():
    logger.info("Starting weekly data aggregation")
    # creates the folder wherever your terminal is currently pointing
    # exist_ok = True : Meaning, do not crash if folder already exists
    INPUT_FOLDER.mkdir(exist_ok=True) 
    logger.info(f"Looking for CSV files in: {INPUT_FOLDER}")

    # create a list of files from input_folder ending in .csv 
    csv_files = list(INPUT_FOLDER.glob('*.csv')) #`glob` is pattern matching for files.
    logger.info(f"Found {len(csv_files)} CSV files")

    #Add all files to the df
    df = []
    for file in csv_files:
        logger.info(f"Reading File: {file.name}")
        curr_df = pd.read_csv(file)
        df.append(curr_df)
    
    # Creating one final combined df
    combined_df = pd.concat(df, ignore_index=True)
    logger.info(f"Total rows after combining: {len(combined_df)}")

    # Removing duplicate order ids from the combined df
    rows_before = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=["order_id"]) #subset defines the primary key
    rows_after = len(combined_df)
    logger.info(f"Dropped: {rows_before - rows_after} duplicate rows")

    # Identifying missing values
    missing_values = combined_df.isnull().sum()
    logger.info(f"Missing values per column:\n{missing_values}")

    # Creating meaningful summary
    summary = combined_df.groupby("State").agg(
        total_qty = ("quantity", "sum"),
        total_revenue = ("price", "sum"),
        order_count = ("order_id", "count")
    ).reset_index() 

    logger.info(f"Summary calculated for {len(summary)} products")

    # Write raw data and summary to excel using openpyxl
    with pd.ExcelWriter(OUTPUT_FILE, engine = "openpyxl") as writer:
        combined_df.to_excel(writer, sheet_name="Combined Orders Data", index=False)
        summary.to_excel(writer, sheet_name="Orders Summary", index=False)
    
    logger.info(f"Report exported to: {OUTPUT_FILE}")

    with open(LOG_FILE, "w") as f:
        f.write("DATA QUALITY REPORT\n")
        f.write("="*40 + "\n")
        f.write(f"Total rows after combining: {rows_before}\n")
        f.write(f"Duplicate rows removed: {rows_before - rows_after}\n")
        f.write(f"Missing values:\n{missing_values}\n")
    logger.info(f"Data quality log written to: {LOG_FILE}")
'''
"Only run this if someone runs THIS file directly —
not if another script imports it."
'''

if __name__ == "__main__":
    main()