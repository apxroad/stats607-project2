.PHONY: all simulate analyze figures test clean

all: simulate analyze figures

simulate:
	@python -m src_cli.simulate --config config/baseline.yaml || echo "TODO: implement simulate"

analyze:
	@python -m src_cli.analyze --config config/baseline.yaml || echo "TODO: implement analyze"

figures:
	@python -m src_cli.figures --config config/baseline.yaml || echo "TODO: implement figures"

test:
	pytest -q

clean:
	rm -rf results/raw/* results/figures/* figures/*
