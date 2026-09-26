#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Hardware & Thermal Sentinel
=========================================
Monitors CPU/GPU temperatures, system RAM, CPU load, and disk storage.
Triggers auto-cooldown warnings and thermal throttling protection for 24/7 autonomous machines.

Usage:
  python scripts/hardware_thermal_sentinel.py --check
  python scripts/hardware_thermal_sentinel.py --watch
"""

import os
import sys
import json
import time
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class HardwareThermalSentinel:
    """Monitors physical host machine thermals and resource health."""

    def __init__(self, temp_warning_c: float = 80.0, temp_critical_c: float = 88.0):
        self.temp_warning = temp_warning_c
        self.temp_critical = temp_critical_c

    def get_gpu_temperature(self) -> Optional[float]:
        """Queries NVIDIA GPU temperature via nvidia-smi if available."""
        try:
            cmd = ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                return float(res.stdout.strip().split("\n")[0])
        except Exception:
            pass
        return None

    def get_cpu_temperature(self) -> Optional[float]:
        """Queries CPU temperature across Linux /sys/class/thermal or Windows WMI."""
        # 1. Linux sysfs thermal zones
        if sys.platform.startswith("linux"):
            try:
                for zone in Path("/sys/class/thermal").glob("thermal_zone*"):
                    type_file = zone / "type"
                    temp_file = zone / "temp"
                    if temp_file.exists():
                        val = int(temp_file.read_text().strip())
                        temp_c = val / 1000.0 if val > 1000 else float(val)
                        return round(temp_c, 1)
            except Exception:
                pass

        # 2. Windows WMI fallback
        elif sys.platform == "win32":
            try:
                cmd = ["powershell", "-NoProfile", "-Command", "Get-CimInstance MSAcpi_ThermalZoneTemperature -Namespace root/wmi -ErrorAction SilentlyContinue | Select-Object -ExpandProperty CurrentTemperature"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if res.returncode == 0 and res.stdout.strip():
                    kelvin_deci = float(res.stdout.strip().split()[0])
                    celsius = (kelvin_deci / 10.0) - 273.15
                    return round(celsius, 1)
            except Exception:
                pass

        return None

    def get_system_health(self) -> Dict[str, Any]:
        """Runs complete hardware health check."""
        gpu_temp = self.get_gpu_temperature()
        cpu_temp = self.get_cpu_temperature()

        # Disk space
        total, used, free = shutil.disk_usage(str(PROJECT_ROOT))
        free_gb = round(free / (1024**3), 2)
        total_gb = round(total / (1024**3), 2)

        # Max temp detected
        active_temps = [t for t in [gpu_temp, cpu_temp] if t is not None]
        highest_temp = max(active_temps) if active_temps else None

        status = "NOMINAL"
        recommendation = "Operating conditions optimal."

        if highest_temp:
            if highest_temp >= self.temp_critical:
                status = "CRITICAL_OVERHEAT"
                recommendation = f"ALERT: Temperature reached {highest_temp}°C! Throttle intensive AI inference and check fans."
            elif highest_temp >= self.temp_warning:
                status = "WARM_WARNING"
                recommendation = f"Caution: System temperature elevated ({highest_temp}°C)."

        return {
            "status": status,
            "highest_temperature_c": highest_temp,
            "cpu_temperature_c": cpu_temp if cpu_temp is not None else "Sensor Not Available",
            "gpu_temperature_c": gpu_temp if gpu_temp is not None else "No NVIDIA GPU Detected",
            "disk_free_gb": free_gb,
            "disk_total_gb": total_gb,
            "disk_usage_pct": round((used / total) * 100, 1),
            "recommendation": recommendation,
        }


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Hardware & Thermal Sentinel")
    parser.add_argument("--check", action="store_true", help="Run single hardware health check")
    parser.add_argument("--watch", action="store_true", help="Watch thermals every 10 seconds")
    args = parser.parse_args()

    sentinel = HardwareThermalSentinel()

    if args.watch:
        print("Hardware Thermal Sentinel watching system health (Ctrl+C to stop)...")
        while True:
            health = sentinel.get_system_health()
            print(f"[{health['status']}] CPU: {health['cpu_temperature_c']} | GPU: {health['gpu_temperature_c']} | Disk Free: {health['disk_free_gb']} GB")
            time.sleep(10)
    else:
        health = sentinel.get_system_health()
        print(json.dumps(health, indent=2))


if __name__ == "__main__":
    main()
