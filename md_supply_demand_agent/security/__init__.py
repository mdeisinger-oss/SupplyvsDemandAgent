"""Security & Secret Management Package for MD-Supply-vs-Demand-Agent."""

from .secret_manager import SecretManagerClient, global_secret_manager

__all__ = ["SecretManagerClient", "global_secret_manager"]
