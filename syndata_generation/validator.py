from models import(
    Invoice,
    Payment,
    BankTransaction
)

def validate_document(
    invoice : Invoice,
    payment : Payment,
    bank_transaction : BankTransaction
) -> bool:

    # Payment must reference the correct invoice
    assert payment.invoice_id == invoice.invoice_id,(
        "Payment references the wrong invoice"
    )

    # Transaction IDs must match

    assert payment.transaction_id == invoice.transaction_id,(
        "Payment references the wrong invoice"
    )

    assert bank_transaction.transaction_id == invoice.transaction_id,(
        "Payment transaction ID does not match invoice"
    )

    # Customer IDs must match
    assert payment.customer_id == invoice.customer_id, (
        "Payment customer ID does not match invoice"
    )

    assert bank_transaction.customer_id == invoice.customer_id, (
            "Bank transaction customer ID does not match invoice"
    )

    # Amounts must match
    assert payment.amount == invoice.amount,(
        "Payment amount does not match invoice"
    )

    assert bank_transaction.amount == invoice.amount,(
        "Bank transaction amount does not match invoice"
    )


    return True