from typing import Any, Union


from syndata_generation.models import(
    Transaction,
    Invoice,
    Payment,
    BankTransaction
)

FinancialDocument = Union[
    Transaction,
    Invoice,
    Payment,
    BankTransaction
]

class ScoutAgent:
    """
        Scout Agent

        Responsible for:
        - Reading financial documents
        - Identifying documents types
        - Validating supposrted schemas
        - Normalizing documents into a common evidence format
    """


    def identify_document_type(
            self,
            document: FinancialDocument
    ) -> str:
        """
        Identify the type of financila document
        """

        if isinstance(document, Transaction):
            return "TRANSACTION"
        
        if isinstance(document, Transaction):
            return "INVOICE"

        if isinstance(document, Transaction):
            return "PAYMENT"

        if isinstance(document, Transaction):
            return "BANK_TRANSACTION"


        raise ValueError(
            f"Unsupported document type : {type(document)}"
        )

    def normalize_document(
            self,
            document: FinancialDocument
    ) -> dict[str, Any]:

        """
            Convert different financial document schemas
            into one standard evidence format.
        """

        document_type = self.identify_document_type(document)

        evidence = {
            "document_type" : document_type,
            "document_id" : None,
            "transaction_id" : None,
            "customer_id" : None,
            "amount" : None,
            "date" : None,
            "reference_id" : None,
        }

        if isinstance(document, Transaction):
            evidence["document_id"] = document.transaction_id
            evidence["transaction_id"] = document.transaction_id
            evidence["customer_id"] = document.customer_id
            evidence["amount"] = document.transaction_amount
            evidence["date"] = document.transaction_date

        elif isinstance(document, Invoice):
            evidence["document_id"] = document.invoice_id
            evidence["transaction_id"] = document.transaction_id
            evidence["customer_id"] = document.customer_id
            evidence["amount"] = document.transaction_amount
            evidence["date"] = document.invoice_date   


        elif isinstance(document, Payment):
            evidence["document_id"] = document.payment_id
            evidence["transaction_id"] = document.transaction_id
            evidence["customer_id"] = document.customer_id
            evidence["amount"] = document.transaction_amount
            evidence["date"] = document.payment_date    

            evidence["reference_id"] = document.invoice_id

        elif isinstance(document, BankTransaction):
            evidence["document_id"] = document.bank_transaction_id
            evidence["transaction_id"] = document.transaction_id
            evidence["customer_id"] = document.customer_id
            evidence["amount"] = document.transaction_amount
            evidence["date"] = document.transaction_date 

        return evidence

    def process(
            self, documents: list[FinancialDocument]
    ) -> list[dict[str, Any]]:

        """
            Process a collection of financial documents

            Returns a standardized evidence list
        """

        standardized_evidence = []

        for document in documents:
            evidence = self.normalize_document(document)

            standardized_evidence.append(
                evidence
            )

        return standardized_evidence
