"""
F.R.I.D.A.Y. Main Entrypoint & CLI.
Runs the primary asyncio event loop, diagnostics, and interactive interface.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
import sys
from friday_engine.core.engine import FridayEngine
from friday_engine.logger import ANSIColor, logger

# Ensure Windows console supports UTF-8
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BANNER = rf"""{ANSIColor.CYAN}
  ==============================================================
  |   F . R . I . D . A . Y .                                  |
  |   Fully Recursive Intelligent Digital Autonomous Yield     |
  |   Parent Forge Architecture | Creator: Rohan               |
  |   Status: INITIALIZED & ONLINE                             |
  ==============================================================
{ANSIColor.RESET}"""


async def run_diagnostics(engine: FridayEngine) -> None:
    """Run boot health checks and print formatted diagnostic status."""
    report = await engine.boot()
    print(BANNER)
    print(f"{ANSIColor.GREEN}=== SYSTEM HEALTH & DIAGNOSTIC MATRIX ==={ANSIColor.RESET}")
    print(json.dumps(report, indent=2))
    print(f"{ANSIColor.GREEN}=========================================={ANSIColor.RESET}\n")


async def run_interactive_cli(engine: FridayEngine) -> None:
    """Run interactive terminal session between Rohan and F.R.I.D.A.Y."""
    await engine.boot()
    print(BANNER)
    print(f"{ANSIColor.GREEN}F.R.I.D.A.Y. is online and awaiting directives from Rohan.{ANSIColor.RESET}")
    print(f"Type 'exit', 'quit', or 'backup' to interact.\n")

    loop = asyncio.get_running_loop()

    while True:
        try:
            user_input = await loop.run_in_executor(None, input, f"{ANSIColor.CYAN}Rohan > {ANSIColor.RESET}")
            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print(f"{ANSIColor.YELLOW}F.R.I.D.A.Y.: Standing by. Preserving state...{ANSIColor.RESET}")
                await engine.shutdown()
                break

            if user_input.lower() == "backup":
                print(f"{ANSIColor.CYAN}Triggering Midnight Protocol manually...{ANSIColor.RESET}")
                res = engine.trigger_midnight_backup(custom_message="Manual trigger from CLI")
                print(f"Backup Result: {res}")
                continue

            response = await engine.chat(user_input)
            print(f"\n{ANSIColor.GREEN}F.R.I.D.A.Y. >{ANSIColor.RESET} {response}\n")

        except (KeyboardInterrupt, EOFError):
            print(f"\n{ANSIColor.YELLOW}Termination signal detected. Shutting down...{ANSIColor.RESET}")
            await engine.shutdown()
            break
        except Exception as exc:
            logger.error(f"Error in main loop: {exc}", exc_info=True)


async def main_async() -> None:
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Autonomous Parent Forge Engine")
    parser.add_argument("--status", action="store_true", help="Run subsystem diagnostics and exit")
    parser.add_argument("--backup", action="store_true", help="Trigger Midnight Protocol backup and exit")
    parser.add_argument("--cli", action="store_true", help="Run interactive CLI chat mode (default)")
    args = parser.parse_args()

    engine = FridayEngine()

    if args.status:
        await run_diagnostics(engine)
    elif args.backup:
        await engine.boot()
        res = engine.trigger_midnight_backup(custom_message="Triggered via CLI --backup flag")
        print(json.dumps(res, indent=2))
    else:
        await run_interactive_cli(engine)


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nShutdown complete.")


if __name__ == "__main__":
    main()
