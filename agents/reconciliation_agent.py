from typing import Any

class ReconciliationAgent:
    """
        Reconciliation Agent

        Responsible for :
        - Group related documents
        - Matching documents using transaction_id
        - Comparing amounts
        - Comparing dates
        - Comparing customer IDs
        - Producing reconciliation results
    """

    REQUIRED_DOCUMENT_TYPES =  {
        "TRANSACTION",
        "INVOICE",
        "PAYMENT",
        "BANK_TRANSACTION"
    }

    def group_by_transaction(
            self,
            evidence : list[dict[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """
            Group standardized documents by transaction_id.
        """

        grouped_documents = {}

        for document in evidence:

            transaction_id = document["transaction_id"]

            if transaction_id not in grouped_documents:
                grouped_documents["transaction_id"] = []

            grouped_documents["transaction_id"].append(
                document
            )

        return grouped_documents

    def check_required_documents(
            self, documents : list[dict[str, Any]]
    ) -> list[str]:

        present_document_types = {
            document["document_type"]
            for document in documents
        }

        missing_documents = {
            self.REQUIRED_DOCUMENT_types
            - present_document_types
        }

        return list(missing_documents)

    def compare_amounts(
            self, 
            documents: list[dict[str, Any]]
    ) -> bool:
        """
            Check whether all documents amounts match
        """

        amounts = {
            document["amount"]
            for document in documents
        }

        return len(amounts) == 1


    def compare_dates(
            self,
            documents : list[dict[str, Any]]
    ) -> bool:
        """
            Check whether all document dates match
        """

        dates = {
            document["dates"]
            for document in documents
        }

        return len(dates) == 1

    def compare_customers(
            self,
            documents : list[dict[str, Any]]
    ) -> bool:
        """
            Check whether all customer IDs match
        """

        customer_ids = {
            document["customer_id"]
            for document in documents
        }

        return len(customer_ids) == 1

    
    def reconcile_transaction(
            self,
            transaction_id : str,
            documents : list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
            Reconcile all documents belonging
            to one transaction.
        """

        missing_documents = self.check_required_documents(
            documents
        )

        if missing_documents:

            return {
                "transaction_id" : transaction_id,
                "status": "MISSING_DOCUMENT",
                "reason": "Required document is missing",
                "missing_documents" : missing_documents,
                "documents" : documents
            }

        if not self.compare_amounts(documents):

            return {
                "transaction_id" : transaction_id,
                "status": "AMOUNT_MISMATCH",
                "reason": "Amounts do not match",
                "missing_documents" : [],
                "documents" : documents
            }

        if not self.compare_dates(documents):

            return {
                "transaction_id" : transaction_id,
                "status": "DATE_MISMATCH",
                "reason": "Dates do not match",
                "missing_documents" : [],
                "documents" : documents
            }

        if not self.compare_customers(documents):

            return {
                "transaction_id" : transaction_id,
                "status": "CUSTOMER_MISMATCH",
                "reason": "Customer IDs do not match",
                "missing_documents" : [],
                "documents" : documents
            }

        return {
            "transaction_id" : transaction_id,
            "status": "MATCH",
            "reason": "All related documents match",
            "missing_documents" : [],
            "documents" : documents
        }

    def process(
            self,
            evidence: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        """
            Process standardized evidence and
            reconcile every transaction.
        """

        grouped_documents = self.group_by_transaction(
            evidence
        )

        reconciliaton_results = []

        for transaction_id, documents in grouped_documents.item():

            result = self.reconcile_transaction(
                transaction_id,
                documents
            )

            reconciliaton_results.append(result)


        return reconciliaton_results
