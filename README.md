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


## Baseline config
Uses `config/baseline.yaml` (Normal(0,1), n={1000,5000}, reps=10, J=100).

## How to run
make all   # simulate → analyze → figures
make test  # run pytest

## Pólya / DP baseline
- Config: `config/polya.yaml` (base=uniform, n list, reps=M).
- Run all: `make all`  # simulate → analyze → figures
- Examples:
    - Single-t: `PYTHONPATH=. python examples/polya_single_t.py --t 0.5 --alpha 5 --n 100 --reps 3000 --base uniform`
    - Panels:   `PYTHONPATH=. python examples/polya_panel.py --base uniform --ts 0.25 0.5 0.75 --alphas 1 5 20 --ns 100 500 1000 --reps 4000`
- Outputs:
    - `results/polya_checks.csv` (mean/var vs theory, coverage)
    - `results/figures/` (convergence, PIT, summary, panels)
