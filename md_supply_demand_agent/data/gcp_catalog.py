"""Grounded Domain Catalog for MD-Supply-vs-Demand-Agent.

Synthesizes reference data from three authoritative sources:
1. Google Cloud Regions and Zones: https://cloud.google.com/about/locations?hl=de
2. Google Cloud Machine Types and Shapes: https://docs.cloud.google.com/compute/docs/machine-resource
3. Mid-Sized Company Cloud Demand Benchmark (2026): https://spendark.com/blog/cloud-cost-benchmark-2026/
"""

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Source 1: Google Cloud Regions and Zones
# Reference: https://cloud.google.com/about/locations?hl=de
# ---------------------------------------------------------------------------
GCP_REGIONS_AND_ZONES: Dict[str, Dict[str, Any]] = {
    "europe-west3": {
        "region": "europe-west3",
        "display_name": "Frankfurt, Deutschland (europe-west3)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west3-a", "europe-west3-b", "europe-west3-c"],
        "nearby_regions": ["europe-west4", "europe-west1", "europe-west10", "europe-west6"],
        "latency_tier_ms": {"europe-west4": 7.5, "europe-west1": 8.2, "europe-west10": 9.0, "europe-west6": 6.8},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "europe-west4": {
        "region": "europe-west4",
        "display_name": "Eemshaven, Niederlande (europe-west4)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west4-a", "europe-west4-b", "europe-west4-c"],
        "nearby_regions": ["europe-west1", "europe-west3", "europe-west2", "europe-west10"],
        "latency_tier_ms": {"europe-west1": 5.4, "europe-west3": 7.5, "europe-west2": 9.1, "europe-west10": 10.2},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "europe-west1": {
        "region": "europe-west1",
        "display_name": "St. Ghislain, Belgien (europe-west1)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west1-b", "europe-west1-c", "europe-west1-d"],
        "nearby_regions": ["europe-west4", "europe-west2", "europe-west3"],
        "latency_tier_ms": {"europe-west4": 5.4, "europe-west2": 6.5, "europe-west3": 8.2},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "europe-west2": {
        "region": "europe-west2",
        "display_name": "London, Vereinigtes Königreich (europe-west2)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west2-a", "europe-west2-b", "europe-west2-c"],
        "nearby_regions": ["europe-west1", "europe-west4", "europe-west3"],
        "latency_tier_ms": {"europe-west1": 6.5, "europe-west4": 9.1, "europe-west3": 12.4},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "europe-west10": {
        "region": "europe-west10",
        "display_name": "Berlin, Deutschland (europe-west10)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west10-a", "europe-west10-b", "europe-west10-c"],
        "nearby_regions": ["europe-west3", "europe-west4", "europe-west1"],
        "latency_tier_ms": {"europe-west3": 9.0, "europe-west4": 10.2, "europe-west1": 13.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "europe-west6": {
        "region": "europe-west6",
        "display_name": "Zürich, Schweiz (europe-west6)",
        "MacroGeography": "EUROPE",
        "zones": ["europe-west6-a", "europe-west6-b", "europe-west6-c"],
        "nearby_regions": ["europe-west3", "europe-west1", "europe-west4"],
        "latency_tier_ms": {"europe-west3": 6.8, "europe-west1": 11.2, "europe-west4": 12.5},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "us-central1": {
        "region": "us-central1",
        "display_name": "Council Bluffs, Iowa, USA (us-central1)",
        "MacroGeography": "AMERICAS",
        "zones": ["us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f"],
        "nearby_regions": ["us-east1", "us-east4", "us-west1"],
        "latency_tier_ms": {"us-east1": 22.0, "us-east4": 20.5, "us-west1": 32.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "us-east1": {
        "region": "us-east1",
        "display_name": "Moncks Corner, South Carolina, USA (us-east1)",
        "MacroGeography": "AMERICAS",
        "zones": ["us-east1-b", "us-east1-c", "us-east1-d"],
        "nearby_regions": ["us-east4", "us-central1", "us-west1"],
        "latency_tier_ms": {"us-east4": 11.5, "us-central1": 22.0, "us-west1": 54.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "us-east4": {
        "region": "us-east4",
        "display_name": "Ashburn, Northern Virginia, USA (us-east4)",
        "MacroGeography": "AMERICAS",
        "zones": ["us-east4-a", "us-east4-b", "us-east4-c"],
        "nearby_regions": ["us-east1", "us-central1", "us-west1"],
        "latency_tier_ms": {"us-east1": 11.5, "us-central1": 20.5, "us-west1": 52.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "us-west1": {
        "region": "us-west1",
        "display_name": "The Dalles, Oregon, USA (us-west1)",
        "MacroGeography": "AMERICAS",
        "zones": ["us-west1-a", "us-west1-b", "us-west1-c"],
        "nearby_regions": ["us-central1", "us-east4", "us-east1"],
        "latency_tier_ms": {"us-central1": 32.0, "us-east4": 52.0, "us-east1": 54.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "asia-east1": {
        "region": "asia-east1",
        "display_name": "Changhua County, Taiwan (asia-east1)",
        "MacroGeography": "APAC",
        "zones": ["asia-east1-a", "asia-east1-b", "asia-east1-c"],
        "nearby_regions": ["asia-northeast1", "asia-southeast1"],
        "latency_tier_ms": {"asia-northeast1": 33.0, "asia-southeast1": 42.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "asia-northeast1": {
        "region": "asia-northeast1",
        "display_name": "Tokio, Japan (asia-northeast1)",
        "MacroGeography": "APAC",
        "zones": ["asia-northeast1-a", "asia-northeast1-b", "asia-northeast1-c"],
        "nearby_regions": ["asia-east1", "asia-southeast1"],
        "latency_tier_ms": {"asia-east1": 33.0, "asia-southeast1": 65.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
    "asia-southeast1": {
        "region": "asia-southeast1",
        "display_name": "Jurong West, Singapur (asia-southeast1)",
        "MacroGeography": "APAC",
        "zones": ["asia-southeast1-a", "asia-southeast1-b", "asia-southeast1-c"],
        "nearby_regions": ["asia-east1", "asia-northeast1"],
        "latency_tier_ms": {"asia-east1": 42.0, "asia-northeast1": 65.0},
        "source_url": "https://cloud.google.com/about/locations?hl=de",
    },
}


# ---------------------------------------------------------------------------
# Source 2: Google Cloud Compute Engine Machine Types & Shapes
# Reference: https://docs.cloud.google.com/compute/docs/machine-resource
# ---------------------------------------------------------------------------
GCP_MACHINE_TYPES: Dict[str, Dict[str, Any]] = {
    "e2-standard-4": {
        "machine_type": "e2-standard-4",
        "family": "E2",
        "category": "General-Purpose (Cost-Optimized)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 4,
        "memory_gb": 16.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon / AMD EPYC (Dynamic Resource Allocation)",
        "hourly_price_usd": 0.134,
        "monthly_on_demand_usd": 97.82,
        "compatible_alternatives": ["n2d-standard-4", "e2-standard-8", "n2-standard-4", "e2-highmem-4"],
        "workload_fit": "Web servers, microservices, non-prod CI/CD, small databases",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "e2-standard-8": {
        "machine_type": "e2-standard-8",
        "family": "E2",
        "category": "General-Purpose (Cost-Optimized)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon / AMD EPYC (Dynamic Resource Allocation)",
        "hourly_price_usd": 0.268,
        "monthly_on_demand_usd": 195.64,
        "compatible_alternatives": ["n2d-standard-8", "n2-standard-8", "c3-standard-8", "e2-standard-4"],
        "workload_fit": "Containerized microservices, Kubernetes node pools, medium app backends",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "e2-highmem-4": {
        "machine_type": "e2-highmem-4",
        "family": "E2",
        "category": "General-Purpose (Cost-Optimized)",
        "shape": "highmem (8 GB / vCPU)",
        "vcpus": 4,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon / AMD EPYC",
        "hourly_price_usd": 0.180,
        "monthly_on_demand_usd": 131.40,
        "compatible_alternatives": ["e2-standard-8", "n2-highmem-8", "n2d-standard-8"],
        "workload_fit": "Caching tiers, memory-intensive microservices, small relational DBs",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2-standard-4": {
        "machine_type": "n2-standard-4",
        "family": "N2",
        "category": "General-Purpose (Balanced)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 4,
        "memory_gb": 16.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon Scalable (Cascade Lake / Ice Lake)",
        "hourly_price_usd": 0.194,
        "monthly_on_demand_usd": 141.62,
        "compatible_alternatives": ["n2d-standard-4", "e2-standard-4", "n2-standard-8", "c3-standard-8"],
        "workload_fit": "Enterprise application servers, web tiers, medium relational databases",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2-standard-8": {
        "machine_type": "n2-standard-8",
        "family": "N2",
        "category": "General-Purpose (Balanced)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon Scalable (Cascade Lake / Ice Lake)",
        "hourly_price_usd": 0.388,
        "monthly_on_demand_usd": 283.24,
        "compatible_alternatives": ["n2d-standard-8", "c3-standard-8", "c4-standard-8", "e2-standard-8", "n2-standard-16"],
        "workload_fit": "Production GKE clusters, enterprise backends, transactional databases",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2-standard-16": {
        "machine_type": "n2-standard-16",
        "family": "N2",
        "category": "General-Purpose (Balanced)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 16,
        "memory_gb": 64.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon Scalable (Cascade Lake / Ice Lake)",
        "hourly_price_usd": 0.777,
        "monthly_on_demand_usd": 567.21,
        "compatible_alternatives": ["n2d-standard-16", "n2-standard-8", "c3-highcpu-16", "c4-highcpu-16"],
        "workload_fit": "Large monoliths, high-throughput enterprise middleware, distributed data nodes",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2-highmem-8": {
        "machine_type": "n2-highmem-8",
        "family": "N2",
        "category": "General-Purpose (Balanced)",
        "shape": "highmem (8 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 64.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Intel Xeon Scalable (Cascade Lake / Ice Lake)",
        "hourly_price_usd": 0.524,
        "monthly_on_demand_usd": 382.52,
        "compatible_alternatives": ["n2-standard-16", "n2d-standard-16", "e2-highmem-4", "m3-megamem-64"],
        "workload_fit": "PostgreSQL/MySQL primary nodes, Redis/Memcached clusters, search indices",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2d-standard-4": {
        "machine_type": "n2d-standard-4",
        "family": "N2D",
        "category": "General-Purpose (Balanced AMD)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 4,
        "memory_gb": 16.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "AMD EPYC (Rome / Milan)",
        "hourly_price_usd": 0.169,
        "monthly_on_demand_usd": 123.37,
        "compatible_alternatives": ["e2-standard-4", "n2-standard-4", "n2d-standard-8"],
        "workload_fit": "Cost-efficient general enterprise workloads, web services",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2d-standard-8": {
        "machine_type": "n2d-standard-8",
        "family": "N2D",
        "category": "General-Purpose (Balanced AMD)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "AMD EPYC (Rome / Milan)",
        "hourly_price_usd": 0.338,
        "monthly_on_demand_usd": 246.74,
        "compatible_alternatives": ["n2-standard-8", "e2-standard-8", "c3-standard-8", "n2d-standard-16"],
        "workload_fit": "Scale-out production clusters, batch data pipelines, web tiers",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "n2d-standard-16": {
        "machine_type": "n2d-standard-16",
        "family": "N2D",
        "category": "General-Purpose (Balanced AMD)",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 16,
        "memory_gb": 64.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "AMD EPYC (Rome / Milan)",
        "hourly_price_usd": 0.676,
        "monthly_on_demand_usd": 493.48,
        "compatible_alternatives": ["n2-standard-16", "n2d-standard-8", "c3-highcpu-16"],
        "workload_fit": "High-concurrency backend workloads, video encoding, analytics",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "c3-standard-8": {
        "machine_type": "c3-standard-8",
        "family": "C3",
        "category": "Compute-Optimized",
        "shape": "standard (4 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "4th Gen Intel Xeon Scalable (Sapphire Rapids) + Titanium DPU",
        "hourly_price_usd": 0.418,
        "monthly_on_demand_usd": 305.14,
        "compatible_alternatives": ["c4-standard-8", "n2-standard-8", "n2d-standard-8", "c3-highcpu-16"],
        "workload_fit": "High-performance computing (HPC), low-latency API gateways, ad-serving",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "c3-highcpu-16": {
        "machine_type": "c3-highcpu-16",
        "family": "C3",
        "category": "Compute-Optimized",
        "shape": "highcpu (2 GB / vCPU)",
        "vcpus": 16,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "4th Gen Intel Xeon Scalable (Sapphire Rapids) + Titanium DPU",
        "hourly_price_usd": 0.682,
        "monthly_on_demand_usd": 497.86,
        "compatible_alternatives": ["c4-highcpu-16", "c3-standard-8", "n2-standard-16", "n2d-standard-16"],
        "workload_fit": "CPU-bound batch processing, scientific modeling, multiplayer game servers",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "c4-standard-8": {
        "machine_type": "c4-standard-8",
        "family": "C4",
        "category": "Compute-Optimized (Latest Generation)",
        "shape": "standard (3.75 GB / vCPU)",
        "vcpus": 8,
        "memory_gb": 30.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "5th Gen Intel Xeon (Emerald/Granite Rapids) + Titanium",
        "hourly_price_usd": 0.456,
        "monthly_on_demand_usd": 332.88,
        "compatible_alternatives": ["c3-standard-8", "n2-standard-8", "c4-highcpu-16"],
        "workload_fit": "Ultra-consistent NUMA-bound compute workloads, financial risk engines",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "c4-highcpu-16": {
        "machine_type": "c4-highcpu-16",
        "family": "C4",
        "category": "Compute-Optimized (Latest Generation)",
        "shape": "highcpu (2 GB / vCPU)",
        "vcpus": 16,
        "memory_gb": 32.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "5th Gen Intel Xeon (Emerald/Granite Rapids) + Titanium",
        "hourly_price_usd": 0.740,
        "monthly_on_demand_usd": 540.20,
        "compatible_alternatives": ["c3-highcpu-16", "c4-standard-8", "n2-standard-16"],
        "workload_fit": "High-frequency analytics, low-latency trading & real-time telemetry",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "m3-megamem-64": {
        "machine_type": "m3-megamem-64",
        "family": "M3",
        "category": "Memory-Optimized",
        "shape": "megamem (30.5 GB / vCPU)",
        "vcpus": 64,
        "memory_gb": 1952.0,
        "gpus": 0,
        "gpu_model": None,
        "cpu_platform": "Enterprise Intel Xeon Scalable",
        "hourly_price_usd": 6.320,
        "monthly_on_demand_usd": 4613.60,
        "compatible_alternatives": ["n2-highmem-8", "n2-standard-16"],
        "workload_fit": "SAP HANA, large in-memory ERP databases, real-time OLAP warehouses",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "g2-standard-8": {
        "machine_type": "g2-standard-8",
        "family": "G2",
        "category": "Accelerator-Optimized (Inference & Graphics)",
        "shape": "gpu-standard (1x NVIDIA L4, 8 vCPU, 32 GB RAM)",
        "vcpus": 8,
        "memory_gb": 32.0,
        "gpus": 1,
        "gpu_model": "NVIDIA L4 (24 GB VRAM)",
        "cpu_platform": "Intel Cascade Lake + NVIDIA L4 Tensor Core GPU",
        "hourly_price_usd": 0.898,
        "monthly_on_demand_usd": 655.54,
        "compatible_alternatives": ["g2-standard-24", "a2-highgpu-1g", "c3-standard-8"],
        "workload_fit": "LLM inference serving, media transcoding, real-time computer vision",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "g2-standard-24": {
        "machine_type": "g2-standard-24",
        "family": "G2",
        "category": "Accelerator-Optimized (Inference & Graphics)",
        "shape": "gpu-standard (2x NVIDIA L4, 24 vCPU, 96 GB RAM)",
        "vcpus": 24,
        "memory_gb": 96.0,
        "gpus": 2,
        "gpu_model": "2x NVIDIA L4 (48 GB Total VRAM)",
        "cpu_platform": "Intel Cascade Lake + 2x NVIDIA L4 GPUs",
        "hourly_price_usd": 1.984,
        "monthly_on_demand_usd": 1448.32,
        "compatible_alternatives": ["g2-standard-8", "a2-highgpu-1g", "a2-highgpu-4g"],
        "workload_fit": "Multi-GPU AI model serving, 3D rendering pipelines",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "a2-highgpu-1g": {
        "machine_type": "a2-highgpu-1g",
        "family": "A2",
        "category": "Accelerator-Optimized (Training & HPC)",
        "shape": "highgpu (1x NVIDIA A100 40GB, 12 vCPU, 85 GB RAM)",
        "vcpus": 12,
        "memory_gb": 85.0,
        "gpus": 1,
        "gpu_model": "NVIDIA A100 (40 GB HBM2)",
        "cpu_platform": "Intel Cascade Lake + NVIDIA A100 Tensor Core GPU",
        "hourly_price_usd": 3.673,
        "monthly_on_demand_usd": 2681.29,
        "compatible_alternatives": ["g2-standard-24", "g2-standard-8", "a2-highgpu-4g"],
        "workload_fit": "Deep learning fine-tuning, foundation model training, scientific HPC",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
    "a2-highgpu-4g": {
        "machine_type": "a2-highgpu-4g",
        "family": "A2",
        "category": "Accelerator-Optimized (Training & HPC)",
        "shape": "highgpu (4x NVIDIA A100 40GB, 48 vCPU, 340 GB RAM)",
        "vcpus": 48,
        "memory_gb": 340.0,
        "gpus": 4,
        "gpu_model": "4x NVIDIA A100 (160 GB Total HBM2)",
        "cpu_platform": "Intel Cascade Lake + 4x NVIDIA A100 Tensor Core GPUs",
        "hourly_price_usd": 14.693,
        "monthly_on_demand_usd": 10725.89,
        "compatible_alternatives": ["a2-highgpu-1g", "g2-standard-24"],
        "workload_fit": "Distributed multi-GPU LLM training and large-scale simulation",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
    },
}


# ---------------------------------------------------------------------------
# Source 3: SpendArk Cloud Cost Benchmark 2026 (Mid-Sized Company Profile)
# Reference: https://spendark.com/blog/cloud-cost-benchmark-2026/
# ---------------------------------------------------------------------------
SPENDARK_2026_MID_MARKET_BENCHMARK: Dict[str, Any] = {
    "source_title": "SpendArk Cloud Cost Benchmark Report 2026",
    "source_url": "https://spendark.com/blog/cloud-cost-benchmark-2026/",
    "company_segment": "Mid-Sized Enterprise (250–1,000 Employees / $50M–$300M Revenue)",
    "annual_cloud_spend_range_usd": [2000000, 5000000],
    "monthly_cloud_spend_typical_usd": 285000,
    "compute_share_of_bill_pct_range": [45.0, 55.0],
    "ai_gpu_workload_share_pct_range": [15.0, 19.0],
    "cloud_share_of_total_it_budget_pct_range": [35.0, 45.0],
    "saas_revenue_to_cloud_spend_pct_range": [8.0, 15.0],
    "average_cloud_waste_pct_range": [27.0, 33.0],
    "primary_waste_drivers": [
        "Over-provisioned Kubernetes CPU/memory requests (<50% actual utilization)",
        "Idle non-production (dev/staging/QA) environments running 168 hours/week instead of 45 active business hours",
        "Unattached persistent disks and oversized general-purpose Intel VMs where AMD EPYC (N2D) or E2 shapes suffice",
    ],
    "target_commitment_coverage_pct_range": [50.0, 60.0],
    "typical_mid_sized_fleet_breakdown": [
        {
            "tier": "Production Kubernetes & Microservices",
            "machine_types": ["n2-standard-8", "n2d-standard-8", "e2-standard-8"],
            "typical_instance_count": 25,
            "preferred_regions": ["europe-west3", "us-central1"],
        },
        {
            "tier": "Non-Production Dev / Staging / CI",
            "machine_types": ["e2-standard-4", "n2d-standard-4"],
            "typical_instance_count": 20,
            "preferred_regions": ["europe-west3", "europe-west4", "us-east1"],
        },
        {
            "tier": "High-Throughput API & Compute Engines",
            "machine_types": ["c3-standard-8", "c3-highcpu-16", "c4-standard-8"],
            "typical_instance_count": 12,
            "preferred_regions": ["europe-west3", "us-east4"],
        },
        {
            "tier": "Transactional & In-Memory Databases",
            "machine_types": ["n2-highmem-8", "m3-megamem-64"],
            "typical_instance_count": 6,
            "preferred_regions": ["europe-west3", "us-central1"],
        },
        {
            "tier": "Generative AI Inference & ML Training (15%–19% Spend)",
            "machine_types": ["g2-standard-8", "g2-standard-24", "a2-highgpu-1g"],
            "typical_instance_count": 6,
            "preferred_regions": ["us-central1", "europe-west4", "asia-east1"],
        },
    ],
}


def build_default_static_supply_inventory() -> List[Dict[str, Any]]:
    """Generates the deterministic, constrained static supply inventory across all GCP regions & zones.

    Intentionally models realistic datacenter capacity constraints so that standard
    requests succeed via FCFS while large surges or scarce GPU/Megamem requests
    trigger partial/full shortfalls and alternative recommendations.
    """
    base_zone_quotas: Dict[str, int] = {
        "e2-standard-4": 24,
        "e2-standard-8": 18,
        "e2-highmem-4": 14,
        "n2-standard-4": 16,
        "n2-standard-8": 10,     # Constrained in primary zones to demonstrate FCFS depletion
        "n2-standard-16": 8,
        "n2-highmem-8": 8,
        "n2d-standard-4": 22,
        "n2d-standard-8": 20,    # Abundant AMD alternative when n2-standard-8 is exhausted
        "n2d-standard-16": 12,
        "c3-standard-8": 12,
        "c3-highcpu-16": 8,
        "c4-standard-8": 10,
        "c4-highcpu-16": 6,
        "m3-megamem-64": 2,      # Scarce SAP HANA megamem nodes
        "g2-standard-8": 6,      # Constrained L4 GPU inference capacity
        "g2-standard-24": 4,
        "a2-highgpu-1g": 3,      # Highly constrained A100 GPU capacity
        "a2-highgpu-4g": 1,
    }

    inventory: List[Dict[str, Any]] = []
    for region_id, region_meta in GCP_REGIONS_AND_ZONES.items():
        for idx, zone_id in enumerate(region_meta["zones"]):
            # Vary capacity slightly across zones a, b, c so sibling zones can serve as alternatives
            zone_multiplier = 1.0 if idx == 0 else (1.25 if idx == 1 else 1.4)
            for m_type, base_qty in base_zone_quotas.items():
                m_meta = GCP_MACHINE_TYPES[m_type]
                initial_supply = max(1, int(round(base_qty * zone_multiplier)))
                # Make europe-west3-a and us-central1-a slightly tighter on n2-standard-8 and a2-highgpu-1g
                if zone_id in ("europe-west3-a", "us-central1-a") and m_type == "n2-standard-8":
                    initial_supply = 10
                if zone_id in ("europe-west3-a", "us-central1-a") and m_type == "a2-highgpu-1g":
                    initial_supply = 2

                inventory.append(
                    {
                        "region": region_id,
                        "zone": zone_id,
                        "machine_type": m_type,
                        "family": m_meta["family"],
                        "category": m_meta["category"],
                        "shape": m_meta["shape"],
                        "vcpus": m_meta["vcpus"],
                        "memory_gb": m_meta["memory_gb"],
                        "gpus": m_meta["gpus"],
                        "hourly_price_usd": m_meta["hourly_price_usd"],
                        "initial_supply": initial_supply,
                        "available_supply": initial_supply,
                        "allocated_supply": 0,
                    }
                )
    return inventory


KNOWLEDGE_BASE_DOCUMENTS: List[Dict[str, str]] = [
    {
        "doc_id": "GCP-LOC-001",
        "title": "Google Cloud Global Locations — Regions and Zones",
        "source_url": "https://cloud.google.com/about/locations?hl=de",
        "section": "European, American, and APAC Regions & Zones",
        "content": (
            "Google Cloud operates isolated failure domains called zones within geographical regions. "
            "Key European regions include europe-west3 (Frankfurt: europe-west3-a, europe-west3-b, europe-west3-c), "
            "europe-west4 (Netherlands: europe-west4-a, b, c), europe-west1 (Belgium: europe-west1-b, c, d), "
            "europe-west2 (London: a, b, c), europe-west10 (Berlin: a, b, c), and europe-west6 (Zurich: a, b, c). "
            "Key US regions include us-central1 (Iowa: a, b, c, f), us-east1 (South Carolina: b, c, d), "
            "us-east4 (Northern Virginia: a, b, c), and us-west1 (Oregon: a, b, c). "
            "Key APAC regions include asia-east1 (Taiwan: a, b, c), asia-northeast1 (Tokyo: a, b, c), "
            "and asia-southeast1 (Singapore: a, b, c). When a single zone is capacity-constrained, "
            "workloads should fail over first to sibling zones in the same region (<1ms latency) or "
            "to nearby regions within the same macro-geography (e.g., europe-west3 to europe-west4 at ~7.5ms)."
        ),
    },
    {
        "doc_id": "GCP-MACH-002",
        "title": "Google Cloud Compute Engine Machine Families Resource & Comparison Guide",
        "source_url": "https://docs.cloud.google.com/compute/docs/machine-resource",
        "section": "General-Purpose, Compute-Optimized, Memory-Optimized, and Accelerator-Optimized Families",
        "content": (
            "Compute Engine categorizes VM shapes into four primary groups: "
            "1. General-Purpose: E2 (cost-optimized everyday compute), N2 (Intel Xeon balanced 4GB/vCPU standard & 8GB/vCPU highmem), "
            "and N2D (AMD EPYC balanced compute offering ~13% lower cost than N2 with identical vCPU/RAM shapes). "
            "2. Compute-Optimized: C3 (4th Gen Intel Sapphire Rapids + Titanium DPU) and C4 (5th Gen Intel Xeon + Titanium) "
            "in standard (~3.75-4 GB/vCPU) and highcpu (2 GB/vCPU) shapes for compute-bound workloads. "
            "3. Memory-Optimized: M3 (m3-megamem-64 with 64 vCPUs and 1,952 GB RAM) for SAP HANA and in-memory databases. "
            "4. Accelerator-Optimized: G2 (NVIDIA L4 Tensor Core GPUs for AI inference and graphics) and "
            "A2 (NVIDIA A100 Tensor Core GPUs for ML training and HPC). When N2 supply is constrained, N2D or C3 "
            "in the same vCPU/memory shape provides a drop-in compatible alternative."
        ),
    },
    {
        "doc_id": "SPENDARK-BENCH-2026",
        "title": "SpendArk Cloud Cost Benchmark 2026 — Mid-Sized Company Compute Demand Profile",
        "source_url": "https://spendark.com/blog/cloud-cost-benchmark-2026/",
        "section": "Mid-Market Compute Spend, AI/GPU Growth, and FinOps Optimization",
        "content": (
            "According to the SpendArk 2026 Cloud Cost Benchmark, mid-sized companies spend between $2M and $5M annually "
            "on public cloud (~$285k/month median), with Compute accounting for 45% to 55% of the total bill and "
            "AI/GPU workloads representing 15% to 19% of total cloud spend. "
            "Average cloud waste sits at 27% to 33%, driven by over-provisioned Kubernetes clusters (<50% CPU/RAM utilization) "
            "and idle non-production environments running 168 hours/week. Best-in-class FinOps engineering teams target "
            "50% to 60% Committed Use Discount (CUD) coverage and actively substitute constrained Intel N2 instances "
            "with AMD N2D or E2 instances in low-cost regions (such as europe-west4 or us-central1) to save 13%–30%."
        ),
    },
]
