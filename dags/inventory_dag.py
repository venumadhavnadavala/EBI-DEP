"""
MEMBER 2 — Inventory DAG
Same orchestration pattern as sales_dag.py, different domain.
Runs daily at 3 AM — staggered after sales so both don't hit
the warehouse at once (a real consideration in shared infra).
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import sys

sys.path.append("/opt/airflow/data")
from etl_inventory import run as run_inventory_etl  # noqa: E402


default_args = {
    "owner": "member_2",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="inventory_pipeline",
    default_args=default_args,
    description="Product & Inventory Analytics ETL + dbt run",
    schedule_interval="0 3 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["inventory", "member_2"],
) as dag:

    extract_clean_load = PythonOperator(
        task_id="extract_clean_load_inventory",
        python_callable=run_inventory_etl,
    )

    dbt_run_inventory = BashOperator(
        task_id="dbt_run_inventory_models",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select inventory",
    )

    # Run dbt only after the inventory data has been loaded successfully.
    extract_clean_load >> dbt_run_inventory