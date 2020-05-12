

venv: activate_venv
activate_venv: requirements/dev.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -U pip
	venv/bin/pip install -Ur requirements/dev.txt
	touch venv/bin/activate

install_pip: venv
	venv/bin/pip install -Ur requirements/dev.txt
	pre-commit install

open_api:
	open http://0.0.0.0:8001/swagger/

run_dev:
	docker-compose -f dev.yml up --build

run_prod:
	docker-compose -f prod.yml up -d --build

stop_dev:
	docker-compose -f dev.yml down

stop_prod:
	docker-compose -f prod.yml down

migrate_db:
	docker-compose -f prod.yml run web python3 manage.py migrate

start_pg:
	docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres:12.2
