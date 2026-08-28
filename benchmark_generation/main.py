from datetime import date

from syndata_generation.models import Transaction

from benchmark_generation.benchmark_generator import(
    generate_benchmark_dataset
)

transactions = [
    Transaction(
        transaction_id = "TXN001",
        customer_id = "CUST001",
        account_type = "Savings",
        total_balance = 50000,
        transaction_amount=5000,
        investment_amount=10000,
        investment_type="Mutual Fund",
        transaction_date=date(2026,8,28)
    )

    Transaction(
        transaction_id = "TXN002",
        customer_id = "CUST002",
        account_type = "Current",
        total_balance = 75000,
        transaction_amount=10000,
        investment_amount=20000,
        investment_type="Stock",
        transaction_date=date(2026,8,27)
    )

    Transaction(
        transaction_id = "TXN003",
        customer_id = "CUST003",
        account_type = "Savings",
        total_balance = 30000,
        transaction_amount=2500,
        investment_amount=5000,
        investment_type="Bond",
        transaction_date=date(2026,8,26)
    )  
]


fault_types = [
    "clean",
    "amount_mismatch",
    "date_mismatch",
    "duplicate_document",
    "missing_document",
    "wrong_customer",
    "broken_reference"
]

benchmark_cases, ground_truth_labels = (
    generate_benchmark_dataset(
        transactions,
        fault_types
    )
)


print("\nBENCHMARK CASES\n")

for case in benchmark_cases:

    print(case["case_id"])

    print(case["documents"])

    print("-" * 50)


print("\nGROUND TRUTH\n")

for label in ground_truth_labels:
    print(label)