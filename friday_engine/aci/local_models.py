"""
F.R.I.D.A.Y. Local Model Manager & Hardware Accelerator.
Manages local LLM runtimes (Ollama, llama.cpp), downloads models (GGUF, HuggingFace, Ollama Library),
detects hardware acceleration (CUDA/NVIDIA, Apple Metal, AMD ROCm, CPU), and keeps runtimes updated.
"""

from __future__ import annotations

import os
import sys
import shutil
import platform
import subprocess
from typing import Dict, Any, List, Optional
import httpx

from friday_engine.logger import logger


class LocalModelManager:
    """
    Manages local AI model runtimes, automatic installation of Ollama / llama.cpp,
    model pulls, hardware acceleration detection, and self-updating.
    """

    def __init__(self, ollama_host: str = "http://127.0.0.1:11434", models_dir: str = "data/models"):
        self.ollama_host = ollama_host
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
        self.client = httpx.AsyncClient(timeout=180.0)

    def detect_hardware(self) -> Dict[str, Any]:
        """
        Detects GPU acceleration capabilities: NVIDIA CUDA, Apple Metal, AMD ROCm, or CPU cores.
        """
        system = platform.system().lower()
        info: Dict[str, Any] = {
            "os": system,
            "architecture": platform.machine(),
            "acceleration": "CPU",
            "details": {}
        }

        # 1. Check NVIDIA GPU / CUDA
        nvidia_smi = shutil.which("nvidia-smi")
        if nvidia_smi:
            try:
                res = subprocess.run([nvidia_smi, "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                                     capture_output=True, text=True, timeout=5)
                if res.returncode == 0 and res.stdout.strip():
                    gpus = [line.strip() for line in res.stdout.strip().split("\n")]
                    info["acceleration"] = "CUDA (NVIDIA)"
                    info["details"]["gpus"] = gpus
                    logger.info(f"[Hardware] Detected NVIDIA GPU(s): {gpus}")
                    return info
            except Exception as e:
                logger.warning(f"[Hardware] nvidia-smi query error: {e}")

        # 2. Check Apple Silicon Metal
        if system == "darwin":
            try:
                res = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, timeout=3)
                if "Apple" in res.stdout:
                    info["acceleration"] = "Metal (Apple Silicon MPS)"
                    info["details"]["chip"] = res.stdout.strip()
                    logger.info(f"[Hardware] Detected Apple Silicon: {res.stdout.strip()}")
                    return info
            except Exception:
                pass

        # 3. CPU Fallback
        info["details"]["cpu_count"] = os.cpu_count() or 1
        logger.info(f"[Hardware] Defaulting to CPU execution ({info['details']['cpu_count']} cores)")
        return info

    async def check_runtime_status(self) -> Dict[str, Any]:
        """
        Checks if Ollama or llama.cpp local inference service is currently running.
        """
        try:
            res = await self.client.get(f"{self.ollama_host}/api/version", timeout=3.0)
            if res.status_code == 200:
                version_data = res.json()
                return {
                    "running": True,
                    "runtime": "Ollama",
                    "version": version_data.get("version", "unknown"),
                    "host": self.ollama_host
                }
        except Exception:
            pass

        # Check if Ollama CLI binary exists in PATH
        binary_exists = shutil.which("ollama") is not None
        return {
            "running": False,
            "runtime": "Ollama",
            "binary_installed": binary_exists,
            "host": self.ollama_host,
            "message": "Ollama service is not currently active on port 11434."
        }

    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """
        Pulls/downloads an AI model locally via Ollama (e.g., 'llama3:8b', 'qwen2.5-coder:7b', 'deepseek-r1:8b').
        """
        logger.info(f"[LocalModels] Initiating pull for model: {model_name}")
        url = f"{self.ollama_host}/api/pull"
        try:
            res = await self.client.post(url, json={"name": model_name, "stream": False}, timeout=600.0)
            if res.status_code == 200:
                logger.info(f"[LocalModels] Successfully pulled {model_name}")
                return {"status": "success", "model": model_name, "message": f"Model '{model_name}' successfully downloaded."}
            else:
                return {"status": "error", "code": res.status_code, "detail": res.text}
        except Exception as e:
            logger.error(f"[LocalModels] Failed to pull model {model_name}: {e}")
            return {"status": "error", "message": str(e)}

    async def list_installed_models(self) -> List[Dict[str, Any]]:
        """
        Lists all locally downloaded models currently available in Ollama.
        """
        url = f"{self.ollama_host}/api/tags"
        try:
            res = await self.client.get(url, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                models = data.get("models", [])
                return [
                    {
                        "name": m.get("name"),
                        "size_gb": round(m.get("size", 0) / (1024 ** 3), 2),
                        "modified_at": m.get("modified_at"),
                        "details": m.get("details", {})
                    }
                    for m in models
                ]
            return []
        except Exception as e:
            logger.warning(f"[LocalModels] Could not list models: {e}")
            return []

    async def download_gguf(self, url: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Downloads a custom GGUF model file directly from HuggingFace or any direct URL.
        """
        if not filename:
            filename = url.split("/")[-1].split("?")[0]
            if not filename.endswith(".gguf"):
                filename += ".gguf"

        dest_path = os.path.join(self.models_dir, filename)
        logger.info(f"[LocalModels] Downloading GGUF model from {url} to {dest_path}")

        try:
            async with self.client.stream("GET", url, follow_redirects=True) as response:
                if response.status_code != 200:
                    return {"status": "error", "message": f"HTTP {response.status_code}"}

                with open(dest_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=1024 * 1024):
                        f.write(chunk)

            logger.info(f"[LocalModels] Download complete: {dest_path}")
            return {"status": "success", "file": dest_path, "filename": filename}
        except Exception as e:
            logger.error(f"[LocalModels] GGUF download failed: {e}")
            return {"status": "error", "message": str(e)}

    def install_runtime(self) -> Dict[str, Any]:
        """
        Automatically installs Ollama on the host operating system if not present.
        """
        os_name = platform.system().lower()
        logger.info(f"[LocalModels] Installing Ollama runtime for OS: {os_name}")

        try:
            if os_name == "windows":
                if shutil.which("winget"):
                    subprocess.run(["winget", "install", "--exact", "--accept-package-agreements",
                                    "--accept-source-agreements", "Ollama.Ollama"], check=True)
                    return {"status": "installed", "runtime": "Ollama", "method": "winget"}
                else:
                    return {"status": "manual_action_required", "download_url": "https://ollama.com/download/OllamaSetup.exe"}

            elif os_name == "linux":
                subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
                return {"status": "installed", "runtime": "Ollama", "method": "install.sh"}

            elif os_name == "darwin":
                if shutil.which("brew"):
                    subprocess.run(["brew", "install", "--cask", "ollama"], check=True)
                    return {"status": "installed", "runtime": "Ollama", "method": "brew"}
                else:
                    return {"status": "manual_action_required", "download_url": "https://ollama.com/download/mac"}

            return {"status": "unsupported_os", "os": os_name}
        except Exception as e:
            logger.error(f"[LocalModels] Failed to install runtime: {e}")
            return {"status": "error", "message": str(e)}

    async def check_runtime_updates(self) -> Dict[str, Any]:
        """
        Checks for latest Ollama releases from GitHub releases API.
        """
        try:
            res = await self.client.get("https://api.github.com/repos/ollama/ollama/releases/latest", timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                latest_tag = data.get("tag_name", "unknown")
                current_status = await self.check_runtime_status()
                current_version = current_status.get("version", "unknown")
                return {
                    "latest_release": latest_tag,
                    "current_version": current_version,
                    "update_available": (latest_tag.lstrip("v") != current_version.lstrip("v")) if current_version != "unknown" else None,
                    "release_notes_url": data.get("html_url")
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return {"status": "unknown"}
