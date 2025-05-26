.PHONE: pre-commit
pre-commit:
	pre-commit install

.PHONE: test
test:
	pytest -s -v
