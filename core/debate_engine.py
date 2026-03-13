"""
PROPHETIQ Debate Engine
The brain that orchestrates the multi-agent debate
"""
import google.generativeai as genai
import re
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich.markdown import Markdown

from agents.agent_definitions import AGENTS
from memory.session_memory import SessionMemory
from core.calculator import RealEstateCalculator
from config import Config

console = Console()


class DebateEngine:
    def __init__(self, config: Config, memory: SessionMemory):
        self.config = config
        self.memory = memory
        self.calc = RealEstateCalculator()
        
        # Initialize Gemini
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)

    def _call_agent(self, system_prompt: str, user_prompt: str, agent_name: str) -> str:
        """Call Gemini with agent persona"""
        full_prompt = f"""AGENT PERSONA:
{system_prompt}

YOUR ANALYSIS TASK:
{user_prompt}

Respond in character. Be specific, analytical, and decisive."""
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config.TEMPERATURE,
                    max_output_tokens=self.config.MAX_TOKENS,
                )
            )
            return response.text
        except Exception as e:
            return f"[Agent {agent_name} encountered an error: {str(e)}]"

    def _display_agent_analysis(self, agent_key: str, analysis: str):
        """Display one agent's analysis with styling"""
        agent = AGENTS[agent_key]
        color = agent["color"]
        emoji = agent["emoji"]
        name = agent["name"]
        
        panel = Panel(
            Markdown(analysis),
            title=f"[bold {color}]{emoji} {name}[/bold {color}]",
            border_style=color,
            padding=(1, 2)
        )
        console.print(panel)
        console.print()

    def _extract_score(self, text: str, agent_key: str) -> float:
        """Extract numerical score from agent analysis"""
        # Look for patterns like "SCORE: X/10" or "X/10"
        patterns = [
            r'(?:SCORE[:\s]+)(\d+(?:\.\d+)?)\s*/\s*10',
            r'(\d+(?:\.\d+)?)\s*/\s*10',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                score = float(matches[-1])  # Take last score found
                return min(max(score, 0), 10)
        return 5.0  # Default if not found

    def _get_property_context(self) -> str:
        """Gather property information from user"""
        console.print("\n[bold cyan]📋 PROPERTY INFORMATION[/bold cyan]")
        console.print("[dim]The more you share, the better the debate. Include:[/dim]")
        console.print("[dim]  • Location (city, neighborhood, address)[/dim]")
        console.print("[dim]  • Price, size (sqft/m²), bedrooms[/dim]")
        console.print("[dim]  • Asking rent or rental market[/dim]")
        console.print("[dim]  • Property type (apartment, villa, commercial)[/dim]")
        console.print("[dim]  • Any known issues or special features[/dim]")
        console.print("[dim]  • Your investment goal (rental income, flip, live-in)[/dim]")
        console.print()
        
        console.print("[bold yellow]Paste property details (press Enter twice when done):[/bold yellow]")
        
        lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        
        return "\n".join(lines)

    def run_property_analysis(self):
        """Main analysis flow — the full debate"""
        property_info = self._get_property_context()
        
        if len(property_info.strip()) < 20:
            console.print("[red]Please provide more property details.[/red]")
            return

        console.print("\n")
        console.print(Rule("[bold cyan]🏛️  PROPHETIQ DEBATE COMMENCING[/bold cyan]", style="cyan"))
        console.print()

        # Phase 1: Individual analyses
        console.print("[bold]Phase 1: Individual Agent Analyses[/bold]")
        console.print("[dim]Each specialist analyzes the property independently...[/dim]\n")
        
        agent_analyses = {}
        agent_scores = {}
        
        for agent_key in ["skeptic", "bull", "quant", "sociologist", "contrarian"]:
            agent = AGENTS[agent_key]
            
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[{agent['color']}]{agent['emoji']} {agent['name']} analyzing...[/{agent['color']}]"),
                transient=True,
                console=console
            ) as progress:
                progress.add_task("", total=None)
                
                analysis = self._call_agent(
                    agent["persona"],
                    f"PROPERTY TO ANALYZE:\n\n{property_info}",
                    agent_key
                )
            
            agent_analyses[agent_key] = analysis
            agent_scores[agent_key] = self._extract_score(analysis, agent_key)
            
            self._display_agent_analysis(agent_key, analysis)
            time.sleep(0.5)  # Breathing room between agents

        # Phase 2: The Debate — agents challenge each other
        console.print(Rule("[bold magenta]🔥 THE DEBATE — Agents Challenge Each Other[/bold magenta]", style="magenta"))
        console.print("[dim]The Skeptic vs The Bull — the core tension...[/dim]\n")

        debate_prompt = f"""The Skeptic said:
{agent_analyses['skeptic'][:800]}

The Bull said:
{agent_analyses['bull'][:800]}

The Quant's numbers show:
{agent_analyses['quant'][:600]}

YOU ARE THE SKEPTIC. The Bull has just made the case above. 
Now DIRECTLY challenge the Bull's most optimistic points. Call out where the numbers don't add up.
Keep it sharp — 3-4 key rebuttals maximum. Stay in character."""

        with Progress(SpinnerColumn(), TextColumn("[red]🔍 Skeptic fires back...[/red]"), transient=True, console=console) as progress:
            progress.add_task("", total=None)
            skeptic_rebuttal = self._call_agent(AGENTS["skeptic"]["persona"], debate_prompt, "skeptic_rebuttal")

        console.print(Panel(
            Markdown(skeptic_rebuttal),
            title="[bold red]🔍 Skeptic's Rebuttal[/bold red]",
            border_style="red",
            padding=(1, 2)
        ))
        console.print()

        bull_counter_prompt = f"""The Skeptic just said:
{skeptic_rebuttal[:800]}

YOU ARE THE BULL. Counter these concerns directly. Where is the Skeptic being overly pessimistic?
What opportunities are they completely missing? Give numbers, give examples.
3-4 sharp counterpoints. Stay aggressive but rational."""

        with Progress(SpinnerColumn(), TextColumn("[green]🚀 Bull counters...[/green]"), transient=True, console=console) as progress:
            progress.add_task("", total=None)
            bull_counter = self._call_agent(AGENTS["bull"]["persona"], bull_counter_prompt, "bull_counter")

        console.print(Panel(
            Markdown(bull_counter),
            title="[bold green]🚀 Bull's Counter[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        console.print()

        # Phase 3: Judge's Verdict
        console.print(Rule("[bold white]⚖️  THE JUDGE DELIVERS VERDICT[/bold white]", style="white"))
        console.print()

        judge_prompt = f"""You have observed the full debate. Here is the complete record:

=== THE SKEPTIC'S ANALYSIS ===
{agent_analyses['skeptic'][:1000]}

=== THE BULL'S ANALYSIS ===
{agent_analyses['bull'][:1000]}

=== THE QUANT'S NUMBERS ===
{agent_analyses['quant'][:1000]}

=== THE SOCIOLOGIST'S VIEW ===
{agent_analyses['sociologist'][:800]}

=== THE CONTRARIAN'S ANGLE ===
{agent_analyses['contrarian'][:800]}

=== THE DEBATE ===
Skeptic rebuttal: {skeptic_rebuttal[:500]}
Bull counter: {bull_counter[:500]}

ORIGINAL PROPERTY:
{property_info}

Now deliver your FINAL VERDICT as the Judge."""

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold white]⚖️  Judge deliberating final verdict...[/bold white]"),
            transient=True,
            console=console
        ) as progress:
            progress.add_task("", total=None)
            verdict = self._call_agent(AGENTS["judge"]["persona"], judge_prompt, "judge")

        console.print(Panel(
            Markdown(verdict),
            title="[bold white]⚖️  PROPHETIQ FINAL VERDICT[/bold white]",
            border_style="white",
            padding=(1, 2)
        ))

        # Score summary table
        console.print("\n")
        self._display_score_summary(agent_scores, verdict)

        # Save to memory
        final_score = sum(agent_scores.values()) / len(agent_scores)
        
        # Extract grade and recommendation from verdict
        grade = "B"
        recommendation = "Hold"
        grade_match = re.search(r'INVESTMENT GRADE[:\s]+([A-F][+\-]?)', verdict, re.IGNORECASE)
        if grade_match:
            grade = grade_match.group(1)
        rec_match = re.search(r'(?:RECOMMENDATION|PROPHETIQ)[:\s]+(Strong Buy|Buy|Hold|Avoid|Strong Avoid)', verdict, re.IGNORECASE)
        if rec_match:
            recommendation = rec_match.group(1)

        results = {
            "agent_scores": agent_scores,
            "final_score": round(final_score, 1),
            "grade": grade,
            "recommendation": recommendation,
            "verdict_summary": verdict[:500]
        }
        
        analysis_id = self.memory.save_analysis(property_info, results, round(final_score, 1))
        console.print(f"\n[dim]Analysis saved as #{analysis_id} in session memory.[/dim]")

    def _display_score_summary(self, agent_scores: dict, verdict: str):
        """Display the score breakdown table"""
        table = Table(title="📊 Agent Score Summary", show_header=True, header_style="bold cyan")
        table.add_column("Agent", min_width=20)
        table.add_column("Score", width=10, justify="center")
        table.add_column("Signal", width=15, justify="center")

        score_data = {
            "skeptic": ("🔍 The Skeptic", "red"),
            "bull": ("🚀 The Bull", "green"),
            "quant": ("📊 The Quant", "blue"),
            "sociologist": ("🌆 The Sociologist", "yellow"),
            "contrarian": ("🔄 The Contrarian", "magenta")
        }

        total = 0
        for key, (name, color) in score_data.items():
            score = agent_scores.get(key, 5.0)
            total += score
            signal = "🟢 Positive" if score >= 7 else "🟡 Neutral" if score >= 5 else "🔴 Caution"
            table.add_row(
                f"[{color}]{name}[/{color}]",
                f"[bold]{score}/10[/bold]",
                signal
            )

        avg = round(total / len(score_data), 1)
        table.add_row("", "", "")
        table.add_row("[bold white]CONSENSUS[/bold white]", f"[bold white]{avg}/10[/bold white]", 
                     "🏆 Final Score")

        console.print(table)

    def compare_properties(self):
        """Compare all properties analyzed in this session"""
        analyses = self.memory.get_all_analyses()
        
        if len(analyses) < 2:
            console.print("\n[yellow]Need at least 2 analyzed properties to compare. Analyze more properties first.[/yellow]")
            return

        console.print(Rule("[bold cyan]📈 Portfolio Comparison[/bold cyan]", style="cyan"))
        
        summary = self.memory.get_portfolio_summary()
        
        table = Table(title="Property Comparison Matrix", show_header=True, header_style="bold cyan")
        table.add_column("#", width=4)
        table.add_column("Property", min_width=35)
        table.add_column("Score", width=8, justify="center")
        table.add_column("Grade", width=8, justify="center")
        table.add_column("Verdict", width=20)

        for a in analyses:
            score = a["score"]
            color = "green" if score >= 7 else "yellow" if score >= 5 else "red"
            table.add_row(
                str(a["id"]),
                a["property"],
                f"[{color}]{score}/10[/{color}]",
                a["grade"],
                a["recommendation"]
            )

        console.print(table)
        console.print(f"\n[bold]Session Summary:[/bold]")
        console.print(f"  • Properties Analyzed: [cyan]{summary['count']}[/cyan]")
        console.print(f"  • Average Score: [cyan]{summary['avg_score']}/10[/cyan]")
        console.print(f"  • Best Property: [green]#{summary['best']['id']} ({summary['best']['score']}/10)[/green]")
        console.print(f"  • Weakest Property: [red]#{summary['worst']['id']} ({summary['worst']['score']}/10)[/red]")

        # Ask Gemini for portfolio-level insight
        properties_text = "\n".join([f"Property {a['id']}: {a['property']} — Score: {a['score']}/10, Grade: {a['grade']}" for a in analyses])
        
        portfolio_prompt = f"""As a senior real estate portfolio advisor, here are the properties a client has analyzed:

{properties_text}

Give brief portfolio-level advice:
1. Which is the strongest investment and why?
2. Any diversification considerations?
3. One key strategic insight for this investor

Keep it concise — this is a summary, not a full analysis."""

        with Progress(SpinnerColumn(), TextColumn("[cyan]Generating portfolio insight...[/cyan]"), transient=True, console=console) as progress:
            progress.add_task("", total=None)
            portfolio_advice = self._call_agent(AGENTS["judge"]["persona"], portfolio_prompt, "portfolio")

        console.print(Panel(
            Markdown(portfolio_advice),
            title="[bold cyan]🎯 Portfolio Intelligence[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))

    def ask_question(self):
        """Ask any real estate question — powered by all agent knowledge"""
        console.print("\n[bold cyan]💬 REAL ESTATE INTELLIGENCE[/bold cyan]")
        console.print("[dim]Ask anything — market strategy, investment concepts, due diligence, negotiation...[/dim]\n")
        
        question = console.input("[bold yellow]Your question: [/bold yellow]").strip()
        
        if not question:
            return

        # Include session context if available
        session_context = ""
        if self.memory.analyses:
            session_context = f"\n\nCONTEXT — User has analyzed these properties this session:\n"
            for a in self.memory.analyses:
                session_context += f"- {a['property']} (Score: {a['score']}/10, {a['recommendation']})\n"

        prompt = f"""You are PROPHETIQ — a world-class real estate intelligence system powered by 5 specialist agents (Skeptic, Bull, Quant, Sociologist, Contrarian).

A user asks: {question}
{session_context}

Answer with the depth and insight of all 5 specialists combined. Be practical, specific, and honest.
Use real numbers and examples where relevant. Don't hedge — give real advice."""

        with Progress(SpinnerColumn(), TextColumn("[cyan]Thinking...[/cyan]"), transient=True, console=console) as progress:
            progress.add_task("", total=None)
            answer = self._call_agent(prompt, question, "qa")

        console.print(Panel(
            Markdown(answer),
            title="[bold cyan]💡 PROPHETIQ Intelligence[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))

        self.memory.save_question(question, answer)
