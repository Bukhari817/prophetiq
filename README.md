# 🏛️ PROPHETIQ — World's First Multi-Agent Real Estate Debate System

> *"Before you sign anything, let 5 AI specialists fight about it."*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 2.5](https://img.shields.io/badge/Powered%20by-Gemini%202.5-orange.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

Most real estate AI tools are chatbots. You ask a question, you get an answer. That's fine.

**PROPHETIQ is different.**

When you submit a property, 5 specialist AI agents analyze it from completely different angles — then they *argue with each other*. The Skeptic attacks the Bull's optimism. The Bull challenges the Skeptic's pessimism. The Quant brings hard numbers. The Sociologist reads the neighborhood's future. The Contrarian questions everything everyone else assumed.

Then a Judge synthesizes the debate into a decisive, actionable verdict.

This isn't a chatbot. It's a boardroom debate for your investment decision.

---

## The 5 Agents

| Agent | Role | Focus |
|-------|------|-------|
| 🔍 **The Skeptic** | Risk Analyst | Red flags, hidden costs, overvaluation, what can go wrong |
| 🚀 **The Bull** | Opportunity Finder | Growth potential, upside, undervalued aspects |
| 📊 **The Quant** | Numbers Expert | ROI, yield, cap rates, cash flow, break-even |
| 🌆 **The Sociologist** | Urban Analyst | Demographics, neighborhood trajectory, livability |
| 🔄 **The Contrarian** | Assumption Challenger | Unconventional risks/opportunities others miss |
| ⚖️ **The Judge** | Final Arbitrator | Synthesizes debate → decisive verdict |

---

## Features

- **Multi-Agent Debate**: Agents don't just analyze — they challenge each other in real time
- **Financial Calculations**: Gross/Net yield, Cap rate, P/R ratio, mortgage analysis, 5/10/20yr projections
- **Investment Scoring**: Each agent scores independently; Judge synthesizes to consensus
- **Investment Grade**: A+ to F grading with explanation
- **Session Memory**: Remembers all properties analyzed; compare them as a portfolio
- **Portfolio Intelligence**: Analyze multiple properties, get portfolio-level advice
- **Real Estate Q&A**: Ask any real estate question, get multi-agent wisdom
- **Beautiful CLI**: Rich terminal interface with colors, panels, progress indicators

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/prophetiq.git
cd prophetiq
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your free Gemini API key
Go to [Google AI Studio](https://aistudio.google.com/apikey) → Create API Key → Copy it

### 4. Configure
```bash
cp .env.example .env
# Edit .env and paste your API key
```

### 5. Run
```bash
python main.py
```

---

## Example Analysis Flow

```
You: 3BHK apartment, DHA Phase 5 Lahore, asking PKR 2.5 crore
     650 sqft, 3rd floor, 10 years old building
     Rent in area: PKR 65,000/month
     Goal: Rental income + long-term appreciation

🔍 Skeptic: "Maintenance costs on a 10-year building will escalate..."
             SKEPTIC SCORE: 4/10

🚀 Bull: "DHA Phase 5 has 8% annual appreciation history, undervalued vs Phase 6..."
          BULL SCORE: 7.5/10

📊 Quant: "Gross yield: 3.12% — below market threshold of 4%..."
           QUANT SCORE: 5/10

🌆 Sociologist: "Phase 5 demographics shifting to young professionals post-2022..."
                 SOCIOLOGIST SCORE: 7/10

🔄 Contrarian: "Everyone's buying DHA. The smart money moved to Bahria Town..."
                CONTRARIAN SCORE: 6/10

[Debate erupts...]

⚖️ Judge: GRADE: B | RECOMMENDATION: Buy (with conditions)
          Consensus Score: 5.9/10
```

---

## Project Structure

```
prophetiq/
├── main.py                    # Entry point
├── config.py                  # Configuration (model, API settings)
├── requirements.txt
├── .env.example
├── agents/
│   ├── __init__.py
│   └── agent_definitions.py   # All 6 agent personas
├── core/
│   ├── __init__.py
│   ├── debate_engine.py       # Orchestrates the full debate
│   └── calculator.py          # Real estate financial calculations
├── memory/
│   ├── __init__.py
│   └── session_memory.py      # Session history & portfolio memory
├── reports/
│   └── __init__.py
└── utils/
    ├── __init__.py
    └── display.py             # CLI display and banner
```

---

## Why Gemini 2.5?

- **Free tier** is generous enough for full debates
- **Large context window** — agents can read each other's full analyses
- **Strong reasoning** — handles nuanced investment analysis well
- `gemini-2.5-flash-preview-04-17` is the default model (fast + capable)

If you want maximum quality, change `MODEL_NAME` in `config.py` to `gemini-2.5-pro-preview-05-06`.

---

## Contributing

PRs welcome. Ideas for new agents:
- 🏗️ **The Developer** — renovation cost estimator + value-add expert
- ⚖️ **The Lawyer** — title issues, zoning, legal risks
- 🌍 **The Macro Economist** — interest rate impact, currency risk, global factors

---

## License

MIT — use it, fork it, build on it.

---

*Built with Python + Google Gemini 2.5 + Rich + way too much coffee.*
