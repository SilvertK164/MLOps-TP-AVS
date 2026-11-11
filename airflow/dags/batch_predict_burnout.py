"""DAG de predicción por lotes (clase 5): aplica el champion a un lote de estudiantes."""

from datetime import datetime, timedelta

from airflow.sdk import Variable, dag, task

DOC_MD = """
### Predicción por lotes del riesgo de burnout

Simula el caso de la clase 5: todos los días llega un lote de estudiantes y precalculamos su
riesgo de burnout para que otro sistema lo consulte sin esperar al modelo.

1. Arma el lote: si existe `s3://data/burnout/batch/input.csv` lo usa; si no, toma una muestra
   del test (tamaño en la variable de Airflow `burnout_batch_size`).
2. Carga `models:/burnout_model_prod@champion` desde MLflow.
3. Guarda en `s3://data/burnout/batch/predictions.csv` la clase predicha y la probabilidad de
   cada clase por `Student_ID`.

Requiere haber corrido antes `etl_burnout` y `train_burnout`.
"""

default_args = {
    "owner": "Grupo AVS",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="batch_predict_burnout",
    description="Predicción por lotes con el modelo champion",
    doc_md=DOC_MD,
    schedule="@daily",
    start_date=datetime(2026, 11, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=15),
    default_args=default_args,
    tags=["Batch", "Burnout"],
)
def batch_predict_burnout():
    @task
    def build_batch() -> int:
        """Deja el lote de entrada en ``batch/input.csv`` y devuelve su tamaño."""
        from botocore.exceptions import ClientError

        from burnout import storage
        from burnout.config import OUTCOMES, S3_KEYS

        try:
            batch = storage.read_csv(S3_KEYS["batch_input"])
        except ClientError:
            # Simulamos estudiantes nuevos: sin las variables que se miden a fin de semestre.
            size = int(Variable.get("burnout_batch_size", default=500))
            batch = storage.read_csv(S3_KEYS["raw"]).sample(size).drop(columns=OUTCOMES)
            storage.write_csv(batch, S3_KEYS["batch_input"])
        return len(batch)

    @task
    def predict(batch_size: int) -> str:
        """Predice con el champion y guarda clase y probabilidades por estudiante."""
        import mlflow

        from burnout import storage
        from burnout.batch import predict_batch
        from burnout.config import CHAMPION_ALIAS, REGISTERED_MODEL, S3_KEYS

        batch = storage.read_csv(S3_KEYS["batch_input"])
        model = mlflow.sklearn.load_model(f"models:/{REGISTERED_MODEL}@{CHAMPION_ALIAS}")
        out = predict_batch(model, batch)
        print(f"{batch_size} estudiantes:\n{out['Burnout_Risk_Pred'].value_counts()}")
        return storage.write_csv(out, S3_KEYS["batch_output"])

    predict(build_batch())


batch_predict_burnout()
