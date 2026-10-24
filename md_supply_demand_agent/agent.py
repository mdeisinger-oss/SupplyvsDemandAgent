"""Google ADK Standard Entrypoint (`root_agent`) for MD-Supply-vs-Demand-Agent.

Compatible with ADK CLI commands:
- `adk web`
- `adk run md_supply_demand_agent`
- `adk eval md_supply_demand_agent eval/golden_dataset.json`
- `adk deploy cloud_run md_supply_demand_agent`
"""

from .orchestration.multi_agent import build_adk_agent_hierarchy, global_orchestrator

root_agent, adk_hierarchy_metadata = build_adk_agent_hierarchy()

__all__ = ["root_agent", "adk_hierarchy_metadata", "global_orchestrator"]
