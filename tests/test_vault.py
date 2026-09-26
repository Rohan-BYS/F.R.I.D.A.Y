"""
Unit tests for Identity Vault encryption and retrieval.
"""

import tempfile
from pathlib import Path
from friday_engine.config import SecurityConfig
from friday_engine.security.vault import IdentityVault


def test_vault_store_and_retrieve():
    with tempfile.TemporaryDirectory() as temp_dir:
        vault_file = Path(temp_dir) / "test_vault.enc"
        key_file = Path(temp_dir) / "test_vault.key"

        cfg = SecurityConfig(
            vault_file=str(vault_file),
            key_file=str(key_file),
            auto_generate_key=True,
        )

        vault = IdentityVault(cfg)

        # Store credentials
        vault.store_credentials(
            service="github",
            username="rohan_forge",
            password="secret_token_12345",
            metadata={"scope": "repo,workflow"},
        )

        # Check key and vault file creation
        assert key_file.exists()
        assert vault_file.exists()

        # Retrieve credentials
        creds = vault.retrieve_credentials("github")
        assert creds is not None
        assert creds["username"] == "rohan_forge"
        assert creds["password"] == "secret_token_12345"
        assert creds["metadata"]["scope"] == "repo,workflow"

        # List services
        services = vault.list_services()
        assert "github" in services

        # Delete
        assert vault.delete_credentials("github") is True
        assert vault.retrieve_credentials("github") is None
