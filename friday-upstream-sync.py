#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Upstream Intelligence Scanner & Auto-Merger
=========================================================
This script monitors upstream AI agent repositories (Hermes, OpenHands, CrewAI, etc.)
for new releases, features, tools, and skills — then automatically:
  1. Detects new releases and changelogs
  2. Downloads and analyzes new features
  3. Integrates compatible features into F.R.I.D.A.Y.'s codebase
  4. Logs all integrations to the Evolution Codex

Usage:
  python friday-upstream-sync.py                    # Check all watched repos
  python friday-upstream-sync.py --auto-merge       # Check + auto-integrate new features
  python friday-upstream-sync.py --watch hermes     # Watch only Hermes
  python friday-upstream-sync.py --daemon           # Run as background cron job

Designed to be called by the ProactiveScheduler or cron.
"""

import os
import sys
import json
import shutil
import subprocess
import datetime
import hashlib
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM_STATE_FILE = BASE_DIR / "data" / "upstream_state.json"
UPSTREAM_CACHE_DIR = BASE_DIR / "data" / "upstream_cache"

# ── Watched Repositories ────────────────────────────────────────────────
WATCHED_REPOS = {
    "hermes": {
        "name": "Hermes Agent",
        "url": "https://github.com/NousResearch/hermes-agent",
        "clone_url": "https://github.com/NousResearch/hermes-agent.git",
        "priority": "critical",  # critical = auto-merge, normal = suggest, low = log only
        "watch_paths": [
            "tools/",           # New native tools
            "skills/",          # New built-in skills
            "optional-skills/", # Community skills
            "optional-mcps/",   # New MCP integrations
            "agent/",           # Core agent improvements
            "SOUL.md",          # Persona updates
            "pyproject.toml",   # Dependency updates
        ],
        "integration_map": {
            "tools/": "friday_engine/aci/hermes_tools/",
            "skills/": "data/skills/hermes_upstream/",
            "optional-skills/": "data/skills/hermes_community/",
            "optional-mcps/": "data/mcp_servers_upstream/",
        }
    },
    "hermes-evolution": {
        "name": "Hermes Self-Evolution",
        "url": "https://github.com/NousResearch/hermes-agent-self-evolution",
        "clone_url": "https://github.com/NousResearch/hermes-agent-self-evolution.git",
        "priority": "critical",
        "watch_paths": ["evolution/", "datasets/"],
        "integration_map": {
            "evolution/": "friday_engine/evolution/hermes_upstream/",
        }
    },
    "openhands": {
        "name": "OpenHands (All-Hands AI)",
        "url": "https://github.com/All-Hands-AI/OpenHands",
        "clone_url": "https://github.com/All-Hands-AI/OpenHands.git",
        "priority": "normal",
        "watch_paths": ["openhands/agenthub/", "openhands/runtime/"],
        "integration_map": {}
    },
    "browser-use": {
        "name": "Browser Use",
        "url": "https://github.com/browser-use/browser-use",
        "clone_url": "https://github.com/browser-use/browser-use.git",
        "priority": "normal",
        "watch_paths": ["browser_use/"],
        "integration_map": {}
    },
    "crewai": {
        "name": "CrewAI",
        "url": "https://github.com/crewAIInc/crewAI",
        "clone_url": "https://github.com/crewAIInc/crewAI.git",
        "priority": "low",
        "watch_paths": ["src/crewai/tools/", "src/crewai/agents/"],
        "integration_map": {}
    },
    "swe-agent": {
        "name": "SWE-Agent",
        "url": "https://github.com/princeton-nlp/SWE-agent",
        "clone_url": "https://github.com/princeton-nlp/SWE-agent.git",
        "priority": "low",
        "watch_paths": ["sweagent/tools/", "config/"],
        "integration_map": {}
    },
}


class UpstreamState:
    """Tracks the last known state of each watched repository."""

    def __init__(self, state_file: Path = UPSTREAM_STATE_FILE):
        self.state_file = state_file
        self.state: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.state = {}

    def _save(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def get_last_commit(self, repo_key: str) -> Optional[str]:
        return self.state.get(repo_key, {}).get("last_commit")

    def get_last_version(self, repo_key: str) -> Optional[str]:
        return self.state.get(repo_key, {}).get("last_version")

    def update(self, repo_key: str, commit: str, version: str = "", changes: List[str] = None):
        self.state[repo_key] = {
            "last_commit": commit,
            "last_version": version,
            "last_checked": datetime.datetime.now().isoformat(),
            "changes_integrated": changes or [],
        }
        self._save()


class UpstreamScanner:
    """
    Scans upstream repos for new commits, releases, features, and skills.
    """

    def __init__(self):
        self.state = UpstreamState()
        UPSTREAM_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _run_git(self, args: List[str], cwd: str = None) -> Tuple[int, str]:
        """Run a git command and return (exit_code, stdout)."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return 1, str(e)

    def _get_latest_release(self, repo_key: str) -> Optional[Dict]:
        """Fetch latest release info via GitHub API."""
        repo = WATCHED_REPOS[repo_key]
        # Extract owner/repo from URL
        parts = repo["url"].rstrip("/").split("/")
        owner_repo = f"{parts[-2]}/{parts[-1]}"

        try:
            import urllib.request
            url = f"https://api.github.com/repos/{owner_repo}/releases/latest"
            req = urllib.request.Request(url, headers={
                "User-Agent": "FRIDAY-UpstreamSync/1.0",
                "Accept": "application/vnd.github.v3+json",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except Exception:
            return None

    def _get_latest_commits(self, repo_key: str, since_commit: str = None) -> List[Dict]:
        """Fetch recent commits via GitHub API."""
        repo = WATCHED_REPOS[repo_key]
        parts = repo["url"].rstrip("/").split("/")
        owner_repo = f"{parts[-2]}/{parts[-1]}"

        try:
            import urllib.request
            url = f"https://api.github.com/repos/{owner_repo}/commits?per_page=20"
            req = urllib.request.Request(url, headers={
                "User-Agent": "FRIDAY-UpstreamSync/1.0",
                "Accept": "application/vnd.github.v3+json",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                commits = json.loads(resp.read())

            if since_commit:
                new_commits = []
                for c in commits:
                    if c["sha"] == since_commit:
                        break
                    new_commits.append({
                        "sha": c["sha"][:8],
                        "message": c["commit"]["message"].split("\n")[0],
                        "date": c["commit"]["author"]["date"],
                    })
                return new_commits
            else:
                return [{"sha": c["sha"][:8], "message": c["commit"]["message"].split("\n")[0]} for c in commits[:5]]
        except Exception:
            return []

    def _clone_or_update_cache(self, repo_key: str) -> Optional[Path]:
        """Clone repo to cache or update existing clone."""
        repo = WATCHED_REPOS[repo_key]
        cache_dir = UPSTREAM_CACHE_DIR / repo_key

        if cache_dir.exists() and (cache_dir / ".git").exists():
            code, _ = self._run_git(["pull", "--ff-only"], cwd=str(cache_dir))
            if code != 0:
                # Force re-clone on pull failure
                shutil.rmtree(cache_dir, ignore_errors=True)
                code, _ = self._run_git(["clone", "--depth=1", repo["clone_url"], str(cache_dir)])
        else:
            cache_dir.parent.mkdir(parents=True, exist_ok=True)
            code, _ = self._run_git(["clone", "--depth=1", repo["clone_url"], str(cache_dir)])

        return cache_dir if code == 0 else None

    def scan_repo(self, repo_key: str) -> Dict:
        """Scan a single repo for updates."""
        repo = WATCHED_REPOS[repo_key]
        last_commit = self.state.get_last_commit(repo_key)
        last_version = self.state.get_last_version(repo_key)

        report = {
            "repo": repo_key,
            "name": repo["name"],
            "priority": repo["priority"],
            "has_updates": False,
            "new_version": None,
            "new_commits": [],
            "new_files": [],
        }

        # Check latest release
        release = self._get_latest_release(repo_key)
        if release:
            tag = release.get("tag_name", "")
            if tag and tag != last_version:
                report["has_updates"] = True
                report["new_version"] = tag
                report["release_url"] = release.get("html_url", "")
                report["release_notes"] = release.get("body", "")[:500]

        # Check new commits
        new_commits = self._get_latest_commits(repo_key, since_commit=last_commit)
        if new_commits:
            report["has_updates"] = True
            report["new_commits"] = new_commits

        return report

    def scan_all(self) -> List[Dict]:
        """Scan all watched repos."""
        results = []
        for repo_key in WATCHED_REPOS:
            print(f"  Scanning {WATCHED_REPOS[repo_key]['name']}...")
            report = self.scan_repo(repo_key)
            results.append(report)
            if report["has_updates"]:
                status = f"🆕 {report.get('new_version', '')} + {len(report['new_commits'])} new commits"
            else:
                status = "✓ Up to date"
            print(f"    {status}")
        return results

    def auto_merge(self, repo_key: str) -> Dict:
        """
        Auto-merge new features from an upstream repo into F.R.I.D.A.Y.
        Only works for repos with 'critical' priority and defined integration_map.
        """
        repo = WATCHED_REPOS[repo_key]
        if repo["priority"] != "critical":
            return {"status": "skipped", "reason": f"Priority is '{repo['priority']}', not 'critical'"}

        if not repo.get("integration_map"):
            return {"status": "skipped", "reason": "No integration_map defined"}

        # Clone/update cache
        cache_dir = self._clone_or_update_cache(repo_key)
        if not cache_dir:
            return {"status": "error", "reason": "Failed to clone/update repo cache"}

        merged_files = []

        for source_path, target_path in repo["integration_map"].items():
            src = cache_dir / source_path
            dst = BASE_DIR / target_path

            if not src.exists():
                continue

            dst.mkdir(parents=True, exist_ok=True)

            if src.is_dir():
                for item in src.rglob("*"):
                    if item.is_file() and not item.name.startswith("."):
                        rel = item.relative_to(src)
                        target_file = dst / rel
                        target_file.parent.mkdir(parents=True, exist_ok=True)

                        # Only copy if file is new or changed
                        if not target_file.exists():
                            shutil.copy2(item, target_file)
                            merged_files.append(str(rel))
                        else:
                            # Check if content changed
                            src_hash = hashlib.md5(item.read_bytes()).hexdigest()
                            dst_hash = hashlib.md5(target_file.read_bytes()).hexdigest()
                            if src_hash != dst_hash:
                                shutil.copy2(item, target_file)
                                merged_files.append(f"{rel} (updated)")

        # Update state
        code, latest_sha = self._run_git(["rev-parse", "HEAD"], cwd=str(cache_dir))
        release = self._get_latest_release(repo_key)
        version = release.get("tag_name", "") if release else ""

        self.state.update(
            repo_key,
            commit=latest_sha[:8] if code == 0 else "",
            version=version,
            changes=merged_files
        )

        # Log to Evolution Codex
        if merged_files:
            try:
                sys.path.insert(0, str(BASE_DIR))
                # Import without the hyphen issue
                import importlib.util
                spec = importlib.util.spec_from_file_location("friday_evolve", BASE_DIR / "friday-evolve.py")
                evolve_mod = importlib.util.load_module("friday_evolve", spec.loader, "friday_evolve", (".py", "r", 1), spec.submodule_search_locations)
                # Simpler approach - just append to codex
                codex_path = BASE_DIR / "EVOLUTION_CODEX.md"
                with open(codex_path, "a", encoding="utf-8") as f:
                    f.write(f"\n### Upstream Sync: {repo['name']}\n")
                    f.write(f"* **Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                    f.write(f"* **Source:** {repo['url']}\n")
                    f.write(f"* **Version:** {version}\n")
                    f.write(f"* **Files Merged:** {len(merged_files)}\n")
                    for mf in merged_files[:20]:
                        f.write(f"  - `{mf}`\n")
                    f.write("\n")
            except Exception:
                pass  # Non-critical

        return {
            "status": "success",
            "repo": repo_key,
            "files_merged": len(merged_files),
            "merged": merged_files,
            "version": version,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Upstream Intelligence Scanner")
    parser.add_argument("--auto-merge", action="store_true", help="Auto-integrate new features from critical repos")
    parser.add_argument("--watch", type=str, default=None, help="Watch a specific repo (e.g., hermes)")
    parser.add_argument("--daemon", action="store_true", help="Run as background daemon (checks every 6 hours)")
    args = parser.parse_args()

    scanner = UpstreamScanner()

    print("\n" + "="*60)
    print("  F.R.I.D.A.Y. Upstream Intelligence Scanner")
    print("  Monitoring the AI landscape for new capabilities...")
    print("="*60 + "\n")

    if args.daemon:
        import time
        while True:
            print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] Running scan...")
            results = scanner.scan_all()
            for r in results:
                if r["has_updates"] and WATCHED_REPOS[r["repo"]]["priority"] == "critical":
                    print(f"\n  🔄 Auto-merging {r['name']}...")
                    merge_result = scanner.auto_merge(r["repo"])
                    print(f"    → {merge_result['status']}: {merge_result.get('files_merged', 0)} files")
            print(f"\n  Next scan in 6 hours...")
            time.sleep(6 * 3600)

    elif args.watch:
        if args.watch not in WATCHED_REPOS:
            print(f"Unknown repo: {args.watch}. Available: {', '.join(WATCHED_REPOS.keys())}")
            return
        report = scanner.scan_repo(args.watch)
        print(json.dumps(report, indent=2))
        if args.auto_merge and report["has_updates"]:
            result = scanner.auto_merge(args.watch)
            print(json.dumps(result, indent=2))

    else:
        results = scanner.scan_all()
        print(f"\n{'─'*60}")

        updates_found = [r for r in results if r["has_updates"]]
        if updates_found:
            print(f"\n  📦 {len(updates_found)} repo(s) have updates:\n")
            for r in updates_found:
                print(f"  • {r['name']}: {r.get('new_version', 'new commits')}")
                for c in r["new_commits"][:3]:
                    print(f"    └─ [{c['sha']}] {c['message'][:60]}")

            if args.auto_merge:
                print(f"\n  🔄 Auto-merging critical repos...\n")
                for r in updates_found:
                    if WATCHED_REPOS[r["repo"]]["priority"] == "critical":
                        result = scanner.auto_merge(r["repo"])
                        print(f"  ✓ {r['name']}: {result.get('files_merged', 0)} files merged")
        else:
            print("\n  ✅ All watched repositories are up to date.")

        print(f"\n{'─'*60}\n")


if __name__ == "__main__":
    main()
