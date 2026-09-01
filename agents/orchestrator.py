from typing import Any
from agents.scout_agent import ScoutAgent
from agents.reconciliation_agent import ReconciliationAgent
from agents.anomaly_agent import AnomalyAgent
from agents.resolution_agent import ResolutionAgent
from agents.compliance_agent import ComplianceAgent
from agents.audit_logger import AuditLogger


class MultiAgentOrchestrator:
    """
        Orchestrates the multi-agent financial reconciliation process.
        Coordinates the Scout, Anomaly Detection, Compliance, and Reconciliation agents.
        Maintains an audit trail of all decisions and actions taken by each agent.
    """

    def __init__(self, audit_log_path: str = "logs/audit_trail.json", llm_model: str = "qwen2.5:7b-instruct"):
        self.scout = ScoutAgent()
        self.reconciler = ReconciliationAgent()
        self.anomaly_detector = AnomalyAgent()
        self.resolution_agent = ResolutionAgent()
        self.compliance_agent = ComplianceAgent()
        self.audit_logger = AuditLogger(output_file=audit_log_path)

        self.resolution_agent.MODEL = llm_model

    def process_case(self, case_id : str, document_objects : list[Any]) -> dict[str, Any]:

        """
             Processes a single benchmark case 
             through the multi-agent reconciliation pipeline.
             
        """

        # Step 1: Scout Agent - Extracts and summarizes transaction data from documents

        evidence = self.scout.process(document_objects)

        tx_id = evidence[0]["transaction_id"] if evidence else case_id

        # Step 2 Reconciliation Agent - Match & Discrepance Detection

        recon_results = self.reconciler.process(evidence)
        recon_result = recon_results[0] if recon_results else {"status" : 
                                                               "UNKNOWN", "documents": []}

        recon_status = recon_result.get("status", "UNKNOWN")

        # Branching : clean Case (Match)
        if recon_status == "MATCH":
            self.audit_logger.log_entry(
                case_id=case_id,
                transaction_id=tx_id,
                step_name="RECONCILIATION",
                agent_name = "ReconciliationAgent",
                decision = "MATCH",
                reason= "All documents match perfectly",
                confidence=1.0,
                final_action="AUTO_RECONCILE"
            )
            return {
                "case_id" : case_id,
                "transaction_id" : tx_id,
                "status" : "MATCH",
                "final_action": "AUTO_RECONCILE",
                "is_clean": True,
                "anomaly": None,
                "proposal": None,
                "compliance": None
            }

        # Step 3: Anomaly Agent - Classification & Explanation
        anomalies = self.anomaly_detector.process(recon_results)

        anomaly = anomalies[0] if anomalies else{
            "transaction_id" : tx_id,
            "anomaly_type": recon_status,
            "severity": "MEDIUM",
            "explanation": recon_result.get("reason", "Anomaly detected")
        }

        self.audit_logger.log_entry(
            case_id=case_id,
            transaction_id=tx_id,
            step_name="ANOMALY_DETECTION",
            agent_name = "AnomalyAgent",
            decision = anomaly["anomaly_type"],
            reason= anomaly["explanation"],
            confidence=1.0
        )

        # Step  4 : Resolution Agent - LLM proposed action

        proposal = self.resolution_agent.resolve(
            transaction_id=tx_id,
            financial_documents={"evidence": evidence},
            reconciliation_results= recon_result,
            anomaly_results=anomaly
        )


        self.audit_logger.log_entry(
            case_id=case_id,
            transaction_id=tx_id,
            step_name="RESOLUTIO_PROPOSAL",
            agent_name="ResolutionAgent (LLM)",
            decision = proposal.action,
            reason=proposal.reason,
            confidence=proposal.confidence
        )

        # Step 5 : Compliance Agent - Deterministic Rule & Guardrail Validation

        verdict = self.compliance_agent.validate(proposal,
                                                 anomaly_result=anomaly)

        self.audit_logger.log_entry(
            case_id=case_id,
            transaction_id=tx_id,
            step_name="COMPLIANCE_VERDICT",
            agent_name="ComplianceAgent",
            decision = verdict.approved_action,
            reason=verdict.override_reason or "Proposal passed compliance rules.",

            confidence=verdict.confidence,
            final_action=verdict.approved_action
        )

        return {
            "case_id" : case_id,
            "transaction_id" : tx_id,
            "status" : recon_status,
            "final_action" : verdict.approved_action,
            "is_clean": False,
            "anomaly": anomaly,
            "proposal": proposal.model_dump(),
            "compliance" : verdict.model_dump()
        }



    def save_audit_logs(self):
        self.audit_logger.save()

        