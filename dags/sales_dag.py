"""
MEMBER 1 — Sales DAG
Orchestrates: extract -> clean/load (staging) -> dbt run (sales marts)

This is what you point to when asked "how is this scheduled/orchestrated?"
Runs daily at 2 AM, simulating an overnight batch load before business
hours — a standard pattern in real data engineering.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import sys
sys.path.append("/opt/airflow/data")  # where etl_sales.py lives in the container
from etl_sales import run as run_sales_etl  # noqa: E402

default_args = {
    "owner": "member_1",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sales_pipeline",
    default_args=default_args,
    description="Sales & Customer Analytics ETL + dbt run",
    schedule_interval="0 2 * * *",  # daily at 2 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["sales", "member_1"],
) as dag:

    extract_clean_load = PythonOperator(
        task_id="extract_clean_load_sales",
        python_callable=run_sales_etl,
    )

    dbt_run_sales = BashOperator(
        task_id="dbt_run_sales_models",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select sales",
    )

    extract_clean_load >> dbt_run_sales
