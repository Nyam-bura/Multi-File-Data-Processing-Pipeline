# Multi-File-Data-Processing-Pipeline

## 1. Project Overview

The Multi-File Data Processing Pipeline is a Python project that reads transaction records from multiple CSV files, validates and cleans the data, identifies invalid and duplicate transactions, and produces consolidated output files.

The pipeline processes three input CSV files containing a total of 43 transaction records. It standardizes column names, including normalizing `qty` to `quantity`, checks required fields and numeric values, and detects duplicate transaction IDs.

After processing, valid transactions are saved to a cleaned CSV file, while rejected transactions are saved separately with their source filenames and rejection reasons.


## 2. Project Structure

```
multi-file-data-processing/
├── data/
│   ├── transactions_2026-10-01.csv
│   ├── transactions_2026-10-02.csv
│   └── transactions_2026-10-03.csv
├── output/
│   ├── Cleaned_transactions.csv
│   └── rejected_transactions.csv
├── pipeline.py
├── requirements.txt
└── README.md
```

- `data/` contains the input transaction CSV files.
- `output/` stores the generated cleaned and rejected transaction files.
- `pipeline.py` contains the file discovery, reading, validation, cleaning, and output logic.
- `requirements.txt` lists any external Python dependencies.
- `README.md` documents the project and explains how to run it.

## 3. Requirements and Installation

### Requirements

- Python 3.14.6 or a compatible Python 3 version.
- A code editor such as Visual Studio Code.
- CSV input files stored in the `data/` directory.

### Installation

1. Install Python if it is not already installed.
2. Download or clone the project repository.
3. Open the project folder in Visual Studio Code.
4. Open the integrated terminal and navigate to the project directory.
5. Ensure the input CSV files are available in the `data/` directory.

The pipeline uses Python's built-in modules and does not require additional package installation, provided no external libraries are imported in `pipeline.py`.

## 4. How to Run the Pipeline

1. Open the project folder in Visual Studio Code.
2. Open the terminal in the project directory.
3. Confirm that the three transaction CSV files are inside the `data/` directory.
4. Run the pipeline using:

```powershell
python pipeline.py
```

5. Review the processing summary displayed in the terminal.
6. Open the `output/` directory to view the cleaned and rejected transaction records.


The pipeline discovers the input files matching the `transactions_*.csv` pattern, processes their records, and saves the results in the output directory.

## 5. Validation and Cleaning Rules

The pipeline applies the following validation and cleaning rules:

- **Column normalization:** Renames the `qty` column to `quantity` to maintain consistent column naming.
- **Required fields:** Checks that required fields, including transaction ID, date, branch, customer ID, product, quantity, unit price, and payment method, are present and not blank.
- **Numeric validation:** Checks that quantity and unit price contain numeric values.
- **Positive values:** Rejects transactions where quantity or unit price is zero or negative.
- **Duplicate detection:** Identifies duplicate transaction IDs across the input files.
- **Data cleaning:** Removes unnecessary whitespace from string values and converts valid quantities to integers and unit prices to floating-point numbers.
- **Rejected records:** Stores invalid transactions separately and records the reasons for rejection, together with the source filename.

## 6. Output Files and Processing Summary

The pipeline generates two CSV output files in the `output/` directory.

### Cleaned_transactions.csv

Contains valid transaction records after validation and cleaning.

### rejected_transactions.csv

Contains rejected transaction records, their source filenames, and the reasons why they failed validation.

### Processing Summary

The pipeline processed 43 transaction records from three input CSV files.

 Input CSV files- 3 

Total records processed  43 

 Valid transactions  34 

 Rejected transactions  9 

The processing summary is displayed in the terminal after execution.
