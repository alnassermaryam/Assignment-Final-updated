.PHONY: install run eval test gate compare report
install:
	pip install -e .
run:
	python -m ai_engineering.cli --interactive
eval:
	python -m ai_engineering.eval_runner
test:
	pytest -q
gate:
	python scripts/regression_gate.py eval/summary.json
compare:
	@echo "Run scripts/run_backend.py for commercial and open_weight, then scripts/compare_backends.py on the two result files."
report:
	python -m ai_engineering.eval_runner && python scripts/regression_gate.py eval/summary.json
