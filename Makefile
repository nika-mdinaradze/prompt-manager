.PHONY: migrations
.PHONY: tests

build:
	@echo "Building development server docker"
	docker-compose build

run:
	@echo "starting API development server docker"
	docker-compose up

get_requirements:
	@echo "getting requirements"
	docker-compose run --rm web pip list

migrations:
	@echo "making migrations"
	docker-compose run --rm web alembic revision --autogenerate -m "$(name)"

upgrade:
	@echo "upgrading"
	docker-compose run --rm web alembic upgrade head

test:
	@echo "running tests..."
	docker-compose run --rm web sh -c "pytest"
