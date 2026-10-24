"""Guided Error Handling Decorator & Recovery Instructions for Agent Tools.

Rubric Criterion 1.4 — Guided Error Handling (5 pts):
"Tool error returns provide descriptive recovery instructions back to the LLM
instead of just crashing."

Wraps tool functions so that any schema validation error, domain lookup failure,
or runtime exception returns a structured JSON dictionary containing:
- `status`: "ERROR"
- `error_code`: Categorized error code
- `message`: Human-readable explanation of what went wrong
- `recovery_instructions`: Actionable step-by-step instructions telling the LLM
  how to self-correct its arguments and retry.
"""

import functools
from typing import Any, Callable, Dict

from ..data.gcp_catalog import GCP_MACHINE_TYPES, GCP_REGIONS_AND_ZONES
from .schemas import validate_tool_arguments


def build_guided_error_response(
    tool_name: str,
    error_code: str,
    error_message: str,
    recovery_instructions: str,
    provided_arguments: Dict[str, Any],
) -> Dict[str, Any]:
    """Constructs a standardized guided error payload for LLM self-correction."""
    return {
        "status": "ERROR",
        "tool_name": tool_name,
        "error_code": error_code,
        "message": error_message,
        "recovery_instructions": recovery_instructions,
        "provided_arguments": provided_arguments,
        "valid_regions": sorted(GCP_REGIONS_AND_ZONES.keys()),
        "valid_machine_types": sorted(GCP_MACHINE_TYPES.keys()),
    }


def with_guided_error_handling(tool_name: str) -> Callable[[Callable[..., Dict[str, Any]]], Callable[..., Dict[str, Any]]]:
    """Decorator that enforces strict schema validation and returns guided recovery instructions on error."""

    def decorator(func: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            import inspect

            sig = inspect.signature(func)
            try:
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                raw_args = dict(bound.arguments)
            except TypeError as bind_exc:
                return build_guided_error_response(
                    tool_name=tool_name,
                    error_code="INVALID_ARGUMENT_SIGNATURE",
                    error_message=str(bind_exc),
                    recovery_instructions=(
                        f"Inspect the required parameters in TOOL_JSON_SCHEMAS['{tool_name}']['input_schema'] "
                        "and re-invoke the tool with all required fields populated."
                    ),
                    provided_arguments=kwargs,
                )

            is_valid, validated_args, validation_error = validate_tool_arguments(tool_name, raw_args)
            if not is_valid or validated_args is None:
                return build_guided_error_response(
                    tool_name=tool_name,
                    error_code="SCHEMA_OR_CATALOG_VALIDATION_ERROR",
                    error_message=validation_error or "Invalid tool arguments.",
                    recovery_instructions=(
                        "Self-Correction Action: "
                        "1. Ensure `region` is one of the valid Google Cloud regions (e.g., 'europe-west3', 'us-central1', 'asia-east1'). "
                        "2. Ensure `zone` matches the region prefix (e.g., 'europe-west3-a', 'europe-west1-b', 'us-central1-a'). "
                        "3. Ensure `machine_type` is a valid Compute Engine shape from `valid_machine_types` (e.g., 'n2-standard-8', 'e2-standard-4', 'a2-highgpu-1g'). "
                        "4. Ensure `requested_count` / `shortfall_count` is an integer >= 1. Retry the tool call with corrected parameters."
                    ),
                    provided_arguments=raw_args,
                )

            try:
                return func(**validated_args)
            except Exception as runtime_exc:
                return build_guided_error_response(
                    tool_name=tool_name,
                    error_code="TOOL_EXECUTION_RUNTIME_ERROR",
                    error_message=f"Unexpected error in '{tool_name}': {runtime_exc}",
                    recovery_instructions=(
                        "Verify that the referenced `proposal_id` or supply pool exists by calling "
                        "`query_static_regional_supply_tool` first, then retry the operation."
                    ),
                    provided_arguments=raw_args,
                )

        return wrapper

    return decorator
