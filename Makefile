test:
	PYTHONPATH=. pytest .
lint:
	-isort .
	-black .
	-pylint .
	-flake8 .
dev:
	docker compose -f develop.yml up
prod:
	docker compose -f production.yml up -d