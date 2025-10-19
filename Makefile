# --- 607 targets (Polya/DP) ---
POLYA_CFG := config/polya.yaml

.PHONY: simulate
simulate:
	python -m src_cli.simulate --config $(POLYA_CFG)

.PHONY: analyze
analyze:
	python -m src_cli.analyze_polya --config $(POLYA_CFG) --t 0.25 0.5 0.75 --level 0.95

.PHONY: figures
figures:
	python -m src_cli.figures --config $(POLYA_CFG)
	python -m src_cli.figures_polya_summary
	python -m src_cli.figures_overview --config $(POLYA_CFG)
	python -m src_cli.panels_from_config --config $(POLYA_CFG)
	python -m src_cli.figures_sweep_M

.PHONY: sweepm
sweepm:
	python -m src_cli.sweep_M --config $(POLYA_CFG) --Ms 30 60 100 200

.PHONY: all
all: simulate analyze figures

.PHONY: everything
everything: clean simulate analyze sweepm analyze figures

.PHONY: test
test:
	python -m pytest -q

.PHONY: clean
clean:
	rm -rf results/raw* results/figures* results/polya_checks*.csv .pytest_cache __pycache__
