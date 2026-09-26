#!/usr/bin/env python3
"""
F.R.I.D.A.Y. CLI Entry Point.
Usage:
    friday              - Start the engine (runs setup wizard on first launch)
    friday setup        - Re-run the interactive setup wizard
    friday update       - Pull latest code from GitHub and update dependencies
    friday hud          - Launch the desktop HUD visualizer
    friday evolve       - Generate a flawless Child Version
    friday sync         - Sync upstream repos (Hermes, etc.) for new features
    friday scan-market  - Scan the AI landscape for new frameworks
    friday help         - Show all available commands
"""
import os
import sys
import subprocess
import asyncio

# Ensure the project root is on PATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

CONFIG_PATH = os.path.join(project_root, "data", "friday_config.json")


def detect_display():
    """Auto-detect and configure display for GUI capabilities."""
    display = os.environ.get("DISPLAY")
    if display:
        xauth = os.path.expanduser("~/.Xauthority")
        if os.path.exists(xauth):
            os.environ.setdefault("XAUTHORITY", xauth)
        return True
    wayland = os.environ.get("WAYLAND_DISPLAY")
    if wayland:
        return True
    return False


def self_update():
    """Pull latest code from GitHub and update dependencies."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    console = Console()

    console.print(Panel("[bold cyan]F.R.I.D.A.Y. Self-Update Protocol[/bold cyan]", border_style="cyan"))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        t = prog.add_task("[cyan]Pulling latest code from GitHub...", total=3)
        subprocess.run(["git", "pull"], cwd=project_root, check=True, capture_output=True)
        prog.update(t, advance=1, description="[green]Code updated.")

        prog.update(t, description="[cyan]Updating Python dependencies...")
        venv_pip = os.path.join(project_root, ".venv", "bin", "pip")
        pip_cmd = venv_pip if os.path.exists(venv_pip) else sys.executable
        if pip_cmd == sys.executable:
            subprocess.run([pip_cmd, "-m", "pip", "install", "-r", "requirements.txt"], cwd=project_root, capture_output=True)
        else:
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], cwd=project_root, capture_output=True)
        prog.update(t, advance=1, description="[green]Dependencies updated.")

        prog.update(t, description="[cyan]Refreshing browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], cwd=project_root, capture_output=True)
        prog.update(t, advance=1, description="[green]All systems updated.")

    console.print("\n[bold green]Update complete.[/bold green] Restart with: [bold cyan]friday[/bold cyan]\n")


def show_help():
    """Display help menu."""
    from rich.console import Console
    from rich.table import Table
    from rich import box
    console = Console()

    table = Table(title="F.R.I.D.A.Y. Commands", box=box.ROUNDED, border_style="cyan")
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="white")
    table.add_row("friday", "Start the interactive text chat")
    table.add_row("friday voice", "Start the hands-free voice listener")
    table.add_row("friday setup", "Re-run the interactive setup wizard")
    table.add_row("friday update", "Self-update from GitHub + refresh dependencies")
    table.add_row("friday hud", "Launch the desktop orb visualizer")
    table.add_row("friday market", "5m candle + news surveillance & predictive analysis")
    table.add_row("friday clean-pdfs", "Delete raw PDFs to free disk space while keeping structured data")
    table.add_row("friday evolve", "Generate a flawless Child Version (Project Phoenix)")
    table.add_row("friday sync", "Auto-merge new features from upstream AI agents")
    table.add_row("friday scan", "Scan the AI landscape for new frameworks to learn")
    table.add_row("friday help", "Show this help message")
    console.print(table)


def main():
    # Handle CLI subcommands
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "update":
            self_update()
            return
        elif cmd == "hud":
            from friday_engine.gui.hud import launch_hud
            launch_hud()
            return
        elif cmd == "voice":
            from friday_voice_listener import main as friday_voice_main
            import asyncio
            asyncio.run(friday_voice_main())
            return
        elif cmd == "setup":
            from friday_setup import run_setup
            run_setup()
            return
        elif cmd == "evolve":
            subprocess.run([sys.executable, os.path.join(project_root, "friday-evolve.py")] + sys.argv[2:])
            return
        elif cmd == "sync":
            subprocess.run([sys.executable, os.path.join(project_root, "friday-upstream-sync.py"), "--auto-merge"] + sys.argv[2:])
            return
        elif cmd == "scan-market" or cmd == "scan":
            subprocess.run([sys.executable, os.path.join(project_root, "friday-upstream-sync.py")] + sys.argv[2:])
            return
        elif cmd == "market":
            subcmd = sys.argv[2].lower() if len(sys.argv) > 2 else "track"
            if subcmd == "analyze":
                subprocess.run([sys.executable, os.path.join(project_root, "scripts", "market_correlation_analyst.py")] + sys.argv[3:])
            elif subcmd == "track":
                subprocess.run([sys.executable, os.path.join(project_root, "scripts", "market_chronos_logger.py"), "--daemon"] + sys.argv[3:])
            elif subcmd == "export":
                fmt = sys.argv[3].lower() if len(sys.argv) > 3 else "excel"
                subprocess.run([sys.executable, os.path.join(project_root, "scripts", "market_chronos_logger.py"), "--export", fmt] + sys.argv[4:])
            else:
                subprocess.run([sys.executable, os.path.join(project_root, "scripts", "market_chronos_logger.py")] + sys.argv[2:])
            return
        elif cmd == "clean-pdfs" or cmd == "purge-pdfs":
            subprocess.run([sys.executable, os.path.join(project_root, "scripts", "financial_filings_harvester.py"), "--clean-pdfs"])
            return
        elif cmd == "help" or cmd == "--help" or cmd == "-h":
            show_help()
            return

    # First run? Launch setup wizard automatically
    if not os.path.exists(CONFIG_PATH):
        from friday_setup import run_setup
        run_setup()

        # After setup, ask if they want to start the engine now
        from rich.prompt import Confirm
        start_now = Confirm.ask("\n[cyan]Start F.R.I.D.A.Y. now?[/cyan]", default=True)
        if not start_now:
            return

    # Auto-detect display
    has_display = detect_display()
    os.environ["FRIDAY_HAS_DISPLAY"] = "1" if has_display else "0"
    if has_display:
        from rich.console import Console
        Console().print("[dim]Display detected — GUI mode enabled.[/dim]")
    else:
        from rich.console import Console
        Console().print("[dim]No display — running in terminal-only mode.[/dim]")

    # Boot the engine in chat mode
    from friday_chat import main as friday_chat_main
    friday_chat_main()


if __name__ == "__main__":
    main()
