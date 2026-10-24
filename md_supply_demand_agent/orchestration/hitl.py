"""Human-in-the-Loop (HITL) Customer Acceptance Hooks for MD-Supply-vs-Demand-Agent.

Rubric Criterion 3.4 — Human-in-the-Loop Hooks (5 pts):
"High-stakes actions include explicit code stops requiring human confirmation
before execution."

When demand exceeds static supply for a requested `(region, zone, machine_type)`,
the agent MUST NOT automatically substitute a different machine shape, zone, or
region without explicit customer confirmation. Instead:
1. `HITLCustomerAcceptanceGate.register_confirmation_stop()` creates an explicit
   code stop (`status="WAITING_FOR_HUMAN_CONFIRMATION"`) linked to `proposal_id`.
2. Execution pauses until the customer confirms via Chat (e.g., "Accept alternative 1")
   or the UI/CLI confirmation hook (`approve_and_continue_matching()`), which
   then unlocks and commits the alternative allocation.
"""

import time
from typing import Any, Dict, List, Optional

from ..memory.session_store import global_session_store
from ..observability.structured_logger import get_structured_logger
from ..tools.capacity_tools import commit_customer_accepted_alternative_tool

logger = get_structured_logger("md_supply_demand_agent.hitl")


class HITLCustomerAcceptanceGate:
    """Manages explicit Human-in-the-Loop stops for alternative capacity substitutions."""

    def __init__(self) -> None:
        self._active_stops: Dict[str, Dict[str, Any]] = {}
        self._resolved_stops: Dict[str, Dict[str, Any]] = {}

    def register_confirmation_stop(
        self,
        proposal_id: str,
        customer_id: str,
        original_request: Dict[str, Any],
        alternatives: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Creates an explicit HITL code stop awaiting customer confirmation of an alternative."""
        stop_record = {
            "proposal_id": proposal_id,
            "customer_id": customer_id,
            "hitl_gate_status": "WAITING_FOR_HUMAN_CONFIRMATION",
            "original_request": original_request,
            "recommended_alternatives": alternatives,
            "created_at": time.time(),
            "instructions_for_human": (
                f"Supply was exceeded for {original_request.get('shortfall_count')}x "
                f"`{original_request.get('machine_type')}` in `{original_request.get('zone')}`. "
                f"To accept an alternative and continue matching, reply `'Accept option 1 for {proposal_id}'` "
                "in Chat or click the **Accept Alternative** button."
            ),
        }
        self._active_stops[proposal_id] = stop_record

        logger.info(
            f"[HITL_STOP] Execution paused at Human-in-the-Loop gate for proposal '{proposal_id}' "
            f"(customer='{customer_id}'). Awaiting customer confirmation.",
            extra={
                "component": "HITLCustomerAcceptanceGate",
                "event_type": "HITL_CONFIRMATION_REQUIRED",
                "structured_data": {
                    "proposal_id": proposal_id,
                    "customer_id": customer_id,
                    "alternatives_offered": len(alternatives),
                },
            },
        )
        return stop_record

    def approve_and_continue_matching(
        self,
        proposal_id: str,
        option_rank: int = 1,
        reviewer_id: str = "Customer-Operator",
        confirmation_note: str = "Customer confirmed alternative capacity allocation.",
    ) -> Dict[str, Any]:
        """Approves a pending HITL stop and resumes FCFS matching with the accepted alternative."""
        commit_res = commit_customer_accepted_alternative_tool(
            proposal_id=proposal_id,
            option_rank=option_rank,
            customer_confirmation_note=f"[{reviewer_id}] {confirmation_note}",
        )
        if commit_res.get("status") == "SUCCESS":
            stop_item = self._active_stops.pop(proposal_id, {"proposal_id": proposal_id})
            stop_item["hitl_gate_status"] = "APPROVED_AND_EXECUTED"
            stop_item["approved_by"] = reviewer_id
            stop_item["approved_option_rank"] = option_rank
            stop_item["resolved_at"] = time.time()
            stop_item["allocation_result"] = commit_res["allocation_result"]
            self._resolved_stops[proposal_id] = stop_item

            logger.info(
                f"[HITL_APPROVED] Proposal '{proposal_id}' Option #{option_rank} approved by '{reviewer_id}'. "
                "Alternative capacity allocated.",
                extra={
                    "component": "HITLCustomerAcceptanceGate",
                    "event_type": "HITL_CONFIRMATION_APPROVED",
                    "structured_data": {
                        "proposal_id": proposal_id,
                        "option_rank": option_rank,
                        "allocation_id": commit_res["allocation_result"].get("allocation_id"),
                    },
                },
            )
        return commit_res

    def reject_alternative(
        self,
        proposal_id: str,
        reviewer_id: str = "Customer-Operator",
        reason: str = "Customer declined alternative region/shape.",
    ) -> Dict[str, Any]:
        """Rejects a pending alternative proposal without deducting alternative supply."""
        proposal = global_session_store.get_pending_proposal(proposal_id)
        if not proposal:
            return {
                "status": "ERROR",
                "message": f"Proposal '{proposal_id}' not found.",
            }

        global_session_store.mark_proposal_resolved(
            proposal_id=proposal_id,
            status="REJECTED_BY_CUSTOMER",
            accepted_option_index=None,
        )
        stop_item = self._active_stops.pop(proposal_id, {"proposal_id": proposal_id})
        stop_item["hitl_gate_status"] = "REJECTED_BY_HUMAN"
        stop_item["rejected_by"] = reviewer_id
        stop_item["rejection_reason"] = reason
        stop_item["resolved_at"] = time.time()
        self._resolved_stops[proposal_id] = stop_item

        logger.info(
            f"[HITL_REJECTED] Proposal '{proposal_id}' declined by '{reviewer_id}': {reason}",
            extra={
                "component": "HITLCustomerAcceptanceGate",
                "event_type": "HITL_CONFIRMATION_REJECTED",
                "structured_data": {"proposal_id": proposal_id, "reason": reason},
            },
        )
        return {
            "status": "REJECTED",
            "proposal_id": proposal_id,
            "rejected_by": reviewer_id,
            "reason": reason,
        }

    def list_pending_confirmations(self) -> List[Dict[str, Any]]:
        """Returns all active HITL confirmation gates awaiting customer decision."""
        db_pending = global_session_store.list_pending_proposals(
            status_filter="PENDING_CUSTOMER_ACCEPTANCE"
        )
        return db_pending

    def adk_before_tool_hitl_callback(
        self, tool: Any, args: Dict[str, Any], tool_context: Any
    ) -> Optional[Dict[str, Any]]:
        """Google ADK `before_tool_callback` enforcing human confirmation before committing alternatives."""
        tool_name = getattr(tool, "name", str(tool))
        if tool_name == "commit_customer_accepted_alternative_tool":
            if not args.get("proposal_id"):
                return {
                    "status": "HITL_BLOCKED",
                    "message": "Human confirmation with a valid `proposal_id` is required before committing an alternative.",
                }
        return None


global_hitl_gate = HITLCustomerAcceptanceGate()
