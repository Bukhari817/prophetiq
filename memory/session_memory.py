"""
Session Memory — remembers everything analyzed in this session
Enables portfolio comparison and learning from past analyses
"""
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class SessionMemory:
    def __init__(self):
        self.analyses = []
        self.questions = []
        self.session_start = datetime.now()

    def save_analysis(self, property_input: str, results: dict, final_score: float):
        entry = {
            "id": len(self.analyses) + 1,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "property": property_input[:100] + "..." if len(property_input) > 100 else property_input,
            "score": final_score,
            "grade": results.get("grade", "N/A"),
            "recommendation": results.get("recommendation", "N/A"),
            "full_results": results
        }
        self.analyses.append(entry)
        return entry["id"]

    def save_question(self, question: str, answer: str):
        self.questions.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "question": question,
            "answer": answer
        })

    def get_all_analyses(self):
        return self.analyses

    def get_analysis_by_id(self, analysis_id: int):
        for a in self.analyses:
            if a["id"] == analysis_id:
                return a
        return None

    def show_history(self, console: Console):
        if not self.analyses:
            console.print("\n[yellow]No properties analyzed yet in this session.[/yellow]")
            return

        table = Table(title="📊 Session Analysis History", show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Property", min_width=30)
        table.add_column("Score", width=8)
        table.add_column("Grade", width=8)
        table.add_column("Recommendation", width=20)
        table.add_column("Time", width=10)

        for a in self.analyses:
            score_color = "green" if a["score"] >= 7 else "yellow" if a["score"] >= 5 else "red"
            table.add_row(
                str(a["id"]),
                a["property"],
                f"[{score_color}]{a['score']}/10[/{score_color}]",
                a["grade"],
                a["recommendation"],
                a["timestamp"]
            )

        console.print(table)

    def get_portfolio_summary(self):
        if not self.analyses:
            return None
        
        scores = [a["score"] for a in self.analyses]
        return {
            "count": len(self.analyses),
            "avg_score": round(sum(scores) / len(scores), 1),
            "best": max(self.analyses, key=lambda x: x["score"]),
            "worst": min(self.analyses, key=lambda x: x["score"])
        }
