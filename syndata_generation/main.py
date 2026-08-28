import json

import pandas as pd

from models import Transaction

from generators import (
    generate_bank_transaction,
    generate_invoice,
    generate_payment
)

from validator import validate_document


def main():

    # Ground Truth Transaction dataset

    df = pd.read_csv("data/transaction_data.csv")

    invoices = []
    payments = []
    bank_transactions = []


    # Process every transaction

    for _, row in df.iterrows():

        transaction = Transaction(
            transaction_id = str(row["Transaction_ID"]),
            customer_id = str(row["Customer_ID"]),
            account_type = row["Account_Type"],
            total_balance = row["Total_Balance"],
            transaction_amount = row["Transaction_Amount"],
            investment_amount = row["Investment_Amount"],
            investment_type = row["Investment_Type"],
            transaction_date = row["Transaction_Date"]
        )

        # Generate documents

        invoice = generate_invoice(transaction)

        payment = generate_payment(transaction, invoice)

        bank_transaction = generate_bank_transaction(transaction)


        # Validate generated documents

        validate_document(
            invoice,
            payment,
            bank_transaction
        )


        # Serialize Pydantic models

        invoices.append(
            invoice.model_dump(mode = "json")
        )

        payments.append(
            payment.model_dump(mode = "json")
        )

        bank_transactions.append(
            bank_transaction.model_dump(mode = "json")
        )

    # Save generated documents

    with open("data/invoices.json", "w") as file:
        json.dump(
            invoices,
            file,
            indent =4
        )

    with open("data/payments.json", "w") as file:
        json.dump(
            payments,
            file,
            indent =4
        )

    with open("data/bank_transactions.json", "w") as file:
        json.dump(
            bank_transactions,
            file,
            indent =4
        )



    print("\n-----------Document generation completed-----------")

    print(f"Transaction processed : {len(df)}")
    print(f"Invoices generated : {len(invoices)}")
    print(f"Payments generated : {len(payments)}")


    print(
        f"Bank transactions generated: "
        f"{len(bank_transactions)}"
    )

if __name__ == "__main__":
    main()
