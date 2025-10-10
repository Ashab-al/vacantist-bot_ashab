test:
	PYTHONPATH=. pytest --cov=app
lint:
	black . && isort . && pylint .
