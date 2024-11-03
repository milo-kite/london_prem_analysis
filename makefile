VENV_NAME = hockey_venv

create_venv:
	python3 -m venv $(VENV_NAME)

activate:
	@echo "Run 'source $(VENV_NAME)/bin/activate' to activate the virtual environment"

requirements:
	$(VENV_NAME)/bin/pip install -r requirements.txt

run:
	python3 code/london_prem_analysis.py

airflow_ui:
	open http://localhost:8080

deploy_dag:
	mkdir -p ~/airflow/dags/models
	cp code/dag.py ~/airflow/dags/
	cp code/config.py ~/airflow/dags/
	cp code/models/* ~/airflow/dags/models/
	cp credentials/* ~/airflow/dags/models