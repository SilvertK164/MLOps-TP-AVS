"""DAG de ETL: lleva el dataset crudo al Data Lake y deja listos train y test."""

from datetime import timedelta

from airflow.sdk import dag, task

DOC_MD = """
### ETL del dataset de burnout

Toma el CSV de [Impact of AI on Students](https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students)
(versionado en `data/raw/` del repo), lo sube a `s3://data/burnout/raw/`, valida el esquema y
genera el split 80/20 estratificado (semilla 42) en `s3://data/burnout/final/`.

Al final guarda `s3://data/burnout/data_info/data.json` con el esquema y registra los datasets
en MLflow (experimento *Burnout Risk*), para que cada entrenamiento sepa con qué datos se hizo.
"""

default_args = {
    "owner": "Grupo AVS",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="etl_burnout",
    description="ETL: CSV crudo → validación → split train/test en MinIO",
    doc_md=DOC_MD,
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=15),
    default_args=default_args,
    tags=["ETL", "Burnout"],
)
def etl_burnout():
    # La lógica de cada paso está en src/burnout/etl.py (testeable sin Airflow).
    @task
    def extract() -> str:
        """Sube el CSV crudo del repo al bucket ``data``."""
        from burnout import etl

        return etl.extract()

    @task
    def validate_raw(raw_uri: str) -> dict:
        """Valida el esquema del crudo; si algo no cumple, la tarea falla y el DAG se corta."""
        from burnout import etl

        return etl.validate_raw(raw_uri)

    @task
    def split(summary: dict) -> dict:
        """Genera el split 80/20 estratificado y lo guarda en ``final/``."""
        from burnout import etl

        return etl.split(summary)

    @task
    def register_dataset(summary: dict) -> None:
        """Guarda el esquema en ``data_info/data.json`` y registra el ETL en MLflow."""
        from datetime import datetime

        import mlflow

        from burnout import etl, storage
        from burnout.config import EXPERIMENT_NAME, S3_KEYS

        etl.write_data_info(summary)

        mlflow.set_experiment(EXPERIMENT_NAME)
        X_train = storage.read_csv(S3_KEYS["X_train"])
        with mlflow.start_run(run_name=f"etl_{datetime.now():%Y%m%d_%H%M%S}", tags={"stage": "etl"}):
            mlflow.log_params({k: summary[k] for k in ("rows", "train_rows", "test_rows")})
            mlflow.log_dict(summary["class_share"], "class_share.json")
            dataset = mlflow.data.from_pandas(
                X_train, source=f"s3://data/{S3_KEYS['X_train']}", name="burnout_X_train"
            )
            mlflow.log_input(dataset, context="training")

    register_dataset(split(validate_raw(extract())))


etl_burnout()
