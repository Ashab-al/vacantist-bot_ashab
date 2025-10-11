test:
	PYTHONPATH=. pytest .
lint:
	-isort .
	-black .
	-pylint .
	-flake8 .
