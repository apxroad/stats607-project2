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

.PHONY: clean
clean:
	rm -rf results/raw* results/figures* results/polya_checks*.csv .pytest_cache __pycache__
	mkdir -p results/raw results/figures

.PHONY: partA-prior
partA-prior:
	# Prior-by-continuation panels (n=0)
	python -m src_cli.panels_cont_from_config \
	  --base uniform \
	  --t 0.25 0.5 0.75 \
	  --alpha 1 5 20 \
	  --n 0 \
	  --M 4000 \
	  --N 2000 \
	  --seed 2025

.PHONY: partA
partA:
	# Prior & posterior panels via continuation (matching provided logic)
	python -m src_cli.panels_cont_from_config \
	  --base uniform \
	  --t 0.25 0.5 0.75 \
	  --alpha 1 5 20 \
	  --n 100 \
	  --M 4000 \
	  --N 2000 \
	  --seed 2025
	python -m src_cli.panels_cont_from_config \
	  --base uniform \
	  --t 0.25 0.5 0.75 \
	  --alpha 1 5 20 \
	  --n 500 \
	  --M 4000 \
	  --N 2000 \
	  --seed 2025
	python -m src_cli.panels_cont_from_config \
	  --base uniform \
	  --t 0.25 0.5 0.75 \
	  --alpha 1 5 20 \
	  --n 1000 \
	  --M 4000 \
	  --N 2000 \
	  --seed 2025

.PHONY: partB
partB:
	# Log PIT + convergence distances + P_m(t) paths
	python -m src_cli.log_pit_and_distances \
	  --n 1000 --alpha 5 --t 0.25 0.5 0.75 --seed 2025 --base uniform
	# Build the three Part-B figures (PIT, convergence, P_m paths)
	python -m src_cli.figures_partB \
	  --stem partB_n1000_a5.0_seed2025_uniform \
	  --title "n=1000, α=5, base=uniform"

.PHONY: partC
partC:
	# Proposition 2.6 simulation: coverage/width/pooled Z
	python -m src_cli.log_prop26 \
	  --alpha 5 \
	  --t 0.25 0.5 0.75 \
	  --n 100 500 1000 \
	  --M 400 \
	  --seed 2025 \
	  --base uniform
	python -m src_cli.figures_prop26 \
	  --csv results/raw/prop26_M400_L50000_a5.0_seed2025_uniform.csv \
	  --title "Proposition 2.6: α=5, base=uniform"

.PHONY: everything
everything: clean partA-prior partA partB partC
