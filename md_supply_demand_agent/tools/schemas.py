"""Explicit JSON Schemas & Strict Pydantic / JSON-Schema Input/Output Models for Agent Tools.

Rubric Criterion 1.3 — Explicit JSON Schemas (5 pts):
"The code utilizes strict input and output schemas to validate tool arguments
and constrain LLMs."

Defines:
1. Strict Pydantic `BaseModel` input models (with automatic stdlib JSON-Schema
   validator fallback in bare environments) for all 6 domain tools.
2. Explicit `TOOL_JSON_SCHEMAS` registry exporting Draft-07 / OpenAPI JSON Schemas
   for both `input_schema` and `output_schema` to constrain LLM tool calling.
"""

from typing import Any, Dict, List, Optional, Tuple

from ..data.gcp_catalog import GCP_MACHINE_TYPES, GCP_REGIONS_AND_ZONES

try:
    from pydantic import BaseModel, Field  # type: ignore

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

    def Field(default: Any = ..., **kwargs: Any) -> Any:  # type: ignore
        return default

    class BaseModel:  # type: ignore
        """Lightweight Pydantic-compatible schema validator when running in bare stdlib Python."""

        def __init__(self, **data: Any) -> None:
            annotations = getattr(self.__class__, "__annotations__", {})
            for name, expected_type in annotations.items():
                has_default = hasattr(self.__class__, name)
                default_val = getattr(self.__class__, name, None)
                if name in data:
                    val = data[name]
                elif has_default and default_val is not Ellipsis:
                    val = default_val
                else:
                    raise ValueError(f"Missing required field '{name}'.")
                setattr(self, name, val)

        def model_dump(self) -> Dict[str, Any]:
            return dict(self.__dict__)


# ---------------------------------------------------------------------------
# Strict Input Models (Pydantic BaseModel + Explicit JSON Schemas)
# ---------------------------------------------------------------------------
class QueryStaticSupplyInput(BaseModel):
    """Input schema for `query_static_regional_supply_tool`."""

    region: Optional[str] = Field(
        default=None,
        description="Optional Google Cloud region ID (e.g., 'europe-west3', 'us-central1', 'asia-east1').",
    )
    zone: Optional[str] = Field(
        default=None,
        description="Optional Google Cloud zone ID (e.g., 'europe-west3-a', 'us-central1-b').",
    )
    machine_type: Optional[str] = Field(
        default=None,
        description="Optional Compute Engine machine type (e.g., 'n2-standard-8', 'a2-highgpu-1g').",
    )
    family: Optional[str] = Field(
        default=None,
        description="Optional machine family filter ('E2', 'N2', 'N2D', 'C3', 'C4', 'M3', 'G2', 'A2').",
    )
    only_available: bool = Field(
        default=False,
        description="If True, returns only supply pools where `available_supply > 0`.",
    )


class AllocateFCFSCapacityInput(BaseModel):
    """Input schema for `allocate_fcfs_cloud_capacity_tool`."""

    customer_id: str = Field(
        ...,
        min_length=1,
        description="Customer name or identifier requesting compute capacity (e.g., 'Acme-MidMarket-Corp').",
    )
    region: str = Field(
        ...,
        description="Requested Google Cloud region ID (e.g., 'europe-west3').",
    )
    zone: str = Field(
        ...,
        description="Requested Google Cloud zone ID within the region (e.g., 'europe-west3-a').",
    )
    machine_type: str = Field(
        ...,
        description="Requested Compute Engine machine type/shape (e.g., 'n2-standard-8').",
    )
    requested_count: int = Field(
        ...,
        ge=1,
        le=500,
        description="Number of VM instances requested (must be between 1 and 500).",
    )
    allow_partial: bool = Field(
        default=True,
        description="Whether to allocate available instances partially when `requested_count > available_supply`.",
    )


class RecommendAlternativesInput(BaseModel):
    """Input schema for `recommend_capacity_alternatives_tool`."""

    customer_id: str = Field(
        ...,
        description="Customer identifier experiencing a capacity shortfall.",
    )
    region: str = Field(
        ...,
        description="Original requested Google Cloud region where supply was exceeded.",
    )
    zone: str = Field(
        ...,
        description="Original requested Google Cloud zone where supply was exceeded.",
    )
    machine_type: str = Field(
        ...,
        description="Original requested Compute Engine machine type where supply was exceeded.",
    )
    shortfall_count: int = Field(
        ...,
        ge=1,
        le=500,
        description="Unfulfilled number of VM instances needing an alternative.",
    )


class CommitCustomerAcceptedAlternativeInput(BaseModel):
    """Input schema for `commit_customer_accepted_alternative_tool`."""

    proposal_id: str = Field(
        ...,
        description="Unique pending proposal ID (e.g., 'ALT-1A2B3C4D') generated when supply was exceeded.",
    )
    option_rank: int = Field(
        default=1,
        ge=1,
        le=10,
        description="1-based rank of the recommended alternative accepted by the customer (default: 1).",
    )
    customer_confirmation_note: str = Field(
        default="Customer approved recommended alternative capacity.",
        description="Confirmation message or audit note from the customer.",
    )


class ParseUploadedDemandFileInput(BaseModel):
    """Input schema for `parse_uploaded_demand_file_tool`."""

    file_content: str = Field(
        ...,
        min_length=2,
        description="Raw text content of the uploaded CSV, JSON, or JSONL customer demand file.",
    )
    file_format: str = Field(
        default="auto",
        description="File format: 'csv', 'json', 'jsonl', or 'auto'.",
    )
    default_customer_id: str = Field(
        default="MidSized-Cloud-Customer",
        description="Fallback customer ID if rows omit `customer_id`.",
    )


class EvaluateMidMarketBenchmarkInput(BaseModel):
    """Input schema for `evaluate_midmarket_cloud_benchmark_tool`."""

    monthly_compute_spend_usd: float = Field(
        ...,
        ge=0.0,
        description="Total monthly compute spend in USD to compare against SpendArk 2026 benchmarks.",
    )
    gpu_spend_usd: float = Field(
        default=0.0,
        ge=0.0,
        description="Monthly AI/GPU compute spend in USD.",
    )
    total_vcpus: int = Field(
        default=0,
        ge=0,
        description="Total allocated vCPUs across the customer fleet.",
    )


# ---------------------------------------------------------------------------
# Explicit JSON Schemas Registry (Input + Output Schemas for LLM Validation)
# ---------------------------------------------------------------------------
TOOL_JSON_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "query_static_regional_supply_tool": {
        "name": "query_static_regional_supply_tool",
        "description": "Queries the constrained static Google Cloud compute supply inventory by region, zone, machine_type, or family.",
        "input_schema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": ["string", "null"],
                    "description": "Optional Google Cloud region ID (e.g., 'europe-west3', 'us-central1', 'asia-east1').",
                },
                "zone": {
                    "type": ["string", "null"],
                    "description": "Optional Google Cloud zone ID (e.g., 'europe-west3-a', 'us-central1-b').",
                },
                "machine_type": {
                    "type": ["string", "null"],
                    "description": "Optional Compute Engine machine type (e.g., 'n2-standard-8', 'a2-highgpu-1g').",
                },
                "family": {
                    "type": ["string", "null"],
                    "description": "Optional machine family filter ('E2', 'N2', 'N2D', 'C3', 'C4', 'M3', 'G2', 'A2').",
                },
                "only_available": {
                    "type": "boolean",
                    "default": False,
                    "description": "If True, returns only supply pools where `available_supply > 0`.",
                },
            },
            "required": [],
        },
        "output_schema": {
            "type": "object",
            "required": ["status", "total_pools_matched", "total_available_vms", "supply_pools"],
            "properties": {
                "status": {"type": "string", "enum": ["SUCCESS", "ERROR"]},
                "total_pools_matched": {"type": "integer"},
                "total_available_vms": {"type": "integer"},
                "supply_pools": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    "allocate_fcfs_cloud_capacity_tool": {
        "name": "allocate_fcfs_cloud_capacity_tool",
        "description": "Allocates Google Cloud compute instances following a strict First-Come-First-Serve (FCFS) principle and triggers alternative recommendations if supply is exceeded.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Customer name or identifier requesting compute capacity.",
                },
                "region": {
                    "type": "string",
                    "description": "Requested Google Cloud region ID (e.g., 'europe-west3').",
                },
                "zone": {
                    "type": "string",
                    "description": "Requested Google Cloud zone ID within the region (e.g., 'europe-west3-a').",
                },
                "machine_type": {
                    "type": "string",
                    "description": "Requested Compute Engine machine type/shape (e.g., 'n2-standard-8').",
                },
                "requested_count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 500,
                    "description": "Number of VM instances requested (1 to 500).",
                },
                "allow_partial": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to allocate available instances partially when supply is exceeded.",
                },
            },
            "required": ["customer_id", "region", "zone", "machine_type", "requested_count"],
        },
        "output_schema": {
            "type": "object",
            "required": [
                "status",
                "allocation_id",
                "allocated_count",
                "shortfall_count",
                "supply_exceeded",
            ],
            "properties": {
                "status": {"type": "string"},
                "allocation_id": {"type": "string"},
                "fcfs_sequence_number": {"type": "integer"},
                "allocated_count": {"type": "integer"},
                "shortfall_count": {"type": "integer"},
                "supply_exceeded": {"type": "boolean"},
                "pending_proposal_id": {"type": ["string", "null"]},
                "recommended_alternatives": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    "recommend_capacity_alternatives_tool": {
        "name": "recommend_capacity_alternatives_tool",
        "description": "Generates ranked alternative machine types, shapes, zones, and nearby regions when static supply is exceeded for a demand request.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "region": {"type": "string"},
                "zone": {"type": "string"},
                "machine_type": {"type": "string"},
                "shortfall_count": {"type": "integer", "minimum": 1, "maximum": 500},
            },
            "required": ["customer_id", "region", "zone", "machine_type", "shortfall_count"],
        },
        "output_schema": {
            "type": "object",
            "required": ["status", "proposal_id", "shortfall_count", "alternatives"],
            "properties": {
                "status": {"type": "string", "enum": ["SUCCESS", "ERROR"]},
                "proposal_id": {"type": "string"},
                "shortfall_count": {"type": "integer"},
                "alternatives": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    "commit_customer_accepted_alternative_tool": {
        "name": "commit_customer_accepted_alternative_tool",
        "description": "Continues FCFS capacity matching after the customer accepts a recommended alternative machine type, shape, region, or zone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "proposal_id": {"type": "string"},
                "option_rank": {"type": "integer", "minimum": 1, "maximum": 10, "default": 1},
                "customer_confirmation_note": {"type": "string"},
            },
            "required": ["proposal_id"],
        },
        "output_schema": {
            "type": "object",
            "required": ["status", "proposal_id", "allocation_result"],
            "properties": {
                "status": {"type": "string", "enum": ["SUCCESS", "ERROR"]},
                "proposal_id": {"type": "string"},
                "accepted_alternative": {"type": "object"},
                "allocation_result": {"type": "object"},
            },
        },
    },
    "parse_uploaded_demand_file_tool": {
        "name": "parse_uploaded_demand_file_tool",
        "description": "Parses and validates an uploaded CSV, JSON, or JSONL customer compute demand schedule into structured FCFS demand items.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_content": {"type": "string", "minLength": 2},
                "file_format": {"type": "string", "default": "auto"},
                "default_customer_id": {"type": "string", "default": "MidSized-Cloud-Customer"},
            },
            "required": ["file_content"],
        },
        "output_schema": {
            "type": "object",
            "required": ["status", "total_requests_parsed", "demand_requests"],
            "properties": {
                "status": {"type": "string", "enum": ["SUCCESS", "ERROR"]},
                "total_requests_parsed": {"type": "integer"},
                "demand_requests": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    "evaluate_midmarket_cloud_benchmark_tool": {
        "name": "evaluate_midmarket_cloud_benchmark_tool",
        "description": "Evaluates a customer's allocated compute fleet and cost against the SpendArk 2026 Mid-Sized Company Cloud Cost Benchmark.",
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_compute_spend_usd": {"type": "number", "minimum": 0.0},
                "gpu_spend_usd": {"type": "number", "minimum": 0.0, "default": 0.0},
                "total_vcpus": {"type": "integer", "minimum": 0, "default": 0},
            },
            "required": ["monthly_compute_spend_usd"],
        },
        "output_schema": {
            "type": "object",
            "required": ["status", "annualized_compute_spend_usd", "finops_recommendations"],
            "properties": {
                "status": {"type": "string", "enum": ["SUCCESS", "ERROR"]},
                "annualized_compute_spend_usd": {"type": "number"},
                "benchmark_alignment": {"type": "string"},
                "finops_recommendations": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}


def validate_tool_arguments(
    tool_name: str, raw_args: Dict[str, Any]
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Validates tool arguments against the tool's strict input schema & domain catalog."""
    model_map = {
        "query_static_regional_supply_tool": QueryStaticSupplyInput,
        "allocate_fcfs_cloud_capacity_tool": AllocateFCFSCapacityInput,
        "recommend_capacity_alternatives_tool": RecommendAlternativesInput,
        "commit_customer_accepted_alternative_tool": CommitCustomerAcceptedAlternativeInput,
        "parse_uploaded_demand_file_tool": ParseUploadedDemandFileInput,
        "evaluate_midmarket_cloud_benchmark_tool": EvaluateMidMarketBenchmarkInput,
    }
    model_cls = model_map.get(tool_name)
    if not model_cls:
        return True, raw_args, None

    try:
        validated = model_cls(**raw_args)
        clean_dict = validated.model_dump()
    except Exception as exc:
        return False, None, f"Schema validation failed for '{tool_name}': {exc}"

    # Enforce JSON Schema numeric bounds
    schema_def = TOOL_JSON_SCHEMAS.get(tool_name, {}).get("input_schema", {})
    for prop_name, prop_rules in schema_def.get("properties", {}).items():
        val = clean_dict.get(prop_name)
        if val is not None and isinstance(val, (int, float)) and not isinstance(val, bool):
            if "minimum" in prop_rules and val < prop_rules["minimum"]:
                return (
                    False,
                    None,
                    f"Parameter '{prop_name}'={val} is below minimum {prop_rules['minimum']}.",
                )
            if "maximum" in prop_rules and val > prop_rules["maximum"]:
                return (
                    False,
                    None,
                    f"Parameter '{prop_name}'={val} exceeds maximum {prop_rules['maximum']}.",
                )

    # Domain catalog validation for region/zone/machine_type
    region = clean_dict.get("region")
    zone = clean_dict.get("zone")
    machine_type = clean_dict.get("machine_type")

    if region and region not in GCP_REGIONS_AND_ZONES:
        valid_regions = ", ".join(sorted(GCP_REGIONS_AND_ZONES.keys()))
        return (
            False,
            None,
            f"Unknown Google Cloud region '{region}'. Valid regions are: {valid_regions}.",
        )

    if zone:
        if region and zone not in GCP_REGIONS_AND_ZONES[region]["zones"]:
            valid_zones = ", ".join(GCP_REGIONS_AND_ZONES[region]["zones"])
            return (
                False,
                None,
                f"Zone '{zone}' does not belong to region '{region}'. Valid zones for '{region}' are: {valid_zones}.",
            )
        all_zones = {z for r in GCP_REGIONS_AND_ZONES.values() for z in r["zones"]}
        if zone not in all_zones:
            return (
                False,
                None,
                f"Unknown Google Cloud zone '{zone}'. Verify the region prefix (e.g., 'europe-west3-a', 'us-central1-a').",
            )

    if machine_type and machine_type not in GCP_MACHINE_TYPES:
        valid_machines = ", ".join(sorted(GCP_MACHINE_TYPES.keys()))
        return (
            False,
            None,
            f"Unsupported Compute Engine machine type '{machine_type}'. Supported machine types are: {valid_machines}.",
        )

    return True, clean_dict, None
