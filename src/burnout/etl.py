"""Pasos del ETL. El DAG ``etl_burnout`` llama a estas funciones desde sus tareas.

Viven acá (y no dentro del DAG) para poder testearlas sin Airflow: ver ``tests/test_etl.py``.
Cada paso recibe y devuelve valores chicos (que en Airflow viajan por XCom); los datos grandes
se leen y escriben en el Data Lake.
"""

from datetime import datetime

import pandas as pd

from burnout import storage
from burnout.config import DATA_RAW, FEATURES, LABELS, NOMINAL, ORDINAL, S3_KEYS, TARGET_COL
from burnout.data import make_split, validate


def extract() -> str:
    """Sube el CSV crudo versionado en el repo al Data Lake y devuelve su URI."""
    return storage.write_csv(pd.read_csv(DATA_RAW), S3_KEYS["raw"])


def validate_raw(raw_uri: str) -> dict:
    """Valida el esquema del crudo y devuelve un resumen.

    :raises ValueError: si el esquema no cumple; en Airflow la tarea falla y el DAG se corta.
    """
    df = validate(storage.read_csv(S3_KEYS["raw"]))
    return {
        "source": raw_uri,
        "rows": len(df),
        "class_share": df[TARGET_COL].value_counts(normalize=True).round(4).to_dict(),
    }


def split(summary: dict) -> dict:
    """Genera el split 80/20 estratificado y guarda X/y de train y test en ``final/``."""
    df = validate(storage.read_csv(S3_KEYS["raw"]))
    X_train, X_test, y_train, y_test = make_split(df)
    frames = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train.to_frame(),
        "y_test": y_test.to_frame(),
    }
    for name, frame in frames.items():
        storage.write_csv(frame, S3_KEYS[name])
    return {**summary, "train_rows": len(X_train), "test_rows": len(X_test)}


def write_data_info(summary: dict) -> str:
    """Guarda en ``data_info/data.json`` el esquema que necesita quien use el modelo (p. ej. la API)."""
    info = {
        "features": FEATURES,
        "ordinal_categories": {c: ORDINAL[c] for c in FEATURES["ordinal"]},
        "nominal_categories": NOMINAL,
        "target_col": TARGET_COL,
        "labels": LABELS,
        **summary,
        "date": datetime.now().isoformat(timespec="seconds"),
    }
    return storage.write_json(info, S3_KEYS["data_info"])
