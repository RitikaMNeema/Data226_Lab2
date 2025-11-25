from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

DBT_PROJECT_DIR = "/opt/airflow/dags/dbt"
DBT_PROFILES_DIR = "/opt/airflow/dags/dbt"
ETL_SCRIPT = "/opt/airflow/dags/yfinance_etl.py"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="lab2_stock_pipeline",
    description="Lab-2: Lab1 ETL → dbt (staging → intermediate → mart) → ready for BI",
    default_args=default_args,
    start_date=datetime(2025, 11, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["data226", "stocks", "dbt", "snowflake", "elt"],
) as dag:

    start = EmptyOperator(task_id="start")

    run_etl = BashOperator(
        task_id="etl_raw_prices",
        bash_command=f"python {ETL_SCRIPT}",
        env={},
        append_env=True,
        do_xcom_push=False,
    )

    dbt_env = {
        "DBT_PROFILES_DIR": DBT_PROFILES_DIR,
    }

    print_env = BashOperator(
        task_id="debug_dbt_env",
        bash_command=f'echo "DBT project dir: {DBT_PROJECT_DIR}"',
    )

    dbt_deps = BashOperator(
    task_id="dbt_install_dependencies",
    bash_command=(
        f"dbt deps "
        f"--profiles-dir {DBT_PROFILES_DIR} "
        f"--project-dir {DBT_PROJECT_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)

dbt_stg_stock_data = BashOperator(
    task_id="stg_stock_data",
    bash_command=(
        f"dbt run "
        f"--select stg_stock_data --full-refresh -v "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)

dbt_run = BashOperator(
    task_id="dbt_run_transformations",
    bash_command=(
        f"dbt run -v "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)

dbt_test = BashOperator(
    task_id="dbt_test_data_quality",
    bash_command=(
        f"dbt test -v "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)

dbt_snapshot = BashOperator(
    task_id="dbt_snapshot_history",
    bash_command=(
        f"dbt snapshot -v "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)

dbt_docs_generate = BashOperator(
    task_id="dbt_docs_generate",
    bash_command=(
        f"dbt docs generate -v "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR}"
    ),
    append_env=True,
    do_xcom_push=False,
)



run_etl >> print_env >> dbt_deps >> dbt_stg_stock_data >> dbt_run >> dbt_test >> dbt_snapshot >> dbt_docs_generate
