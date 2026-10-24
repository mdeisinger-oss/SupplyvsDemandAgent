"""Grounded GCP Location, Machine Type, and SpendArk 2026 Benchmark Data."""

from .gcp_catalog import (
    GCP_MACHINE_TYPES,
    GCP_REGIONS_AND_ZONES,
    KNOWLEDGE_BASE_DOCUMENTS,
    SPENDARK_2026_MID_MARKET_BENCHMARK,
    build_default_static_supply_inventory,
)

__all__ = [
    "GCP_REGIONS_AND_ZONES",
    "GCP_MACHINE_TYPES",
    "SPENDARK_2026_MID_MARKET_BENCHMARK",
    "KNOWLEDGE_BASE_DOCUMENTS",
    "build_default_static_supply_inventory",
]
