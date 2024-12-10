from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from refresh_game_urls import refresh_game_urls
from validate_game_numbers import validate_game_numbers
from refresh_data import refresh_data
from refresh_analysis import refresh_analysis
from validate_analysis import validate_analysis
from write_to_gsheet import write_to_gsheet

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 11, 1),
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
}

with DAG(
    "london_prem_analysis",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    catchup=False,
) as dag:
    refresh_game_urls = PythonOperator(
        task_id="refresh_game_urls", python_callable=refresh_game_urls
    )
    validate_game_numbers = PythonOperator(
        task_id="validate_game_numbers", python_callable=validate_game_numbers
    )
    refresh_data = PythonOperator(task_id="refresh_data", python_callable=refresh_data)
    refresh_analysis = PythonOperator(
        task_id="refresh_analysis", python_callable=refresh_analysis
    )
    validate_analysis = PythonOperator(
        task_id="validate_analysis", python_callable=validate_analysis
    )
    write_to_gsheet = PythonOperator(
        task_id="write_to_gsheet", python_callable=write_to_gsheet
    )

    (
        refresh_game_urls
        >> validate_game_numbers
        >> refresh_data
        >> refresh_analysis
        >> validate_analysis
        >> write_to_gsheet
    )
