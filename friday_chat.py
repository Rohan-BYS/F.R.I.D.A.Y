import asyncio
import os
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print as rprint

# Ensure engine is accessible
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from friday_engine.core.engine import FridayEngine
from friday_engine.config import FridayConfig

console = Console()

# Custom styles for the prompt
style = Style.from_dict({
    'prompt': 'ansicyan bold',
    'sign': 'ansiyellow bold',
})

async def chat_loop():
    console.print(Panel(
        "[bold cyan]F.R.I.D.A.Y. Terminal Interface[/bold cyan]\n"
        "[dim]Type your message, or type /help for commands. Press Ctrl+C to exit.[/dim]",
        border_style="cyan"
    ))
    
    config = FridayConfig()
    engine = FridayEngine(config)
    
    with console.status("[cyan]Booting F.R.I.D.A.Y. Omnicore... (Starting memory, agents, and Webhooks)[/cyan]") as status:
        # We will wrap boot in a timeout just in case something is fatally blocked
        try:
            status.update("[cyan]Connecting to external MCP servers (WhatsApp, etc)... this may take a moment to download dependencies.[/cyan]")
            await asyncio.wait_for(engine.boot(), timeout=60.0)
        except asyncio.TimeoutError:
            console.print("[yellow]Warning: Boot took longer than 60s (likely downloading MCP server packages). Continuing anyway.[/yellow]")
            
    session = PromptSession()
    
    while True:
        try:
            # F.R.I.D.A.Y. custom prompt
            user_input = await session.prompt_async(HTML('<prompt>You</prompt><sign> ❯ </sign>'), style=style)
            user_input = user_input.strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "/exit", "/quit"]:
                console.print("[dim]Shutting down F.R.I.D.A.Y... Goodbye.[/dim]")
                break
                
            if user_input.lower() == "/help":
                console.print(Panel(
                    "[bold]/help[/bold] - Show this menu\n"
                    "[bold]/models[/bold] - List available AI models\n"
                    "[bold]/switch <model>[/bold] - Switch active AI model\n"
                    "[bold]/clear[/bold] - Clear terminal\n"
                    "[bold]/setup[/bold] - Re-run the configuration wizard",
                    title="Commands", border_style="yellow"
                ))
                continue
                
            if user_input.lower() == "/clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
                
            if user_input.lower() == "/setup":
                from friday_setup import run_setup
                run_setup()
                continue
                
            if user_input.lower() == "/models":
                providers = list(engine.llm.providers.keys())
                console.print(f"[cyan]Available models:[/cyan] {', '.join(providers)}")
                continue
                
            if user_input.lower().startswith("/switch"):
                parts = user_input.split()
                if len(parts) > 1:
                    new_model = parts[1]
                    if new_model in engine.llm.providers:
                        engine.llm.priority = [new_model] + [p for p in engine.llm.priority if p != new_model]
                        console.print(f"[green]Switched primary model to {new_model}.[/green]")
                    else:
                        console.print(f"[red]Model {new_model} not found. Use /models to list available.[/red]")
                continue

            # Process AI Response
            with console.status("[cyan]F.R.I.D.A.Y. is thinking...[/cyan]"):
                response_text = await engine.chat(user_input)
                
            console.print(Markdown(f"**F.R.I.D.A.Y.** ❯\n{response_text}"))
            console.print()

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

def main():
    asyncio.run(chat_loop())

if __name__ == "__main__":
    main()
