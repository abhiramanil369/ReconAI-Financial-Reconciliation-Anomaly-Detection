from models import(
    Transaction,
    Invoice,
    Payment,
    BankTransaction
)

def generate_invoice(transaction: Transaction) -> Invoice:
    """
    Generate an invoice from a transaction 
    """

    return Invoice(
        invoice_id = f"INV-{transaction.transaction_id}",
        transaction_id = transaction.transaction_id,
        customer_id = transaction.customer_id,
        amount = transaction.transaction_amount,
        invoice_date = transaction.transaction_date
    )


def generate_payment(
    transaction: Transaction,
    invoice: Invoice        
) -> Payment:
    """
        Generate an invoice from a transaction
    """

    return Payment(
        payment_id = f"PAY-{transaction.transaction_id}",
        invoice_id = invoice.invoice_id,
        transaction_id = transaction.transaction_id,
        customer_id = transaction.customer_id,
        amount = transaction.transaction_amount,
        payment_date = transaction.transaction_date
    )


def generate_bank_transaction(
        transaction: Transaction
) ->  BankTransaction:
    """
        Generate a bank transaction from the original transaction.
    """

    return BankTransaction(
        bank_transaction_id = f"BANK-{transaction.transaction_id}",
        transaction_id = transaction.transaction_id,
        customer_id = transaction.customer_id,
        amount = transaction.transaction_amount,
        transaction_date = transaction.transaction_date
    )