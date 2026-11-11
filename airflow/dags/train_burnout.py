"""DAG de entrenamiento: entrena el modelo final y lo registra como champion en MLflow."""

from datetime import timedelta

from airflow.sdk import dag, task

DOC_MD = """
### Entrenamiento del modelo de burnout

1. Busca en MLflow la mejor prueba de la búsqueda de hiperparámetros (runs con
   `tags.stage = 'optuna'`, ver `notebooks/experimento_mlflow_optuna.ipynb`). Si todavía no se
   corrió esa búsqueda, usa los hiperparámetros que encontramos en AMq1.
2. Entrena el pipeline (preprocesador + XGBoost) con `s3://data/burnout/final/train/`.
3. Lo evalúa en test (F1 macro) y lo registra como `burnout_model_prod` con alias `champion`.

Requiere haber corrido antes el DAG `etl_burnout`.
"""

default_args = {
    "owner": "Grupo AVS",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="train_burnout",
    description="Entrena XGBoost con los mejores hiperparámetros y lo registra como champion",
    doc_md=DOC_MD,
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=30),
    default_args=default_args,
    tags=["Train", "Burnout"],
)
def train_burnout():
    @task
    def best_params() -> dict:
        """Hiperparámetros de la mejor prueba de Optuna en MLflow (o los de AMq1)."""
        import mlflow

        from burnout.config import BEST_PARAMS_AMQ1, EXPERIMENT_NAME

        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if experiment is None:
            return {"params": BEST_PARAMS_AMQ1, "source": "amq1"}
        runs = mlflow.search_runs(
            [experiment.experiment_id],
            filter_string="tags.stage = 'optuna'",
            order_by=["metrics.cv_f1_macro DESC"],
            max_results=1,
        )
        if runs.empty:
            return {"params": BEST_PARAMS_AMQ1, "source": "amq1"}
        # MLflow guarda los parámetros como texto: se recuperan con el tipo de AMq1.
        best = runs.iloc[0]
        params = {k: type(v)(best[f"params.{k}"]) for k, v in BEST_PARAMS_AMQ1.items()}
        return {"params": params, "source": f"run {best['run_id']}"}

    @task
    def train_and_register(choice: dict) -> str:
        """Entrena, evalúa en test y registra la nueva versión como champion."""
        import os

        from burnout import storage
        from burnout.config import S3_KEYS
        from burnout.train import log_and_register, train_and_evaluate

        X_train = storage.read_csv(S3_KEYS["X_train"])
        y_train = storage.read_csv(S3_KEYS["y_train"]).squeeze("columns")
        X_test = storage.read_csv(S3_KEYS["X_test"])
        y_test = storage.read_csv(S3_KEYS["y_test"]).squeeze("columns")

        pipeline, metrics = train_and_evaluate(X_train, y_train, X_test, y_test, choice["params"])
        print(f"Hiperparámetros: {choice['source']} → F1 macro test = {metrics['f1_macro']:.4f}")
        return log_and_register(
            pipeline,
            metrics,
            choice["params"],
            X_train,
            tracking_uri=os.environ["MLFLOW_TRACKING_URI"],
            run_name="train_dag",
        )

    train_and_register(best_params())


train_burnout()
