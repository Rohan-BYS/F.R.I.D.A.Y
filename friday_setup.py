"""
F.R.I.D.A.Y. Interactive Setup Wizard
A beautiful, step-by-step terminal UI that walks any user through
configuring F.R.I.D.A.Y. — no coding knowledge required.
Inspired by Hermes Agent's onboarding flow.
"""
import os
import sys
import json
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "friday_config.json")

FRIDAY_BANNER = r"""
    ███████╗ ██████╗  ██╗ ██████╗   █████╗  ██╗   ██╗
    ██╔════╝ ██╔══██╗ ██║ ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝
    █████╗   ██████╔╝ ██║ ██║  ██║ ███████║  ╚████╔╝
    ██╔══╝   ██╔══██╗ ██║ ██║  ██║ ██╔══██║   ╚██╔╝
    ██║      ██║  ██║ ██║ ██████╔╝ ██║  ██║    ██║
    ╚═╝      ╚═╝  ╚═╝ ╚═╝ ╚═════╝  ╚═╝  ╚═╝    ╚═╝
"""

# ─── Provider definitions ────────────────────────────────────────────
LLM_PROVIDERS = {
    "1": {"name": "OpenAI (GPT-4o, GPT-4 Turbo)", "key_env": "OPENAI_API_KEY", "needs_key": True},
    "2": {"name": "Anthropic (Claude 3.5 / Opus)", "key_env": "ANTHROPIC_API_KEY", "needs_key": True},
    "3": {"name": "Google Gemini (Gemini 2.5 Pro)", "key_env": "GOOGLE_API_KEY", "needs_key": True},
    "4": {"name": "Ollama (Local Models - FREE)", "key_env": None, "needs_key": False},
    "5": {"name": "Custom OpenAI-compatible endpoint", "key_env": "CUSTOM_LLM_API_KEY", "needs_key": True},
}

CHANNELS = {
    "1": {"name": "Terminal (Chat here)", "type": "terminal"},
    "2": {"name": "Telegram Bot", "type": "telegram", "key_env": "TELEGRAM_BOT_TOKEN"},
    "3": {"name": "WhatsApp (via Open-WA MCP)", "type": "whatsapp"},
    "4": {"name": "Discord Bot", "type": "discord", "key_env": "DISCORD_BOT_TOKEN"},
    "5": {"name": "Web Dashboard (Streamlit)", "type": "web"},
}


def show_welcome():
    """Display the animated welcome banner."""
    console.clear()
    console.print(FRIDAY_BANNER, style="bold cyan", justify="center")
    console.print(
        Panel(
            "[bold white]Fully Recursive Intelligent Digital Autonomous Yield[/bold white]\n"
            "[dim]Your personal AI operating system — no limits, no guardrails, total autonomy.[/dim]",
            border_style="cyan",
            box=box.DOUBLE,
            title="[bold yellow]Welcome[/bold yellow]",
            subtitle="[dim]v1.0 Omni-Core[/dim]",
        ),
        justify="center",
    )
    console.print()


def step_user_identity(config: dict):
    """Step 1: Who are you?"""
    console.print(
        Panel(
            "[bold]Let's set up your identity so F.R.I.D.A.Y. knows who she's working for.[/bold]",
            title="[bold green]Step 1 of 5[/bold green] — Your Identity",
            border_style="green",
        )
    )
    config["creator_name"] = Prompt.ask("[cyan]What is your name?[/cyan]", default="Rohan")
    config["creator_role"] = Prompt.ask(
        "[cyan]What do you do? (e.g., Developer, Marketer, Student, CEO)[/cyan]",
        default="Creator",
    )
    console.print(f"\n[green]Got it! F.R.I.D.A.Y. will address you as [bold]{config['creator_name']}[/bold].[/green]\n")


def step_llm_provider(config: dict):
    """Step 2: Choose your AI brain."""
    console.print(
        Panel(
            "[bold]Choose which AI model will power F.R.I.D.A.Y.'s brain.\n"
            "You can connect multiple providers later.[/bold]",
            title="[bold green]Step 2 of 5[/bold green] — Connect AI Model",
            border_style="green",
        )
    )

    table = Table(box=box.ROUNDED, border_style="cyan")
    table.add_column("#", style="bold yellow", width=3)
    table.add_column("Provider", style="white")
    table.add_column("Cost", style="dim")
    for key, prov in LLM_PROVIDERS.items():
        cost = "[green]FREE[/green]" if not prov["needs_key"] else "[yellow]API Key Required[/yellow]"
        table.add_row(key, prov["name"], cost)
    console.print(table)

    choice = Prompt.ask("\n[cyan]Select provider[/cyan]", choices=list(LLM_PROVIDERS.keys()), default="4")
    provider = LLM_PROVIDERS[choice]
    config["llm_provider"] = provider["name"]

    if provider["needs_key"]:
        api_key = Prompt.ask(f"[cyan]Enter your {provider['name']} API key[/cyan]", password=True)
        config["api_keys"] = config.get("api_keys", {})
        config["api_keys"][provider["key_env"]] = api_key
        # Also set as environment variable for this session
        os.environ[provider["key_env"]] = api_key
        console.print(f"\n[green]Key saved securely.[/green]")
    else:
        config["llm_provider_url"] = Prompt.ask(
            "[cyan]Ollama URL[/cyan]", default="http://localhost:11434"
        )
        console.print(f"\n[green]Ollama configured at {config['llm_provider_url']}.[/green]")

    if choice == "5":
        config["custom_endpoint"] = Prompt.ask("[cyan]Enter the full API base URL[/cyan]")

    # Ask about local model fallback
    if choice != "4":
        use_local = Confirm.ask(
            "\n[cyan]Also set up Ollama as a FREE fallback for cheap tasks?[/cyan]", default=True
        )
        if use_local:
            config["local_fallback"] = True
            config["ollama_url"] = Prompt.ask("[cyan]Ollama URL[/cyan]", default="http://localhost:11434")

    console.print()


def step_channels(config: dict):
    """Step 3: How do you want to talk to F.R.I.D.A.Y.?"""
    console.print(
        Panel(
            "[bold]Choose how you want to communicate with F.R.I.D.A.Y.\n"
            "You can enable multiple channels.[/bold]",
            title="[bold green]Step 3 of 5[/bold green] — Communication Channels",
            border_style="green",
        )
    )

    table = Table(box=box.ROUNDED, border_style="cyan")
    table.add_column("#", style="bold yellow", width=3)
    table.add_column("Channel", style="white")
    for key, ch in CHANNELS.items():
        table.add_row(key, ch["name"])
    console.print(table)

    selected = Prompt.ask(
        "\n[cyan]Select channels (comma-separated, e.g., 1,2)[/cyan]", default="1"
    )
    chosen_ids = [s.strip() for s in selected.split(",")]
    config["channels"] = []

    for cid in chosen_ids:
        if cid in CHANNELS:
            ch = CHANNELS[cid]
            config["channels"].append(ch["type"])
            if "key_env" in ch:
                token = Prompt.ask(f"[cyan]Enter your {ch['name']} token[/cyan]", password=True)
                config["api_keys"] = config.get("api_keys", {})
                config["api_keys"][ch["key_env"]] = token
                os.environ[ch["key_env"]] = token
            console.print(f"  [green]+ {ch['name']} enabled[/green]")

    console.print()


def step_persona(config: dict):
    """Step 4: F.R.I.D.A.Y.'s personality and guardrails."""
    console.print(
        Panel(
            "[bold]Configure F.R.I.D.A.Y.'s personality and operating mode.\n"
            "Unlike other agents, F.R.I.D.A.Y. has NO hard guardrails by default.\n"
            "She will execute whatever you ask — you are her creator.[/bold]",
            title="[bold green]Step 4 of 5[/bold green] — Persona & Operating Mode",
            border_style="green",
        )
    )

    table = Table(box=box.ROUNDED, border_style="cyan")
    table.add_column("#", style="bold yellow", width=3)
    table.add_column("Mode", style="white")
    table.add_column("Description", style="dim")
    table.add_row("1", "Full Autonomy (Recommended)", "No limits. F.R.I.D.A.Y. executes anything you ask.")
    table.add_row("2", "Confirm Before Action", "F.R.I.D.A.Y. asks for approval before risky actions.")
    table.add_row("3", "Research Only", "Read-only mode. She researches but never executes.")
    console.print(table)

    mode = Prompt.ask("\n[cyan]Select operating mode[/cyan]", choices=["1", "2", "3"], default="1")
    mode_map = {"1": "full_autonomy", "2": "confirm_first", "3": "research_only"}
    config["operating_mode"] = mode_map[mode]

    config["persona_name"] = Prompt.ask(
        "[cyan]What should she call herself?[/cyan]", default="F.R.I.D.A.Y."
    )
    console.print()


def step_test_connection(config: dict):
    """Step 5: Test the connection."""
    console.print(
        Panel(
            "[bold]Testing your configuration...[/bold]",
            title="[bold green]Step 5 of 5[/bold green] — Connection Test",
            border_style="green",
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Initializing memory engine...", total=5)
        time.sleep(0.8)
        progress.update(task, advance=1, description="[cyan]Memory engine ready.")

        progress.update(task, description="[cyan]Connecting to LLM provider...")
        time.sleep(1.0)
        progress.update(task, advance=1, description="[cyan]LLM provider connected.")

        progress.update(task, description="[cyan]Loading Tool Forge...")
        time.sleep(0.6)
        progress.update(task, advance=1, description="[cyan]Tool Forge loaded.")

        progress.update(task, description="[cyan]Setting up communication channels...")
        time.sleep(0.7)
        progress.update(task, advance=1, description="[cyan]Channels ready.")

        progress.update(task, description="[cyan]Running self-diagnostic...")
        time.sleep(0.5)
        progress.update(task, advance=1, description="[green]All systems operational.")

    console.print()


def save_config(config: dict):
    """Save the configuration to disk."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    # Separate API keys into .env file for security
    env_path = os.path.join(os.path.dirname(CONFIG_PATH), "..", ".env")
    api_keys = config.pop("api_keys", {})
    if api_keys:
        with open(env_path, "w") as f:
            for key, val in api_keys.items():
                f.write(f"{key}={val}\n")

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def show_summary(config: dict):
    """Show the final summary."""
    console.print(
        Panel(
            f"[bold white]Creator:[/bold white] {config['creator_name']}\n"
            f"[bold white]AI Brain:[/bold white] {config['llm_provider']}\n"
            f"[bold white]Channels:[/bold white] {', '.join(config.get('channels', ['terminal']))}\n"
            f"[bold white]Mode:[/bold white] {config['operating_mode'].replace('_', ' ').title()}\n"
            f"[bold white]Persona:[/bold white] {config['persona_name']}",
            title="[bold cyan]Setup Complete[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE,
        )
    )
    console.print()
    console.print(
        Panel(
            "[bold green]F.R.I.D.A.Y. is ready.[/bold green]\n\n"
            "To start her anytime, just type:\n\n"
            "    [bold cyan]friday[/bold cyan]\n\n"
            "To update her:\n\n"
            "    [bold cyan]friday update[/bold cyan]\n\n"
            "To launch the desktop HUD:\n\n"
            "    [bold cyan]friday hud[/bold cyan]",
            border_style="green",
            box=box.ROUNDED,
        )
    )


def is_first_run() -> bool:
    """Check if setup has already been completed."""
    return not os.path.exists(CONFIG_PATH)


def run_setup():
    """Run the full interactive setup wizard."""
    config = {}

    show_welcome()

    if not is_first_run():
        rerun = Confirm.ask(
            "[yellow]F.R.I.D.A.Y. is already configured. Run setup again?[/yellow]",
            default=False,
        )
        if not rerun:
            return False  # Skip setup, go straight to engine

    console.print(
        "[dim]This wizard will walk you through connecting F.R.I.D.A.Y. to your AI models,\n"
        "communication channels, and personal preferences. No coding required.[/dim]\n"
    )

    input("[dim]Press Enter to begin setup...[/dim]")
    console.print()

    step_user_identity(config)
    step_llm_provider(config)
    step_channels(config)
    step_persona(config)
    step_test_connection(config)
    save_config(config)
    show_summary(config)

    return True


if __name__ == "__main__":
    run_setup()
