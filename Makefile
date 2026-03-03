# Trinity Protocol Makefile

.PHONY: train submit test clean

train:
	@echo "Starting Trinity Phase: Thesis (Baseline)"
	@# Run the baseline training notebook as a script
	@jupyter nbconvert --to script telco_churn_baseline.ipynb
	@python telco_churn_baseline.py
	@rm telco_churn_baseline.py

usisivac-v5:
	@echo "Launching Usisivac V5: Multi-Agent Intelligence Pipeline"
	@python3 Usisivac/src/orchestrator.py

submit:
	@echo "Gate Verification..."
	@python -c "import json; print(json.load(open('manifest.json')))"
	@kaggle kernels push -p .

test:
	@echo "Running Guardian Validation..."
	@python Usisivac/src/review.py . --recursive

clean:
	rm -rf __pycache__ .pytest_cache
