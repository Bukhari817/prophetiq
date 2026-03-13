"""
Display utilities — the face of PROPHETIQ
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


class Display:
    def __init__(self, console: Console):
        self.console = console

    def show_banner(self):
        banner = """
██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗████████╗██╗ ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║  ██║██╔════╝╚══██╔══╝██║██╔═══██╗
██████╔╝██████╔╝██║   ██║██████╔╝███████║█████╗     ██║   ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══██║██╔══╝     ██║   ██║██║▄▄ ██║
██║     ██║  ██║╚██████╔╝██║     ██║  ██║███████╗   ██║   ██║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝ ╚══▀▀═╝ 
"""
        self.console.print(Text(banner, style="bold cyan"))
        self.console.print(Align.center(
            Text("World's First Multi-Agent Real Estate Debate System", style="bold white")
        ))
        self.console.print(Align.center(
            Text("5 AI Specialists • Real Debates • Decisive Verdicts", style="dim")
        ))
        self.console.print()

    def show_welcome(self):
        panel = Panel(
            """[bold]How it works:[/bold]

[cyan]1.[/cyan] Submit a property → 5 specialist agents analyze it independently
[cyan]2.[/cyan] Agents debate each other (Skeptic challenges Bull, etc.)
[cyan]3.[/cyan] The Judge weighs all arguments → delivers final verdict & score

[bold]Your 5 Agents:[/bold]
  [red]🔍 The Skeptic[/red]   — finds every red flag and risk
  [green]🚀 The Bull[/green]      — finds every opportunity and upside
  [blue]📊 The Quant[/blue]      — crunches every number, ROI, yield
  [yellow]🌆 The Sociologist[/yellow] — reads neighborhood trends and human factors
  [magenta]🔄 The Contrarian[/magenta] — challenges assumptions everyone else misses
  [white]⚖️  The Judge[/white]    — synthesizes everything into a final decision""",
            title="[bold cyan]Welcome to PROPHETIQ[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)
