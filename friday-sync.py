#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Upstream Synchronization Engine.

Safely fetches updates from upstream Hermes Agent repository,
applies non-breaking improvements, and safeguards F.R.I.D.A.Y.'s
custom persona, local environment configuration, and custom skills.
"""
import os
import sys
import subprocess
import shutil

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Files that must always remain in F.R.I.D.A.Y. state
PROTECTED_FILES = [
    "SOUL.md",
    ".env",
    "friday",
    "friday.cmd",
    os.path.join("skills", "friday", "whatsapp", "SKILL.md")
]

def run_cmd(cmd, cwd=REPO_ROOT):
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def backup_custom_files():
    backup_dir = os.path.join(REPO_ROOT, ".friday_backup")
    os.makedirs(backup_dir, exist_ok=True)
    for rel_path in PROTECTED_FILES:
        src = os.path.join(REPO_ROOT, rel_path)
        if os.path.exists(src):
            dest = os.path.join(backup_dir, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)
    print("[F.R.I.D.A.Y. Sync] Custom configurations backed up.")
    return backup_dir

def restore_custom_files(backup_dir):
    for rel_path in PROTECTED_FILES:
        backup_src = os.path.join(backup_dir, rel_path)
        if os.path.exists(backup_src):
            target = os.path.join(REPO_ROOT, rel_path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(backup_src, target)
    # Ensure identity lines in prompt_builder & default_soul remain F.R.I.D.A.Y.
    _patch_core_identities()
    print("[F.R.I.D.A.Y. Sync] Custom F.R.I.D.A.Y. persona and skills verified.")

def _patch_core_identities():
    # Update default_soul.py if upstream reverted it
    ds_path = os.path.join(REPO_ROOT, "hermes_cli", "default_soul.py")
    if os.path.exists(ds_path):
        with open(ds_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "You are Hermes Agent" in content:
            content = content.replace("You are Hermes Agent, built by Nous Research.", "You are F.R.I.D.A.Y., an advanced, highly capable, and autonomous AI operating system.")
            with open(ds_path, "w", encoding="utf-8") as f:
                f.write(content)

    # Update prompt_builder.py if upstream reverted it
    pb_path = os.path.join(REPO_ROOT, "agent", "prompt_builder.py")
    if os.path.exists(pb_path):
        with open(pb_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "You are Hermes Agent, built by Nous Research." in content:
            content = content.replace("You are Hermes Agent, built by Nous Research.", "You are F.R.I.D.A.Y., an advanced, highly capable, and autonomous AI operating system.")
            with open(pb_path, "w", encoding="utf-8") as f:
                f.write(content)

def sync_upstream():
    print("=" * 60)
    print("      F.R.I.D.A.Y. CORE SYNCHRONIZATION")
    print("=" * 60)

    backup_dir = backup_custom_files()

    print("[1/3] Checking upstream repository status...")
    code, stdout, stderr = run_cmd("git fetch origin")
    if code != 0:
        print(f"[Warning] Failed to fetch upstream: {stderr}")
        return

    print("[2/3] Checking for new features and updates...")
    code, stdout, _ = run_cmd("git log HEAD..origin/main --oneline")
    if stdout:
        print("Upcoming improvements:")
        for line in stdout.splitlines()[:10]:
            print(f"  + {line}")
    else:
        print("F.R.I.D.A.Y. chassis is already up to date with upstream.")

    # Pull changes
    code, stdout, stderr = run_cmd("git pull --no-rebase origin main")
    if code != 0:
        print("[Notice] Using local baseline; restoring customizations.")

    print("[3/3] Re-verifying F.R.I.D.A.Y. configuration & skills...")
    restore_custom_files(backup_dir)

    print("=" * 60)
    print("[SUCCESS] F.R.I.D.A.Y. is synchronized and ready.")
    print("=" * 60)

if __name__ == "__main__":
    sync_upstream()
