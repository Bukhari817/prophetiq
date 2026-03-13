#!/usr/bin/env python3
"""
PROPHETIQ — World's First Multi-Agent Real Estate Debate System
Powered by Google Gemini 2.5

Run: python main.py
"""
import sys
from rich.console import Console
from rich.text import Text

console = Console()


def main():
    # Import here to catch missing dependencies gracefully
    try:
        from config import Config
        from core.debate_engine import DebateEngine
        from memory.session_memory import SessionMemory
        from utils.display import Display
    except ImportError as e:
        console.print(f"[red]Missing dependency: {e}[/red]")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
        sys.exit(1)

    display = Display(console)
    display.show_banner()

    config = Config()
    if not config.validate():
        console.print("[bold red]❌ Error: GEMINI_API_KEY not found![/bold red]")
        console.print()
        console.print("To fix this:")
        console.print("  1. Copy [cyan].env.example[/cyan] to [cyan].env[/cyan]")
        console.print("  2. Add your Gemini API key to [cyan].env[/cyan]")
        console.print("  3. Get a free key at: [link]https://aistudio.google.com/apikey[/link]")
        sys.exit(1)

    memory = SessionMemory()
    engine = DebateEngine(config, memory)

    display.show_welcome()

    while True:
        console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        console.print("  [cyan]1.[/cyan] Analyze a property [dim](starts the full debate)[/dim]")
        console.print("  [cyan]2.[/cyan] Compare properties [dim](portfolio view of all analyzed)[/dim]")
        console.print("  [cyan]3.[/cyan] View session history")
        console.print("  [cyan]4.[/cyan] Ask a real estate question")
        console.print("  [cyan]5.[/cyan] Exit")

        try:
            choice = console.input("\n[bold yellow]→ [/bold yellow]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n\n[bold green]Goodbye! May your investments be profitable.[/bold green]")
            break

        if choice == "1":
            try:
                engine.run_property_analysis()
            except KeyboardInterrupt:
                console.print("\n[yellow]Analysis cancelled.[/yellow]")
            except Exception as e:
                console.print(f"\n[red]Something went wrong: {e}[/red]")
                console.print("[dim]Check your API key and internet connection.[/dim]")

        elif choice == "2":
            try:
                engine.compare_properties()
            except KeyboardInterrupt:
                console.print("\n[yellow]Cancelled.[/yellow]")

        elif choice == "3":
            memory.show_history(console)

        elif choice == "4":
            try:
                engine.ask_question()
            except KeyboardInterrupt:
                console.print("\n[yellow]Cancelled.[/yellow]")

        elif choice == "5":
            console.print("\n[bold green]Goodbye! May your investments be profitable.[/bold green]")
            break

        else:
            console.print("[yellow]Please enter 1-5.[/yellow]")


if __name__ == "__main__":
    main()
