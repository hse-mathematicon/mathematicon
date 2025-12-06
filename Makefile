.PHONY: lint format start-app migration migrate-up

lint:
	poetry run ruff check app tests
	poetry run mypy app tests

format:
	poetry run ruff format app tests
	poetry run ruff check app tests --fix


start-app:
	poetry run python main.py


migration:
	poetry run alembic -c migrations/alembic.ini revision --autogenerate -m "$(message)"

migrate-up:
	poetry run alembic -c migrations/alembic.ini upgrade head

migrate-down:
	poetry run alembic -c migrations/alembic.ini downgrade -1
