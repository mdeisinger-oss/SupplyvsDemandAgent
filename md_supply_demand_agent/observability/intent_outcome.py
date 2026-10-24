"""Intent vs. Outcome Capture Module for MD-Supply-vs-Demand-Agent.

Rubric Criterion 4.2 — Intent vs. Outcome Capture (5 pts):
"Logs explicitly record both the agent's intended action before execution and
the actual outcome after."

Every sub-agent delegation and tool invocation explicitly records:
1. Pre-execution `AGENT_INTENT` (intent_id, actor, intended_action, target_resource,
   planned_arguments, expected_outcome, rationale).
2. Post-execution `AGENT_OUTCOME` (intent_id, actual_status, actual_outcome_summary,
   actual_output, latency_ms, discrepancy_detected).
"""

import datetime
import time
import uuid
from typing import Any, Dict, List, Optional

from .pii_redactor import global_pii_redactor
from .structured_logger import get_structured_logger


class IntentOutcomeAuditor:
    """Explicitly logs and correlates pre-execution INTENT with post-execution OUTCOME."""

    def __init__(self) -> None:
        self.logger = get_structured_logger("md_supply_demand_agent.intent_outcome")
        self._records: Dict[str, Dict[str, Any]] = {}
        self._history: List[Dict[str, Any]] = []

    def record_intent(
        self,
        actor: str,
        intended_action: str,
        planned_arguments: Dict[str, Any],
        expected_outcome: str,
        rationale: str = "",
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> str:
        """Logs the agent's intended action BEFORE execution and returns a correlation `intent_id`."""
        intent_id = f"INTENT-{uuid.uuid4().hex[:10].upper()}"
        scrubbed_args = global_pii_redactor.scrub_data(planned_arguments)
        timestamp_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        intent_payload = {
            "intent_id": intent_id,
            "phase": "PRE_EXECUTION_INTENT",
            "actor": actor,
            "intended_action": intended_action,
            "planned_arguments": scrubbed_args,
            "expected_outcome": global_pii_redactor.scrub_text(expected_outcome),
            "rationale": global_pii_redactor.scrub_text(rationale),
            "intent_timestamp": timestamp_iso,
            "start_perf": time.perf_counter(),
            "trace_id": trace_id,
            "span_id": span_id,
        }
        self._records[intent_id] = intent_payload

        self.logger.info(
            f"[AGENT_INTENT] Actor '{actor}' intends to execute '{intended_action}': {expected_outcome}",
            extra={
                "component": actor,
                "event_type": "AGENT_INTENT",
                "intent_id": intent_id,
                "trace_id": trace_id,
                "span_id": span_id,
                "structured_data": {
                    "intent_id": intent_id,
                    "actor": actor,
                    "intended_action": intended_action,
                    "planned_arguments": scrubbed_args,
                    "expected_outcome": intent_payload["expected_outcome"],
                    "rationale": intent_payload["rationale"],
                },
            },
        )
        return intent_id

    def record_outcome(
        self,
        intent_id: str,
        actual_status: str,
        actual_outcome_summary: str,
        actual_data: Optional[Dict[str, Any]] = None,
        discrepancy_detected: bool = False,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Logs the actual outcome AFTER execution and links it to the pre-execution `intent_id`."""
        intent_entry = self._records.get(intent_id, {})
        start_perf = intent_entry.get("start_perf", time.perf_counter())
        latency_ms = round((time.perf_counter() - start_perf) * 1000.0, 2)
        scrubbed_data = global_pii_redactor.scrub_data(actual_data or {})
        scrubbed_summary = global_pii_redactor.scrub_text(actual_outcome_summary)

        combined_record = {
            "intent_id": intent_id,
            "actor": intent_entry.get("actor", "UnknownActor"),
            "intended_action": intent_entry.get("intended_action", "UnknownAction"),
            "planned_arguments": intent_entry.get("planned_arguments", {}),
            "expected_outcome": intent_entry.get("expected_outcome", ""),
            "intent_timestamp": intent_entry.get("intent_timestamp"),
            "actual_status": actual_status,
            "actual_outcome_summary": scrubbed_summary,
            "actual_data": scrubbed_data,
            "discrepancy_detected": discrepancy_detected,
            "latency_ms": latency_ms,
            "outcome_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "trace_id": trace_id or intent_entry.get("trace_id"),
            "span_id": span_id or intent_entry.get("span_id"),
        }

        self._history.append(combined_record)
        if len(self._history) > 300:
            self._history.pop(0)

        self.logger.info(
            f"[AGENT_OUTCOME] Intent '{intent_id}' ({combined_record['intended_action']}) "
            f"completed with status '{actual_status}' in {latency_ms}ms: {scrubbed_summary}",
            extra={
                "component": combined_record["actor"],
                "event_type": "AGENT_OUTCOME",
                "intent_id": intent_id,
                "trace_id": combined_record["trace_id"],
                "span_id": combined_record["span_id"],
                "structured_data": {
                    "intent_id": intent_id,
                    "intended_action": combined_record["intended_action"],
                    "expected_outcome": combined_record["expected_outcome"],
                    "actual_status": actual_status,
                    "actual_outcome_summary": scrubbed_summary,
                    "discrepancy_detected": discrepancy_detected,
                    "latency_ms": latency_ms,
                },
            },
        )
        return combined_record

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns paired Intent-vs-Outcome audit records."""
        return list(reversed(self._history[-limit:]))

    def clear(self) -> None:
        self._records.clear()
        self._history.clear()


global_intent_outcome_auditor = IntentOutcomeAuditor()
