from datetime import date

from agents.scout_agent import ScoutAgent
from agents.reconciliation_agent import ReconciliationAgent

from syndata_generation.models import Transaction

from syndata_generation.generators import(
    generate_bank_transaction,
    generate_payment,
    generate_invoice
)

def test_reconciliation_agent_match():

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

    reconciliation_agent = ReconciliationAgent()

    results = reconciliation_agent.process(
        evidence
    )

    assert len(results) == 1

    assert results[0]["transaction_id"] == "TXN-001"

    assert results[0]["status"] == "MATCH"
    