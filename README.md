# STATS 607 — Project 2: Exchangeable Predictives under a Pólya (Dirichlet Process) Model

Reproducible code for Section 2.4 experiments (Fortini & Petrone, 2024):  
**Part A** prior/posterior (Beta) by *continuation*, **Part B** predictive diagnostics (PIT & convergence),  
**Part C** Proposition 2.6 predictive-only CIs for the **limit mass** F̃(t).

---

## Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH=.
```

## One-command runs (Make)
```bash
# Full DP/Pólya baseline: sim + analysis + panels + M-sweep
make everything

# Prior/posterior panels via continuation (Part A)
make panels-cont

# Predictive paths and diagnostics (Part B)
make predictive_paths
make partB

# Proposition 2.6 (Part C) — build coverage/width/pooled-Z figures
python -m src_cli.prop26 --config config/polya.yaml
```

### CLI snippets (if you prefer explicit commands)
```bash
# Continuation panels (posterior & optional prior)
python -m src_cli.panels_cont_from_config --config config/polya.yaml --N 2000 --M 4000 --outdir results/figures --do-prior

# Log predictive paths for n, α, t-set; then plot
python -m src_cli.log_predictive_paths --n 1000 --alpha 5 --t 0.25 0.5 0.75 --seed 2025 --base uniform
python -m src_cli.figures_predictive_paths --csv results/raw/predictive_path_n1000_a5.0_seed2025_uniform.csv --title "Predictive paths (n=1000, α=5)"

# Part B all-in-one (PIT + distances + Pm paths)
make partB
# (writes results/raw/{PIT,distances,Pm_paths}_*.csv and figures/partB_*.png)
```

## What gets written
- **results/raw/** CSVs: Pm paths, PIT sequences, convergence distances, Prop 2.6 summaries.
- **results/figures/** PNGs: prior/posterior panels, overview, bias/coverage vs M, predictive paths, Part B plots, Prop 2.6 plots.

Both folders are kept but files are git‑ignored (via `.gitignore` with `.gitkeep`).

## Tests
```bash
python -m pytest -q
```
Covers predictive updates, exchangeability properties, and CLI smoke tests.

## Structure (selected)
```
src/
  polya.py                # Pólya urn primitives (sampler, predictive, helpers)
  metrics.py              # d^∞ and RMSE on grids
  simulation.py           # drivers for generating raw streams
src_cli/
  panels_cont_from_config.py   # Part A prior/posterior by continuation
  post_continuation.py         # Single-panel posterior continuation (debug)
  log_predictive_paths.py      # Part B path logger
  figures_predictive_paths.py  # Part B path figure
  log_pit_and_distances.py     # Part B PIT + convergence logger
  figures_partB.py             # Part B figures (PIT, convergence, paths)
  prop26.py                    # Part C coverage/width/Z figures
  figures_polya_summary.py     # Part A moment checks
config/polya.yaml              # α, t, n, seeds, and base selection
Makefile                       # one-command targets
```

## Interpretation (short)
- **Part A**: Histograms line up with **Beta** overlays; mean/variance match theory; coverage near nominal.
- **Part B**: PIT ≈ Uniform; convergence curves decrease; predictive paths stabilize.
- **Part C**: Prop 2.6 CIs for F̃(t) achieve near‑nominal coverage and shrink with n; pooled Z looks ~Normal.

---

**Citation**  
Fortini, S. & Petrone, S. (2024). *Predictive inference under exchangeability.* arXiv:2402.10126.
