import pandas as pd
import pytest

from burnout.config import DATA_RAW, FEATURE_COLUMNS, LABELS, OUTCOMES
from burnout.data import decode_target, encode_target, make_split, validate


@pytest.fixture(scope="module")
def raw() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW)


def test_load_raw_tipa_categorias(raw):
    df = validate(raw)
    assert len(df) == 50_000
    assert df["Year_of_Study"].cat.ordered
    assert list(df["Burnout_Risk_Level"].cat.categories) == LABELS


def test_validate_rechaza_columna_faltante(raw):
    with pytest.raises(ValueError, match="Faltan"):
        validate(raw.drop(columns="Tool_Diversity"))


def test_validate_rechaza_categoria_desconocida(raw):
    bad = raw.head(10).copy()
    bad.loc[0, "Major_Category"] = "Astrology"
    with pytest.raises(ValueError, match="Categorías desconocidas"):
        validate(bad)


def test_validate_rechaza_nulos(raw):
    bad = raw.head(10).copy()
    bad.loc[0, "Weekly_GenAI_Hours"] = None
    with pytest.raises(ValueError, match="nulos"):
        validate(bad)


def test_split_sin_fuga_y_reproducible(raw):
    df = validate(raw)
    X_train, X_test, y_train, y_test = make_split(df)
    assert list(X_train.columns) == FEATURE_COLUMNS
    assert not set(OUTCOMES) & set(X_train.columns)
    assert len(X_test) == 10_000
    # Mismo split en dos llamadas: la semilla está fija.
    assert make_split(df)[1].index.equals(X_test.index)
    # Estratificado: misma proporción de clases (±1 punto) en train y test.
    diff = y_train.value_counts(normalize=True) - y_test.value_counts(normalize=True)
    assert diff.abs().max() < 0.01


def test_encode_decode_ida_y_vuelta():
    y = pd.Series(["Low", "High", "Medium"])
    codes = encode_target(y)
    assert codes.tolist() == [0, 2, 1]
    assert decode_target(codes) == y.tolist()
