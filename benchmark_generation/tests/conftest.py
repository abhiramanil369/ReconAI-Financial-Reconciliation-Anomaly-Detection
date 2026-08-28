import pytest
from datetime import date

from syndata_generation.models import Transaction

from benchmark_generation.benchmark_generator import create_clean_case

@pytest.fixture
def sample_transaction():
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


@pytest.fixture
def clean_documents(sample_transaction):

    return create_clean_case(
        sample_transaction
    )
