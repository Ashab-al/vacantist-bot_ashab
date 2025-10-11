test:
	PYTHONPATH=. pytest .
lint:
	-black . 
	-isort . 
	-pylint . 
	-flake8 .
