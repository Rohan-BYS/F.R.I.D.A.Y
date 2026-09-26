"""
Top-level re-export for Identity Vault to satisfy friday_engine/identity_vault.py interface.
"""

from friday_engine.security.vault import (
    IdentityVault,
    VaultAuthenticationError,
    VaultError,
)

__all__ = ["IdentityVault", "VaultError", "VaultAuthenticationError"]
