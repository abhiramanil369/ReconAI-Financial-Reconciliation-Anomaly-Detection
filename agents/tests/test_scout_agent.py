from datetime import date

from agents.scout_agent import ScoutAgent

from syndata_generation.models import(
    Transaction
)

from syndata_generation.generators import(
    generate_invoice,
    generate_bank_transaction,
    generate_payment
)

def test_scout_agent():

    transaction = Transaction(
        transaction_id = "TXN-001",
        customer_id = "C102",
        account_type = "Savings",
        total_balance = 50000,
        transaction_amount=10000,
        investment_amount=20000,
        investment_type="Mutual Fund",
        transaction_date=date(2026,8,30)
    )

    invoice = generate_invoice(transaction)

    payment = generate_payment(transaction, invoice)

    bank_transaction = generate_bank_transaction(transaction)

    documents = [
        transaction,
        invoice,
        payment,
        bank_transaction
    ]

    scout = ScoutAgent()

    evidence = scout.process(
        documents
    )

    assert len(evidence) == 4

    assert evidence[0]["document_type"] == (
        "TRANSACTION"
    )

    assert evidence[1]["document_type"] == (
        "INVOICE"
    )

    assert evidence[2]["document_type"] == (
        "PAYMENT"
    )

    assert evidence[3]["document_type"] == (
        "BANK_TRANSACTION"
    )

    assert evidence[2]["reference_id"] == (
        invoice.invoice_id
    )

    assert evidence[0]["amount"] == 10000

