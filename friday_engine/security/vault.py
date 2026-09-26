"""
F.R.I.D.A.Y. Identity Vault.
Secure, encrypted credential storage using Fernet (AES-128-CBC + HMAC-SHA256).
Enables Friday to securely manage user and service credentials across sessions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from cryptography.fernet import Fernet, InvalidToken

from friday_engine.config import SecurityConfig
from friday_engine.logger import logger


class VaultError(Exception):
    """Base exception for Identity Vault errors."""
    pass


class VaultAuthenticationError(VaultError):
    """Raised when decryption fails due to invalid key or tampered data."""
    pass


class IdentityVault:
    """
    Encrypted credential storage vault.
    """

    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        self.vault_file = Path(self.config.vault_file)
        self.key_file = Path(self.config.key_file)
        self._fernet: Optional[Fernet] = None
        self._ensure_key()

    def _ensure_key(self) -> None:
        """Load or create the Fernet encryption key."""
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        self.vault_file.parent.mkdir(parents=True, exist_ok=True)

        if self.key_file.is_file():
            key = self.key_file.read_bytes().strip()
            self._fernet = Fernet(key)
        elif self.config.auto_generate_key:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            self._fernet = Fernet(key)
            logger.info(f"Generated new secure vault encryption key at {self.key_file}")
        else:
            raise VaultError(f"Vault key file missing at {self.key_file} and auto_generate_key is disabled.")

    def _read_vault_data(self) -> Dict[str, Any]:
        """Read and decrypt the vault database file."""
        if not self.vault_file.is_file():
            return {}

        encrypted_bytes = self.vault_file.read_bytes()
        if not encrypted_bytes:
            return {}

        try:
            assert self._fernet is not None
            decrypted_json = self._fernet.decrypt(encrypted_bytes).decode("utf-8")
            return json.loads(decrypted_json)
        except InvalidToken as exc:
            raise VaultAuthenticationError("Vault decryption failed: Key is invalid or file is corrupted.") from exc
        except Exception as exc:
            raise VaultError(f"Failed to read vault: {exc}") from exc

    def _write_vault_data(self, data: Dict[str, Any]) -> None:
        """Encrypt and atomically save vault data."""
        assert self._fernet is not None
        json_bytes = json.dumps(data, indent=2).encode("utf-8")
        encrypted_bytes = self._fernet.encrypt(json_bytes)

        # Atomic write via temp file
        temp_file = self.vault_file.with_suffix(".tmp")
        temp_file.write_bytes(encrypted_bytes)
        temp_file.replace(self.vault_file)

    def store_credentials(
        self,
        service: str,
        username: str,
        password: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store credentials for a given service."""
        data = self._read_vault_data()
        data[service] = {
            "username": username,
            "password": password,
            "metadata": metadata or {},
        }
        self._write_vault_data(data)
        logger.info(f"Securely stored credentials for service '{service}'")

    def retrieve_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored credentials for a given service."""
        data = self._read_vault_data()
        return data.get(service)

    def list_services(self) -> List[str]:
        """List all services stored in the vault without revealing passwords."""
        data = self._read_vault_data()
        return list(data.keys())

    def delete_credentials(self, service: str) -> bool:
        """Remove a service from the vault."""
        data = self._read_vault_data()
        if service in data:
            del data[service]
            self._write_vault_data(data)
            logger.info(f"Removed credentials for service '{service}'")
            return True
        return False
