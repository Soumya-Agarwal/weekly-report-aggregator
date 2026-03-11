MULTI-SOURCE DATA AGGREGATOR

Problem It Solves:
Combining weekly reports from multiple CSV files (common BA task)

What It Does:
* Reads all CSV files from a folder
* Validates data (checks for missing values, duplicates)
* Combines data intelligently
* Calculates summary statistics
* Exports consolidated Excel report
* Logs data quality issues

Sample Structure:
Input Folder : Add multiple csvs in this folder
Output files :consolidated_report.xlsx and data_quality_log.txt

Key Features:
* Data validation (missing values, data types)
* Deduplication
* Summary calculations (totals, averages)
* Formatted Excel output
* Error handling

Technologies:
* Pandas (data manipulation)
* openpyxl (Excel writing)
* pathlib (file handling)
* logging (error tracking)

File to Create:
`weekly_aggregator.py`
