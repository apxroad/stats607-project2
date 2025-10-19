.PHONY: all simulate analyze figures test clean

CONFIG := config/baseline.yaml

all: simulate analyze figures

simulate:
	python -m src_cli.simulate --config $(CONFIG)

analyze:
	python -m src_cli.analyze --config $(CONFIG)

figures:
	python -m src_cli.figures --config $(CONFIG)

test:
	pytest -q

clean:
	rm -rf results/raw/* results/figures/* results/*.csv
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

.PHONY: examples
examples:
	PYTHONPATH=. python examples/polya_single_t.py --t 0.5 --alpha 5 --n 100 --reps 3000 --base uniform
	PYTHONPATH=. python examples/polya_panel.py --base uniform --ts 0.25 0.5 0.75 --alphas 1 5 20 --ns 100 500 1000 --reps 4000

.PHONY: all
all: simulate analyze figures

.PHONY: test
test:
	pytest -q

.PHONY: clean
clean:
	rm -rf results/raw/* results/figures/* .pytest_cache __pycache__
