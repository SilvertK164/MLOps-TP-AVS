"""Entrenamiento del modelo final y registro opcional en MLflow.

Uso desde la terminal (en la raíz del repo, con el entorno activado)::

    python -m burnout.train                                   # solo entrena y evalúa
    python -m burnout.train --mlflow-uri http://localhost:5001  # además registra en MLflow
"""

import argparse

import pandas as pd
from sklearn.pipeline import Pipeline

from burnout.config import (
    BEST_PARAMS_AMQ1,
    CHAMPION_ALIAS,
    EXPERIMENT_NAME,
    REGISTERED_MODEL,
    SKOPS_TRUSTED_TYPES,
)
from burnout.data import load_raw, make_split
from burnout.model import make_pipeline, test_metrics


def train_and_evaluate(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    params: dict | None = None,
) -> tuple[Pipeline, dict[str, float]]:
    """Ajusta el pipeline con ``params`` (por defecto, los de AMq1) y lo evalúa en test."""
    pipeline = make_pipeline(**(params or BEST_PARAMS_AMQ1)).fit(X_train, y_train)
    return pipeline, test_metrics(y_test, pipeline.predict(X_test))


def log_and_register(
    pipeline: Pipeline,
    metrics: dict[str, float],
    params: dict,
    X_example: pd.DataFrame,
    tracking_uri: str,
    run_name: str = "final_model",
) -> str:
    """Registra el modelo en MLflow y le pone el alias ``champion``.

    :return: número de versión registrada.
    """
    import mlflow
    from mlflow.models import infer_signature

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run(run_name=run_name, tags={"stage": "final"}):
        mlflow.log_params(params)
        mlflow.log_metrics({f"test_{k}": v for k, v in metrics.items()})
        signature = infer_signature(X_example, pipeline.predict(X_example))
        info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="model",
            signature=signature,
            input_example=X_example.head(3),
            registered_model_name=REGISTERED_MODEL,
            skops_trusted_types=SKOPS_TRUSTED_TYPES,
        )
    version = str(info.registered_model_version)
    mlflow.MlflowClient().set_registered_model_alias(REGISTERED_MODEL, CHAMPION_ALIAS, version)
    return version


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mlflow-uri", help="URI del servidor de MLflow (opcional)")
    args = parser.parse_args()

    X_train, X_test, y_train, y_test = make_split(load_raw())
    pipeline, metrics = train_and_evaluate(X_train, y_train, X_test, y_test)
    for name, value in metrics.items():
        print(f"{name:>18}: {value:.4f}")

    if args.mlflow_uri:
        version = log_and_register(pipeline, metrics, BEST_PARAMS_AMQ1, X_train, args.mlflow_uri)
        print(f"Registrado {REGISTERED_MODEL} v{version} con alias '{CHAMPION_ALIAS}'")


if __name__ == "__main__":
    main()
