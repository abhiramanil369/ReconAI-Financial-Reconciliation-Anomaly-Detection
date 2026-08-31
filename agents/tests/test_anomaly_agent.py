from agents.anomaly_agent import AnomalyAgent

def test_amount_mismatch_anomaly():

    reconciliation_results = [
        {
            "transaction_id" : "TXN-001",
            "status" : "AMOUNT_MISMATCH",
            "reason": "Amounts do no match",
            "missing_documents" : [],
            "documents" : [
                {
                    "document_id" : "TXN-001",
                    "document_type" : "TRANSACTION",
                    "amount" : 10000
                },
                {
                    "document_id" : "INV-TXN-001",
                    "document_type" : "INVOICE",
                    "amount" : 10000 
                },
                {
                    "document_id" : "PAY-TXN-001",
                    "document_type" : "PAYMENT",
                    "amount" : 9500 
                },
                {
                    "document_id" : "BANK-TXN-001",
                    "document_type" : "BANK_TRANSACTION",
                    "amount" : 10000  
                }
            ]
        }
    ]

    anomaly_agent = AnomalyAgent()

    anomalies = anomaly_agent.process(
        reconciliation_results
    )

    assert len(anomalies) == 1

    assert anomalies[0]["transaction_id"] == "TXN-001"

    assert anomalies[0]["anomaly_type"] == "AMOUNT_MISMATCH"

    assert anomalies[0]["severity"] == "HIGH"

    assert "PAY-TXN-001" in (
        anomalies[0]["affected_documents"]
    )

    