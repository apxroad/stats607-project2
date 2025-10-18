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
