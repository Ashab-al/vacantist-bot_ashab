test:
	PYTHONPATH=. pytest .
lint:
	-isort .
	-black .
	-pylint .
	-flake8 .
lintci:
	pylint .
dev:
	docker compose -f develop.yml up
prod:
	docker compose -f production.yml up --build -d