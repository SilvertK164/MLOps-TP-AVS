"""Carga, validación y split del dataset."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from burnout.config import (
    BOOLEAN,
    DATA_RAW,
    EXPECTED_COLUMNS,
    FEATURE_COLUMNS,
    LABELS,
    NOMINAL,
    NUMERIC,
    ORDINAL,
    SEED,
    TARGET_COL,
    TEST_SIZE,
)


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Valida el esquema y devuelve una copia con las categorías tipadas.

    :param df: dataset crudo, tal como sale del CSV.
    :return: copia con columnas ordinales y nominales como ``pd.Categorical``.
    :raises ValueError: si faltan o sobran columnas, hay nulos, una columna no tiene
        el tipo esperado o aparece una categoría desconocida.
    """
    missing = EXPECTED_COLUMNS - set(df.columns)
    extra = set(df.columns) - EXPECTED_COLUMNS
    if missing or extra:
        raise ValueError(f"Columnas inesperadas. Faltan: {sorted(missing)}; sobran: {sorted(extra)}")

    null_cols = df.columns[df.isna().any()].tolist()
    if null_cols:
        raise ValueError(f"Hay valores nulos en: {null_cols}")

    non_numeric = [c for c in NUMERIC if not pd.api.types.is_numeric_dtype(df[c])]
    if non_numeric:
        raise ValueError(f"Deberían ser numéricas: {non_numeric}")

    for col in BOOLEAN:
        if not pd.api.types.is_bool_dtype(df[col]):
            raise ValueError(f"{col} debería ser booleana (True/False)")

    df = df.copy()
    for col, categories in {**ORDINAL, **NOMINAL}.items():
        unknown = set(df[col].unique()) - set(categories)
        if unknown:
            raise ValueError(f"Categorías desconocidas en {col}: {sorted(unknown)}")
        df[col] = pd.Categorical(df[col], categories=categories, ordered=col in ORDINAL)
    return df


def load_raw(path: Path | str = DATA_RAW) -> pd.DataFrame:
    """Lee el CSV crudo y lo valida con :func:`validate`."""
    return validate(pd.read_csv(path))


def encode_target(y: pd.Series) -> pd.Series:
    """Pasa las etiquetas Low/Medium/High a 0/1/2, que es lo que espera XGBoost."""
    return pd.Series(pd.Categorical(y, categories=LABELS).codes, index=y.index, name=TARGET_COL)


def decode_target(codes) -> list[str]:
    """Inversa de :func:`encode_target`: 0/1/2 → Low/Medium/High."""
    return [LABELS[int(c)] for c in codes]


def make_split(df: pd.DataFrame):
    """Split train/test 80/20, estratificado y con semilla fija.

    X conserva solo las features (sin ID ni variables de resultado) y la booleana va
    como 0/1. y queda codificada como entero (Low=0, Medium=1, High=2).

    :return: ``X_train, X_test, y_train, y_test``.
    """
    X = select_features(df)
    y = encode_target(df[TARGET_COL])
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y)


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """Deja solo las columnas de entrada del modelo, en orden, con la booleana como 0/1."""
    X = df[FEATURE_COLUMNS].copy()
    X[BOOLEAN] = X[BOOLEAN].astype(int)  # evita matrices dtype=object
    return X
