# Project 2 — Exchangeable Predictives (Pólya / Dirichlet Process)

This project refactors the original exploratory code into a clear, **installable**, **tested**, and
**one-command** pipeline that reproduces the DP/Pólya baseline (Setting 1): sequential predictives,
PIT calibration, convergence diagnostics, prior/posterior Beta panels, coverage, and M-sensitivity.

**Goal:** frictionless reproducibility — clone, install, run one command, get the same outputs.

---

## What’s in this repo

- `config/` — experiment configs
  - `polya.yaml` — Setting 1 (DP/Pólya with Uniform base)
- `src/` — library code
  - `dgps.py` — truths (Uniform/Normal), sampling and CDF/PDF helpers
  - `methods.py` — `PolyaPredictive` (Blackwell–MacQueen Pólya urn)
  - `metrics.py` — distances (d∞, RMSE), grids, PIT helpers
  - `simulation.py` — stream runner (sequential predictive experiment)
- `src_cli/` — command-line entry points
  - `simulate.py` — run raw Monte Carlo streams to Parquet
  - `analyze_polya.py` — Beta moments, coverage, summaries → CSV
  - `figures.py` — convergence (d∞/RMSE) + PIT per \(n\)
  - `figures_polya_summary.py` — mean/variance vs theory + coverage
  - `figures_overview.py` — single panel with d∞, RMSE, PIT
  - `sweep_M.py` — sweep Monte Carlo reps \(M\) and save per-M CSVs
  - `figures_sweep_M.py` — bias & coverage vs \(M\)
  - `panels_from_config.py` — prior/posterior panels wrapper
- `examples/` — panel script
  - `polya_panel.py` — prior/posterior Beta overlays (by \(t,\alpha,n\))
- `tests/` — pytest suite (sanity, exchangeability, reproducibility)
- `results/` — outputs (git-ignored except `.gitkeep`)
  - `raw/` — Parquet runs
  - `figures/` — PNG figures
- `README.md` — this file
- `ADEMP.md` — design summary
- `ANALYSIS.md` — short narrative findings

> Note: large/derived artifacts under `results/` are **not** tracked by git.

---

## Environment & install

> Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
```

---

## Run the full pipeline (one command)

```bash
make everything
```

This runs:
- **simulate** → DP/Pólya streams per `config/polya.yaml`
- **analyze** → `results/polya_checks.csv`
- **sweepm** → per-M CSVs `results/polya_checks_M*.csv`
- **figures** → all figures into `results/figures/`

### Expected outputs (written to `results/figures/`)

- `overview_polya_dp.png` — panel: \(d^{(\infty)}\), RMSE, PIT  
- `polya_prior_panels_n{N}.png`, `polya_posterior_panels_n{N}.png` — Beta overlays  
- `polya_mean_emp_vs_theory.png`, `polya_var_emp_vs_theory.png` — moments vs theory  
- `polya_coverage.png` — 95% equal-tailed coverage  
- `polya_bias_vs_M.png`, `polya_coverage_vs_M.png` — sensitivity to \(M\)

---

## Makefile targets

```bash
make simulate    # raw runs → results/raw/
make analyze     # summaries → results/polya_checks.csv
make sweepm      # run M ∈ {30,60,100,200} → results/polya_checks_M*.csv
make figures     # all plots (overview, panels, summaries, M-sweep)
make test        # pytest -q
make clean       # clear results/* (keeps .gitkeep)
```

---

## Testing

```bash
python -m pytest -q
```

Covers:
- Truth sampling & CDF (Uniform)
- Pólya predictive update & PIT shape
- Reproducibility of raw outputs (fixed RNG)

---

## Project structure

```text
.
├── config/
│   └── polya.yaml
├── examples/
│   └── polya_panel.py
├── results/
│   ├── figures/         # PNGs (git-ignored; .gitkeep tracked)
│   └── raw/             # Parquet runs (git-ignored; .gitkeep tracked)
├── src/
│   ├── dgps.py
│   ├── methods.py
│   ├── metrics.py
│   └── simulation.py
├── src_cli/
│   ├── simulate.py
│   ├── analyze_polya.py
│   ├── figures.py
│   ├── figures_polya_summary.py
│   ├── figures_overview.py
│   ├── sweep_M.py
│   ├── figures_sweep_M.py
│   └── panels_from_config.py
├── tests/
│   ├── test_dgp.py
│   ├── test_exchangeability.py
│   └── test_repro.py
├── README.md
├── ADEMP.md
├── ANALYSIS.md
├── requirements.txt
├── Makefile
└── .gitignore
```

---

## Troubleshooting

- **`No module named numpy/pandas`** → activate the venv before running: `source .venv/bin/activate`.  
- **Missing figures** → ensure `make analyze` produced `results/polya_checks.csv` (then `make figures`).  
- **Panels missing** → `examples/` must be a package; we include `examples/__init__.py`.  
- **Slow when \(M\) large** → reduce `--Ms` in `make sweepm` or edit `src_cli/sweep_M.py`.
