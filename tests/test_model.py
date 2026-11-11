import pandas as pd
import pytest

from burnout.config import BEST_PARAMS_AMQ1
from burnout.data import load_raw, make_split
from burnout.model import feature_importance, make_pipeline
from burnout.train import train_and_evaluate


@pytest.fixture(scope="module")
def trained():
    X_train, X_test, y_train, y_test = make_split(load_raw())
    pipeline, metrics = train_and_evaluate(X_train, y_train, X_test, y_test, BEST_PARAMS_AMQ1)
    return pipeline, metrics, X_test


def test_reproduce_resultado_de_amq1(trained):
    """El F1 macro en test cae dentro del IC 95 % que reportamos en AMq1 (0,531 – 0,550).

    No pedimos el 0,5405 exacto: XGBoost (hist) cambia levemente según la cantidad de hilos,
    y en AMq1 usamos n_jobs=-1 en otra máquina. Por eso ahora fijamos XGB_N_JOBS.
    """
    _, metrics, _ = trained
    assert 0.531 <= metrics["f1_macro"] <= 0.550


def test_entrenamiento_determinista():
    """Dos entrenamientos con la misma configuración dan exactamente las mismas predicciones."""
    X_train, X_test, y_train, _ = make_split(load_raw())
    sample = X_train.sample(5000, random_state=0).index
    preds = [
        make_pipeline(**BEST_PARAMS_AMQ1).fit(X_train.loc[sample], y_train.loc[sample]).predict(X_test)
        for _ in range(2)
    ]
    assert (preds[0] == preds[1]).all()


def test_predice_las_tres_clases(trained):
    pipeline, _, X_test = trained
    assert set(pipeline.predict(X_test)) == {0, 1, 2}
    proba = pipeline.predict_proba(X_test.head(5))
    assert proba.shape == (5, 3)
    assert proba.sum(axis=1) == pytest.approx(1.0)


def test_importancia_usa_nombres_reales(trained):
    pipeline, _, _ = trained
    gain = feature_importance(pipeline)
    assert "Weekly_GenAI_Hours" in gain.index


def test_predict_batch(trained):
    from burnout.batch import predict_batch
    from burnout.config import DATA_RAW, OUTCOMES

    pipeline, _, _ = trained
    batch = pd.read_csv(DATA_RAW).head(20).drop(columns=OUTCOMES)
    out = predict_batch(pipeline, batch)
    assert list(out.columns) == ["Student_ID", "proba_Low", "proba_Medium", "proba_High", "Burnout_Risk_Pred"]
    assert out["Student_ID"].tolist() == batch["Student_ID"].tolist()
    assert set(out["Burnout_Risk_Pred"]) <= {"Low", "Medium", "High"}


def test_log_and_register_en_mlflow_local(trained, tmp_path, monkeypatch):
    """El modelo se registra y se vuelve a cargar por alias (atrapa problemas de serialización)."""
    import mlflow

    from burnout.config import CHAMPION_ALIAS, REGISTERED_MODEL
    from burnout.train import log_and_register

    pipeline, metrics, X_test = trained
    uri = f"sqlite:///{(tmp_path / 'mlflow.db').as_posix()}"
    mlflow.set_tracking_uri(uri)
    monkeypatch.chdir(tmp_path)  # MLflow guarda los artefactos en ./mlruns del directorio actual
    mlflow.set_experiment("test")
    version = log_and_register(pipeline, metrics, BEST_PARAMS_AMQ1, X_test, uri)
    loaded = mlflow.sklearn.load_model(f"models:/{REGISTERED_MODEL}@{CHAMPION_ALIAS}")
    assert version == "1"
    assert (loaded.predict(X_test) == pipeline.predict(X_test)).all()
