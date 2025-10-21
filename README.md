# Stats 607 — Project 2 (Polya/DP)

This repository contains a **reproducible pipeline** for three tasks:
- **Part A**: prior/posterior panels for Polya sequence predictive CDFs,
- **Part B**: convergence diagnostics (grid distances) and **predictive paths**,
- **Part C**: Proposition 2.6 **pooled Z** check.

All figures are saved to `results/figures` as **PNG**, and (where appropriate) as **PDF** for print‑quality.

---

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Full pipeline: clean → simulate → analyze → figures
make all
```

Useful single steps:

```bash
make partA-prior   # Part A prior panel (n=0)
make partA         # Part A posterior panels (n=100, 500, 1000)
make partB         # Part B logs + figures (convergence & predictive paths)
make partC         # Part C logs + pooled‑Z figure

make simulate      # just raw logs (Part B + Part C)
make analyze       # summaries → results/summary/
make figures       # all figures (A/B/C) from existing logs

make clean         # remove generated files
make test          # run pytest
make help          # list targets
```

You can override defaults at invocation time:

```bash
make all BASE=normal ALPHA=10 SEED=7
```

Default knobs: `BASE=uniform`, `ALPHA=5.0`, `SEED=2025`, thresholds `T=0.25 0.5 0.75`.

---

## Outputs

**Raw logs** (`results/raw/`)
- `distances_partB_n<N>_a<ALPHA>_seed<SEED>_<BASE>.csv` — grid‑based distances vs stream index.
- `Pm_paths_partB_n<N>_a<ALPHA>_seed<SEED>_<BASE>.csv` — predictive path values `P_m(t)`.
- `prop26_M400_L50000_a<ALPHA>_seed<SEED>_<BASE>.csv` — pooled‑Z inputs across `n ∈ {100,500,1000}`.

**Summaries** (`results/summary/`)
- `prop26_summary.csv` — coverage & mean width by `(n, t)`.
- `partB_distances_summary.csv` — mean/min/max for `d^{(∞)}` and RMSE (if distances CSV present).

**Figures** (`results/figures/`)
- Part A: `post_panels_cont_n{0,100,500,1000}_M4000_N2000_<base>.png` (prior/posterior panels).
- Part B: `partB_convergence_<stem>.(png|pdf)`, `partB_paths_<stem>.(png|pdf)`.
- Part C: `prop26_zcheck_<stem>.(png|pdf)` (histogram overlaid with `N(0,1)` density).

> PDF export is enabled for all Part B/C figures and used in Part A wherever safe. Rendering uses the project style in `src/plotstyle.py` (set via `apply_plot_style()` in each CLI).

---

## Repository structure (annotated)

```
.
├─ config/                      # optional configuration/snippets for experiments
├─ examples/                    # example notebooks or small demo scripts (optional)
├─ figures/                     # (optional) manually curated figures
├─ results/
│  ├─ raw/                      # raw CSV logs written by CLI "log_*" scripts
│  ├─ figures/                  # auto‑generated figures (PNG/PDF)
│  └─ summary/                  # tidy CSV summaries created by `make analyze`
├─ scripts/                     # helper shell/python scripts (not required by pipeline)
├─ src/                         # core library code (importable as `src.*`)
│  ├─ dgps.py                   # data‑generating processes (Uniform, Normal, …)
│  ├─ interfaces.py             # minimal protocol/typing helpers
│  ├─ methods.py                # Polya predictive implementation wrappers
│  ├─ metrics.py                # grids, distances (d_infty, RMSE), helpers
│  ├─ plotstyle.py              # `apply_plot_style()` for research‑quality plots
│  ├─ polya.py                  # Polya sequence model utilities
│  └─ simulation.py             # simulation helpers used by CLIs/tests
├─ src_cli/                     # command‑line entry points (callable via `python -m ...`)
│  ├─ analyze.py                # aggregates raw → summary CSVs
│  ├─ parta_panels.py           # generate Part A panels for n in {0,100,500,1000}
│  ├─ partb_log_convergence.py  # log Part B distances + Pm paths
│  ├─ partb_figures.py          # render Part B figures from logs
│  ├─ partc_log_prop26.py       # log data for Proposition 2.6 pooled‑Z
│  └─ partc_figures_prop26.py   # plot pooled‑Z histogram + N(0,1) overlay
├─ tests/                       # pytest suite
│  ├─ conftest.py
│  ├─ test_dgp.py               # DGP sanity checks
│  ├─ test_exchangeability.py   # basic exchangeability/symmetry checks
│  ├─ test_polya_module.py      # Polya utilities
│  ├─ test_repro.py             # reproducibility (seeded runs)
│  ├─ test_smoke_parta.py       # smoke test Part A CLIs
│  ├─ test_smoke_partb.py       # smoke test Part B CLIs
│  └─ test_smoke_partc.py       # smoke test Part C CLIs
├─ Makefile                     # orchestration: all / simulate / analyze / figures / clean / test
├─ README.md
├─ requirements.txt             # Python dependencies
└─ pytest.ini                   # pytest defaults
```

---

## Command‑line interfaces (CLIs)

### Part A — Panels
```bash
python -m src_cli.parta_panels   --base uniform --t 0.25 0.5 0.75 --alpha 1 5 20   --n {0,100,500,1000} --M 4000 --N 2000 --seed 2025
```

### Part B — Convergence + Predictive Paths 
```bash
python -m src_cli.partb_log_convergence   --n 1000 --alpha 5.0 --t 0.25 0.5 0.75 --seed 2025 --base uniform

python -m src_cli.partb_figures   --stem partB_n1000_a5.0_seed2025_uniform   --title "n=1000, α=5.0, base=uniform"
```

### Part C — Proposition 2.6 
```bash
python -m src_cli.partc_log_prop26   --alpha 5.0 --t 0.25 0.5 0.75 --n 100 500 1000 --M 400 --seed 2025 --base uniform

python -m src_cli.partc_figures_prop26   --csv results/raw/prop26_M400_L50000_a5.0_seed2025_uniform.csv   --title "Proposition 2.6: α=5.0, base=uniform"
```

### Analyze (summaries)
```bash
python -m src_cli.analyze   --raw results/raw --summary results/summary   --alpha 5.0 --seed 2025 --base uniform   --stem partB_n1000_a5.0_seed2025_uniform
```

---

## Notes on reproducibility and style

- All CLIs accept `--seed`; the Makefile uses `SEED=2025` by default.
- Plotting calls `apply_plot_style()` which sets readable fonts, tight bounding boxes, and PDF‑friendly rcParams (TrueType embedding).
- Figures are deterministic given the seed and parameters.