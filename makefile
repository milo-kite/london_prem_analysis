VENV_NAME = hockey_venv

pyenv:
	pyenv virtualenv 3.12.6 ${VENV_NAME}

requirements:
	pip install -r requirements.txt

airflow_ui:
	open http://localhost:8080

deploy_dag:
	make format
	make lint
	mkdir -p ~/airflow/dags/models
	cp code/dag.py ~/airflow/dags/
	cp code/config.py ~/airflow/dags/
	cp code/models/* ~/airflow/dags/models/
	cp credentials/* ~/airflow/dags/models

format:
	black code/ credentials/

lint: 
	flake8 code/