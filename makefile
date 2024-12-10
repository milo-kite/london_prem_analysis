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

docker_image:
	docker build --no-cache -t my-airflow-job:latest .

docker_init:
	docker run --rm my-airflow-job:latest db init

docker_down:
	docker-compose down

docker_up:
	docker-compose up -d

kill_webserver:
	kill -9 36504

webserver:
	docker exec -it airflow-webserver /bin/bash

scheduler:
	docker exec -it airflow-scheduler /bin/bash

deploy:
	make docker_image
	make docker_down
	make docker_up

run:
	python code/refresh_game_urls.py
	python code/validate_game_numbers.py
	python code/refresh_data.py
	python code/refresh_analysis.py
	python code/validate_analysis.py
	python code/write_to_gsheet.py
