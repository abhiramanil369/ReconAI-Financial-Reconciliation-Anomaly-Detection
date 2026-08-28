from datetime import date

from pydantic import BaseModel, field_validator

class Transaction(BaseModel):
    transaction_id : str
    customer_id : str
    account_type : str
    total_balance : float
    transaction_amount : float
    investment_amount : float
    investment_type : str
    transaction_date : date


    @field_validator('transaction_amount')
    @classmethod
    def validate_transaction_amount(cls, value):
        if value <= 0:
            raise ValueError('Transaction amount must be positive')

        return value


class Invoice(BaseModel):
    invoice_id : str
    transaction_id : str
    customer_id : str
    amount: float
    invoice_date : date

class Payment(BaseModel):
    payment_id : str
    invoice_id : str
    transaction_id : str
    customer_id : str
    amount : float
    payment_date: date

class BankTransaction(BaseModel):
    bank_transaction_id: str
    transaction_id : str
    customer_id : str
    amount: float
    transaction_date: date
