from typing import Any

class AnomalyAgent:
    """
        AnomalyAgent

        Responsibile for:
        - Detect reconciliation failures
        - Classifying exception types
        - Identifying affected documents
        - Assigning severity
        - Producing anomaly explanation
    """

    SEVERITY_MAPPING = {
        "MISSING_DOCUMENT" : "HIGH",
        "AMOUNT_MISMATCH" : "HIGH",
        "DATE_MISMATCH" : "MEDIUM",
        "CUSTOMER_MISMATCH" : "CRITICAL"
    }

    def is_anomaly(
        self,
        reconciliation_result: dict[str, Any]
    ) -> bool:
        """
            Check whether a reconciliation result
            represents an anomaly
        """

        return reconciliation_result["status"] != "MATCH"


    def get_severity(
            self,
            status: str
    ) -> str:

        """
            Assign severity based on anomaly type
        """

        return self.SEVERITY_MAPPING.get(
            status,
            "LOW"
        )

    def identify_affected_documents(
            self, 
            reconciliation_result: dict[str, Any]
    ) -> list[str]:
        """
            Identify documents involved in the anomaly
        """

        documents = reconciliation_result["documents"]

        affected_documents = []

        for document in documents:

            affected_documents.append(
                document["document_id"]
            )

        return affected_documents


    def create_explanation(
            self,
            reconciliation_result : dict[str, Any]
    )-> str:
        """
            Create a human-readable explanation
            for the anomaly
        """

        status = reconciliation_result["status"]

        if status == "MISSING_DOCUMENT":

            missing_documents = (
                reconciliation_result["missing_documents"]
            )

            return (
                f"Required documents(s) missing:"
                f"{','.join(missing_documents)}"
            )

        if status == "AMOUNT_MISMATCH":


            return (
                "Amounts differ between related"
                "financial documents."
            )

        if status == "DATE_MISMATCH":


            return (
                "Dates differ between related"
                "financial documents."
            )

        if status == "CUSTOMER_MISMATCH":


            return (
                "Customer IDs differ between related"
                "financial documents."
            )


        return "Unknown reconciliation anomaly."


    def analyze_result(
            self, 
            reconciliation_result: dict[str, Any]
    ) -> dict[str, Any] | None:
        """
            Analyze one reconciliation result.

            Returns None when the transaction matches.
        """

        if not self.is_anomaly(
            reconciliation_result
        ):
            return None

        status = reconciliation_result["status"]

        anomaly = {
            "transaction_id" :(
                reconciliation_result["transaction_id"]
            ),
            "anomaly_type" : status,
            "severity" : self.get_severity(status),
            "affected_documents" : (
                self.identify_affected_documents(
                    reconciliation_result
                )
            ),
            "explanation" : self.create_explanation(
                reconciliation_result
            )
        }

        return anomaly

    def process(
            self, 
            reconciliation_results: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        """
            Process reconciliation results and
            return detected anomalies.
        """

        anomalies = []

        for result in reconciliation_results:

            anomaly = self.analyze_result(result)

            if anomaly is not None:

                anomalies.append(anomaly)


        return anomalies

    
