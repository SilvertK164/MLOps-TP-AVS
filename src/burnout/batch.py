"""Predicción por lotes. El DAG ``batch_predict_burnout`` usa estas funciones."""

import pandas as pd

from burnout.config import ID_COL, LABELS
from burnout.data import decode_target, select_features


def predict_batch(model, batch: pd.DataFrame) -> pd.DataFrame:
    """Aplica el modelo a un lote de estudiantes.

    :param model: pipeline entrenado (preprocesador + XGBoost), p. ej. el champion de MLflow.
    :param batch: una fila por estudiante, con ``Student_ID`` y las features (las columnas que
        sobren se ignoran).
    :return: ``Student_ID``, la probabilidad de cada clase y la clase predicha.
    """
    X = select_features(batch)
    proba = pd.DataFrame(model.predict_proba(X), columns=[f"proba_{label}" for label in LABELS]).round(4)
    out = pd.concat([batch[[ID_COL]].reset_index(drop=True), proba], axis=1)
    out["Burnout_Risk_Pred"] = decode_target(model.predict(X))
    return out
