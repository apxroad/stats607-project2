# STATS 607 Project 2 — Simulation Study
Baseline-first pipeline for predictive evaluation (PIT, distances, coverage).

## Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Make targets
make simulate   # run baseline sims (stub)
make analyze    # aggregate results (stub)
make figures    # plots (stub)
make test       # pytest
make all        # simulate → analyze → figures
