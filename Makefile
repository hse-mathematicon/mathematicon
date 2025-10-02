.PHONY: lint format start-app migration

lint:
	poetry run ruff check app tests
	poetry run mypy app tests

format:
	poetry run ruff format app tests
	poetry run ruff check app tests --fix


start-app:
	poetry run python main.py
