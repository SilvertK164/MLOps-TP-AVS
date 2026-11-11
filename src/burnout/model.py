"""Preprocesamiento, pipeline de XGBoost y métricas."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import balanced_accuracy_score, f1_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from xgboost import XGBClassifier

from burnout.config import FEATURES, LABELS, NOMINAL, ORDINAL, SEED, XGB_N_JOBS


def build_preprocessor() -> ColumnTransformer:
    """ColumnTransformer sin ajustar, igual al que usamos con árboles en AMq1.

    - numéricas y booleana: sin tocar (los árboles no necesitan escalar)
    - ordinales: OrdinalEncoder con el orden de ``ORDINAL``
    - nominales: OneHotEncoder con las categorías fijas de ``NOMINAL``
    """
    ordinal = OrdinalEncoder(categories=[ORDINAL[c] for c in FEATURES["ordinal"]])
    nominal = OneHotEncoder(
        categories=[NOMINAL[c] for c in FEATURES["nominal"]],
        sparse_output=False,
    )
    return ColumnTransformer(
        [
            ("num", "passthrough", [*FEATURES["numeric"], *FEATURES["boolean"]]),
            ("ord", ordinal, FEATURES["ordinal"]),
            ("nom", nominal, FEATURES["nominal"]),
        ],
        verbose_feature_names_out=False,
    )


def make_pipeline(**params) -> Pipeline:
    """Pipeline preprocesador + XGBClassifier. ``params`` pisa los valores base."""
    base = {
        "objective": "multi:softprob",
        "num_class": len(LABELS),
        "eval_metric": "mlogloss",
        "tree_method": "hist",
        "random_state": SEED,
        "n_jobs": XGB_N_JOBS,
    }
    return Pipeline(
        [
            ("prep", build_preprocessor()),
            ("xgb", XGBClassifier(**{**base, **params})),
        ]
    )


def test_metrics(y_true, y_pred) -> dict[str, float]:
    """F1 macro (métrica principal), exactitud balanceada y recall por clase."""
    recalls = recall_score(y_true, y_pred, average=None, labels=range(len(LABELS)))
    out = {
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
    }
    for label, value in zip(LABELS, recalls, strict=True):
        out[f"recall_{label.lower()}"] = float(value)
    return out


def feature_importance(pipeline: Pipeline) -> pd.Series:
    """Ganancia promedio por feature, con los nombres que salen del preprocesador."""
    booster = pipeline.named_steps["xgb"].get_booster()
    gain = pd.Series(booster.get_score(importance_type="gain"))
    names = pipeline.named_steps["prep"].get_feature_names_out()
    gain.index = [names[int(k[1:])] for k in gain.index]
    return gain.sort_values(ascending=False)
