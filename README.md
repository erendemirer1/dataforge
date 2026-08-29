# DataForge — Living Synthetic Society OS
### *Strategic Cognitive Digital Twin & Stratified Demographic Simulation Engine for Turkey*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-79%2F79%20Passing%20(%25100)-52B788?style=flat)](file:///tests)
[![License](https://img.shields.io/badge/License-MIT-D4A373?style=flat)](LICENSE)

---

## 🇹🇷 Why DataForge?

Whether you are a municipal leader, political campaign manager, public opinion researcher, or enterprise executive:
* **Traditional Field Polling:** Takes 4 to 6 weeks, burns thousands of dollars, and by the time reports hit your desk, the societal agenda has completely shifted.
* **Generic LLM Prompts:** Lack demographic grounding, hallucinate probabilities, and flatten 85 million distinct human beings into bland, polite corporate monoculture.

**DataForge replaces both paradigms with a deterministic, living computational twin.**  
By anchoring every synthetic individual to empirical datasets (TÜİK household income distributions, BDDK debt ratios, SEGE district socioeconomic tiers, and YSK electoral histories), DataForge generates representative, stratified populations ($N=1,000$ in 12ms) across Turkey's 81 provinces and 973 districts—reflecting the unvarnished, authentic pulse of the street.

---

## 🏛️ The 5 Scientific & Computational Pillars

DataForge replaces guesswork with formal econometrics, computational social science, and cognitive psychology:

```
                                 [ Policy / Ballot Query ]
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               LIVE MACRO & SOCIAL PULSE (Central Bank Rates, Live FX, News RSS)        │
│               └── Real-Time Societal Agitation & Wallet Strain Index (Ψ_live)          │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               DETERMINISTIC STRATIFIED SAMPLER (CPU / N=1,000 in 12ms)                 │
│  ├── NUTS-2 Regional Weighting (TR10 Istanbul to TRA2 Agri/Kars)                        │
│  ├── SEGE-2022 Socioeconomic Tiers (1 to 6) & ISCO-08 Income-Occupation Covariance    │
│  ├── Gaussian Copula Joint Distribution Engine for Age-Income-Debt Correlation         │
│  └── 81-Province Empirical Ideological Cohort Matrix (YSK Calibrated)                  │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                     ┌───────────────────────┴───────────────────────┐
                     ▼                                               ▼
┌───────────────────────────────────────────┐   ┌───────────────────────────────────────────┐
│        STRUCTURAL CAUSAL DAG ENGINE       │   │    COGNITIVE HABITUS & MORAL TENSOR       │
│  ├── Pearl Causal DAG: Shock ➔ Loss λ     │   │  ├── Kahneman Loss Aversion (λ = 2.25)    │
│  ├── Counterfactual do(X) Macro Shocks    │   │  ├── Jonathan Haidt 6 Moral Foundations   │
│  └── Persistent SQLite Episodic Memory    │   │  └── Laibson Quasi-Hyperbolic Time Model  │
└───────────────────────────────────────────┘   └───────────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                  AUTHENTIC DISCURSIVE VOCALIZATION & STREET VERNACULAR                 │
│  ├── Pro-Kurdish / DEM Base: Democratic resolution, anti-trusteeship, peace, amnesty   │
│  ├── Turkish Nationalist / Ülkücü Base: National unity, uncompromising counter-terror │
│  ├── Secular / Kemalist Base: Constitutional order, meritocracy, parliamentary debate  │
│  ├── Conservative / Incumbent Base: State survival, leadership trust, social stability │
│  └── Pragmatist Youth / Apolitical Base: Rent pressure, youth employment, meritocracy │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Capabilities

### 1. Stratified Quantitative Census & Political Camp Breakdown (`MunicipalCensusEngine`)
Simulates municipal, national, or ecological referendums across any target geography:
* Computes 95% confidence intervals and margin of error ($\pm \%1.96$).
* **5 Ideological Camp Cross-Tabulations:** (% DEM, % MHP/Zafer, % CHP, % AK Party, % Apolitical).
* Demographic segmentations across age brackets, household income tiers, and housing status (tenant vs. homeowner).

### 2. Live Macroeconomic & News Agenda Stream (`LivingStreamEngine`)
DataForge connects directly to public data endpoints with automatic caching:
* Real-time live USD/TRY exchange rates from open currency APIs (e.g. `48.23 ₺`),
* Official TÜİK benchmark inflation and TCMB policy rates,
* Real-time headline scanning via live BBC Türkçe and TRT Haber RSS feeds, computing the **Societal Agitation Index** ($\Psi_{live}$).

### 3. Socratic 1-on-1 Persona Interrogation (`InterrogationEngine`)
Conduct qualitative multi-turn probing with any sampled citizen:
* **Subconscious Inner Voice (System 1):** Raw, unfiltered, self-interested primal reaction.
* **Public Statement (System 2):** Socially acceptable, rationalized articulation.
* **Bayesian Belief Shift Badge ($+\%\Delta P$):** Quantifies how deeply your counter-arguments swayed or reinforced their conviction.

### 4. Macroeconomic Counterfactual Stress-Testing (`CounterfactualEngine`)
Simulates instant economic shocks (e.g., $do(\text{Inflation} = +15\%)$, minimum wage hikes, residential rent caps) across the population tensor. Evaluates real-time discretionary budget compression and political vote shifts in sub-100ms.

### 5. 100+ Parameter Micro-Biographical Tensor (`MicroBiographySynthesizer`)
Synthesizes fine-grained human details for every persona: morning vitality scores, daily tea/coffee habits, end-of-month rent day anxiety (1–10), hometown nostalgia, and deep emotional vulnerabilities.

---

## 💻 Quickstart

### Prerequisites
* Python 3.10, 3.11, or 3.12
* Linux / WSL (Recommended) or macOS / Windows

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/erendemirer1/dataforge.git
cd dataforge

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies & local package
pip install -r requirements.txt
pip install -e .
```

### 2. Launch Local Server
```bash
python3 -m uvicorn dataforge.api.app:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:  
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🧪 Comprehensive Test Suite

DataForge includes **79 rigorous unit and integration tests** covering econometrics, copula distributions, causal graphs, and API endpoints:

```bash
python3 -m pytest
```

```text
============================= test session starts ==============================
collected 79 items

tests/test_api.py ...                                                    [  3%]
tests/test_behavior.py .......                                           [ 12%]
tests/test_calibration.py ..                                             [ 15%]
tests/test_causal.py ..                                                  [ 17%]
tests/test_causal_framework.py ...                                       [ 21%]
tests/test_census.py ..                                                  [ 24%]
tests/test_contagion.py .                                                [ 25%]
tests/test_counterfactual.py .                                           [ 26%]
tests/test_generators.py ......................................          [ 74%]
tests/test_historical_backtesting.py .....                               [ 81%]
tests/test_interrogation.py .                                            [ 82%]
tests/test_ml.py .                                                       [ 83%]
tests/test_society_api.py ...                                            [ 87%]
tests/test_tckn.py ..........                                            [100%]

======================== 79 passed, 1 warning in 15.23s ========================
```

---

## 📂 Project Architecture

```
dataforge/
├── dataforge/
│   ├── api/
│   │   ├── app.py                     # FastAPI core application
│   │   ├── routes/
│   │   │   ├── society.py             # Live pulse, interrogation, census endpoints
│   │   │   └── generators.py          # Data generation REST routes
│   │   └── static/
│   │       ├── index.html             # Gazette HUD & Real D3 Mercator Map UI
│   │       └── assets/tr-cities.json  # 81-Province GeoJSON spatial data
│   ├── cognitive/
│   │   ├── census_engine.py           # McFadden Multinomial Choice & Polling Engine
│   │   ├── ideology_matrix.py         # 81-Province Empirical Ideology Cohort Matrix
│   │   ├── living_stream_engine.py    # Live FX & RSS News Ingestion Stream
│   │   ├── micro_biography_matrix.py  # 100+ Parameter Human Nuance Tensor
│   │   ├── continuous_evolver.py      # Evolutionary Bayesian Recalibrator
│   │   ├── causal_dag_engine.py       # Judea Pearl Structural Causal DAG
│   │   ├── belief_system.py           # Jonathan Haidt 6 Moral Foundations Model
│   │   ├── interrogation_engine.py    # Socratic Qualitative Dialogue Reactor
│   │   ├── episodic_memory.py         # SQLite Persistent Agent Longitudinal Memory
│   │   └── social_graph.py            # Watts-Strogatz Small-World Network Graph
│   └── ml/
│       ├── copula_engine.py           # High-Dimensional Gaussian Copula Engine
│       └── reference_stats.py         # Empirical TÜİK, BDDK, SGK & ISCO-08 Tables
├── tests/                             # 79 Comprehensive Test Modules
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 📜 License & Author

Distributed under the **MIT License**.  
Architect & Founder: **Eren Demirer** (2026).
