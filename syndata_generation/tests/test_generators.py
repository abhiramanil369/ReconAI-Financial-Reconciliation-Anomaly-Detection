import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from datetime import date

from models import Transaction

from generators import (
    generate_invoice,
    generate_payment,
    generate_bank_transaction
)

from validator import validate_document


def create_sample_transaction():

    return Transaction(
        transaction_id="TXN001",
        customer_id="C102",
        account_type="Savings",
        total_balance=50000,
        transaction_amount=10000,
        investment_amount=5000,
        investment_type="Mutual Fund",
        transaction_date=date(2026, 8, 25)
    )


def test_invoice_generation():

    transaction = create_sample_transaction()

    invoice = generate_invoice(transaction)

    assert invoice.invoice_id == "INV-TXN001"
    assert invoice.transaction_id == "TXN001"
    assert invoice.customer_id == "C102"
    assert invoice.amount == 10000


def test_payment_generation():

    transaction = create_sample_transaction()

    invoice = generate_invoice(transaction)

    payment = generate_payment(
        transaction,
        invoice
    )

    assert payment.payment_id == "PAY-TXN001"
    assert payment.invoice_id == "INV-TXN001"
    assert payment.transaction_id == "TXN001"
    assert payment.customer_id == "C102"
    assert payment.amount == 10000


def test_bank_transaction_generation():

    transaction = create_sample_transaction()

    bank = generate_bank_transaction(transaction)

    assert bank.bank_transaction_id == "BANK-TXN001"
    assert bank.transaction_id == "TXN001"
    assert bank.customer_id == "C102"
    assert bank.amount == 10000


def test_document_validation():

    transaction = create_sample_transaction()

    invoice = generate_invoice(transaction)

    payment = generate_payment(
        transaction,
        invoice
    )

    bank = generate_bank_transaction(
        transaction
    )

    result = validate_document(
        invoice,
        payment,
        bank
    )

    assert result is True