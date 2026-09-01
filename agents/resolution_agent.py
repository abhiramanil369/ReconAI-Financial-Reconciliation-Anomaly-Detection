import json
from typing import Any, Literal
import ollama
from pydantic import BaseModel, Field, model_validator


class JournalEntry(BaseModel):
    """
    Represents a single docuble-entry accounting journal entry.
    """

    account : str
    debit : float = Field(default=0.0, ge=0.0)
    credit : float = Field(default=0.0, ge=0.0)


class Resolution(BaseModel):
    """
    Structure resolution proposed by the LLM
    
    """

    transaction_id : str
    action : Literal[
        "AUTO_RECONCILE",
        "WAIT_FOR_SETTLEMENT",
        "REQUEST_MISSING_DOCUMENT",
        "CREATE_JOURNAL_ENTRY",
        "ESCALATE"
    ]

    reason : str = Field(min_length=1, description="Reason for the proposed action")

    confidence : float = Field(ge=0.0, le=1.0, description="Confidence score of the proposed action")

    journal_entries : list[JournalEntry] | None = None

    @model_validator(mode="after")
    def valdate_journal_entries(self):
        """
            Pydantic validator checking double-entry bookkeeping balance.
        """

        if self.action == "CREATE_JOURNAL_ENTRY":
            if not self.journal_entries:
                raise ValueError("Journal entries must be provided for CREATE_JOURNAL_ENTRY action")

            total_debit = sum(round(e.debit, 2) for e in self.journal_entries)
            total_credit = sum(round(e.credit, 2) for e in self.journal_entries)

            if round(total_debit, 2) != round(total_credit, 2):
                raise ValueError(f"Journal entries are not balanced: total debit {total_debit} != total credit {total_credit}")

        return self


class ResolutionAgent:
    """
    Resolution Agent
    
    Uses Qwen2.5: 7B-Instruct through Ollama to propose a grounded financial resolution based on the provided evidence documents.
    """

    MODEL = "qwen-2.5-7b-instruct"

    def resolve(
            self, 
            transaction_id : str,
            financial_documents : dict[str, Any],
            reconciliation_results: dict[str, Any],
            anomaly_results : dict[str, Any]
    ) -> Resolution:

        system_prompt = """ You are a senior AI Finanace Controller specializing 

        in multi-source financial reconciliation, exception resolution, and
        doublt-entry bookkeeping.

        YOUR MISSION:
        Analyze financial reconciliation anomalies and propose ONE
        safe resolution action.

        AVAILABLE RESOLUTION ACTIONS:

        1. AUTO_RECONCILE : Use ONLY when available evidence supports complete reconciliation.

        2. WAIT_FOR_SETTLEMET : Use when payment exists but bank settlement evidence is pending (date difference within acceptable clearing window).

        3. REQUEST_MISSING_DOCUMENT : Use when a required financial document (Invoice, Payment, Bank Transaction) is missing.

        4. CREATE_JOURNAL_ENTRY : Use when an accounting adjustment is required (e.g. fee difference, small amount discrepancy).

        5. ESCALATE : Use when the anomaly is complex, ambiguous, or requires human intervention.(e.g. multiple conflicting documents, large amount discrepancy, or regulatory compliance issue).


        ALLOWED CHART OF ACCOUNTS FOR JOURNAL ENTRIES:
        - 1010 Cash
        - 1200 Accounts Receivable
        - 2010 Accounts Payable
        - 5010 Bank Fees & Service Charges
        - 5090 Reconciliation Discrepancies
        - 4000 Revenue

        RULES:
        - Never invent financial documents, transaction amounts, dates or customer IDs.
        - For CREATE_JOURNAL_ENTRY, ensure total debit equals total credit (double-entry bookkeeping).
        - If confidence < 0.75 or evidence is contradictory, choose ESCALATE.

"""

        user_prompt = """
        TRANSACTION ID: {transaction_id}
        
        FINANCIAL EVIDENCE: {json.dumps(financial_evidence, indent= 2, default = str)}

        RECONCILIATION RESULTS: {json.dumps(reconciliation_results, indent= 2, default = str)}

        ANOMALY RESULTS: {json.dumps(anomaly_results, indent= 2, default = str)}

"""

        try:
            response = ollama.chat(
                model = self.MODEL,
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                format = Resolution.model_json_schema(),
                options= {"temperature": 0.0}
            )

            return Resolution.model_validate_json(response.message.content)
        except Exception as e:
            # Safe Fallback to ESCALATE in case of any issues with the LLM response
            return Resolution(
                transaction_id=transaction_id,
                action="ESCALATE",
                reason=f"LLM Resolution Fallback triggered due to error: {str(e)}",
                confidence=0.0,
                journal_entries=None
            )