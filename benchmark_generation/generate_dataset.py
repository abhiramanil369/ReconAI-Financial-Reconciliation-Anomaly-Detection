import sys
from pathlib import Path

# Automatically locate the project root directory (one level up from benchmark_generation)
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
from datetime import datetime
import pandas as pd

from syndata_generation.models import Transaction
from benchmark_generation.benchmark_generator import generate_benchmark_dataset

# 1. Load ground truth transactions from CSV using absolute Path

csv_path = ROOT_DIR / "syndata_generation" / "data" / "transaction_data.csv"

if not csv_path.exists():
    csv_path = ROOT_DIR / "sample_dataset" / "transaction_data.csv"


df = pd.read_csv(csv_path)


transactions = []

for _, row in df.iterrows():

    # Parse transaction date

    raw_date = row["Transaction_Date"]
    tx_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if isinstance(raw_date, str) else raw_date

    transactions.append(
        Transaction(
            transaction_id=str(row["Transaction_ID"]),
            customer_id=str(row["Customer_ID"]),
            account_type=row["Account_Type"],
            total_balance=float(row["Total_Balance"]),
            transaction_amount=float(row["Transaction_Amount"]),
            investment_amount=float(row["Investment_Amount"]),
            investment_type=row["Investment_Type"],
            transaction_date=tx_date
        )
    )


# 2. Define fault types to cycle through

fault_types = [
    "clean",
    "amount_mismatch",
    "date_mismatch",
    "duplicate_document",
    "missing_document",
    "wrong_customer",
    "broken_reference"
]

# 3. Generate benchmark cases & ground truth labels

print(f"Generating benchmark cases for {len(transactions)} transactions...")
benchmark_cases, ground_truth_labels = generate_benchmark_dataset(
    transactions,
    fault_types
)


# 4. Serialize Pydantic models to JSON-friendly dictionaries

serialized_cases = []
for case in benchmark_cases:
    serialized_docs = {}
    for doc_name, doc_obj in case["documents"].items():
        if doc_obj is None:
            serialized_docs[doc_name] = None
        elif hasattr(doc_obj, "model_dump"):
            serialized_docs[doc_name] = doc_obj.model_dump(mode="json")
        else:
            serialized_docs[doc_name] = doc_obj

    serialized_cases.append({
        "case_id": case["case_id"],
        "documents": serialized_docs
    })


# 5. Save output files

output_dir = Path(__file__).resolve().parent
cases_file = output_dir / "benchmark_cases.json"
labels_file = output_dir / "ground_truth_labels.json"

with open(cases_file, "w") as f:
    json.dump(serialized_cases, f, indent=4)

with open(labels_file, "w") as f:
    json.dump(ground_truth_labels, f, indent=4)


print("Done!")

print(f"Saved {len(serialized_cases)} benchmark cases to benchmark_cases.json")

print(f"Saved {len(ground_truth_labels)} ground truth labels to ground_truth_labels.json")
