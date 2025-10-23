test:
	PYTHONPATH=. pytest .
lint:
	-isort .
	-black .
	-pylint .
	-flake8 .
lintci:
	pylint app --ignore=venv,tests,migration
dev:
	docker compose -f develop.yml up
prod:
	docker compose -f production.yml up --build -d