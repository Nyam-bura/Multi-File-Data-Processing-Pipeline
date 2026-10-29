from pathlib import Path
import pathlib
import csv


COLUMN_ALIASES = {
    "qty": "quantity",
}

def discover_files(folder:pathlib.Path,
    pattern:str="transactions_*.csv"
    ) -> list[pathlib.Path]:
    """ 
find all matching transactions csv files and return them in distorted order.
"""
    files = list(folder.glob(pattern))
    return files


def read_transactions(path: Path) -> tuple[list[str], list[dict]]:
    """
    Read one CSV file, normalize column names, and return its header and rows.
    """
    with path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        original_header = reader.fieldnames or []

        header = [
            COLUMN_ALIASES.get(column, column)
            for column in original_header
        ]

        rows = []

        for original_row in reader:
            row = {}

            for column in original_header:
                normalized_column = COLUMN_ALIASES.get(column, column)
                row[normalized_column] = original_row[column]

            row["source_file"] = path.name
            rows.append(row)

    return header, rows


REQUIRED_COLUMNS = {
    "transaction_id",
    "date",
    "branch",
    "customer_id",
    "product",
    "quantity",
    "unit_price",
    "payment_method",
}
def validate_columns(
    header: list[str],
    required: set[str] = REQUIRED_COLUMNS
) -> set[str]:
    """
    Return the required columns missing from the CSV header.
 """
    return required - set(header)

def find_problems(row:dict, seen_ids:set[str]) ->   list[str]:
    """"
    return human readable reasons why transactions row is invalid.
    """
    problems = []
    for column in REQUIRED_COLUMNS:
        value = row.get(column)
        if value is None or value.strip()=="":
            problems.append(f"Blank required value: {column}")
    try:
        quantity = float(row["quantity"])
        if quantity <= 0:
         problems.append("Quantity must be greater than zero")
    except(ValueError, TypeError):
        problems.append("Quantity must be numeric")
    try:
        unit_price = float(row["unit_price"])
        if unit_price <= 0:
         problems.append("Unit Price must be greater than zero")
    except(ValueError, TypeError):
        problems.append("Unit Price must be numeric")
    transaction_id = str(row.get("transaction_id", "")).strip()
    if transaction_id in seen_ids:
        problems.append(f"Duplicate transaction ID: {transaction_id}")
    return problems

def cleaned_row(row:dict) -> dict:
    """"
    clean whitespaces and standardize transaction data types.
    """
    cleaned = {}
    for column, value in row.items():
        if isinstance(value, str):
            cleaned[column] = value.strip()
        else:
            cleaned[column] = value
    cleaned["quantity"] = int(float(cleaned["quantity"]))
    cleaned["unit_price"] = float(cleaned["unit_price"])
    return cleaned

def write_csv(file_path:Path, rows:list[dict]) -> None:
    """
    Write a list of dictionaries to a csv file.
    """
    if not rows:
        print(f"No rows to write to {file_path}")
        return
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(
        column 
        for row in rows
        for column in row.keys()
    ))
    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {file_path}")
    
def prepare_rejected_rows(rejected_rows: list[dict]) -> list[dict]:
    output_rows = []
    for rejected in rejected_rows:
        row = rejected["row"].copy()
        row["source_file"] = rejected["source_file"]
        row["rejected_reason"] = "; ".join(rejected["errors"])
        output_rows.append(row)
    return output_rows

def build_summary(
    total_rows:int,
    valid_rows: list[dict],
    rejected_rows: list[dict],
)-> dict:
    rejection_counts = {}
    for rejected in rejected_rows:
        for reason in rejected["errors"]:
            rejection_counts[reason] = rejection_counts.get(reason,0) + 1
    return{
        "total_rows": total_rows,
        "valid_transactions": len(valid_rows),
        "rejected_transactions": len(rejected_rows),
        "rejection_reason": rejection_counts,
    }

if __name__ == "__main__":
    data_folder = Path("data")
    files = discover_files(data_folder)

    # Store valid and rejected transactions
    valid_rows = []
    rejected_rows = []

    # Track transaction IDs across all files
    seen_ids = set()

    for file_path in files:
        header, rows = read_transactions(file_path)
        missing = validate_columns(header)

        print(f"\nFile: {file_path.name}")
        print(f"Headers: {header}")
        print(f"Missing required columns: {missing}")

        if missing:
            print(f"Skipping {file_path.name}: missing columns {missing}")
            continue

        print(f"Processing {len(rows)} rows...")

        for row in rows:
            problems = find_problems(row, seen_ids)

            transaction_id = str(
                row.get("transaction_id", "")
            ).strip()

            # Remember each non-empty transaction ID
            if transaction_id:
                seen_ids.add(transaction_id)

            if problems:
                rejected_rows.append({
                    "source_file": row.get("source_file", file_path.name),
                    "row": row,
                    "errors": problems,
                })
            else:
                valid_rows.append(cleaned_row(row))

  
    total_rows = len(valid_rows) + len(rejected_rows)

    summary = build_summary(
        total_rows,
        valid_rows,
        rejected_rows,
    )

    print("\n" + "=" * 40)
    print("PROCESSING SUMMARY")
    print("=" * 40)
    print(f"Total rows read: {summary['total_rows']}")
    print(f"Valid transactions: {summary['valid_transactions']}")
    print(f"Rejected transactions: {summary['rejected_transactions']}")

    print("\nRejection reason:")
    for reason, count in summary["rejection_reason"].items():
        print(f"- {reason}: {count}")

    output_folder = Path("output")
    write_csv(
        output_folder / "Cleaned_transactions.csv",
        valid_rows,
    )
    
    rejected_ouput = prepare_rejected_rows(rejected_rows)
    write_csv(
        output_folder / "rejected_transactions.csv",
        rejected_ouput,
    )
