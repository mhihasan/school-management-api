venv: activate_venv
activate_venv: requirements.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -U pip
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

update_pip: venv
	venv/bin/pip install -Ur requirements.txt

run_dev:
	python3 manage.py runserver 0.0.0.0:8001

open_api:
	open http://0.0.0.0:8001/swagger/