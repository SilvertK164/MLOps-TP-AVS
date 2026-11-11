"""Tests del ETL con un S3 falso en una carpeta temporal (sin MinIO ni Airflow)."""

import io

import pytest
from botocore.exceptions import ClientError

from burnout import etl, storage
from burnout.config import FEATURE_COLUMNS, S3_KEYS


class FakeS3:
    """Implementa get_object/put_object de boto3 sobre una carpeta local."""

    def __init__(self, root):
        self.root = root

    def put_object(self, Bucket, Key, Body):
        path = self.root / Bucket / Key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(Body)

    def get_object(self, Bucket, Key):
        path = self.root / Bucket / Key
        if not path.exists():
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        return {"Body": io.BytesIO(path.read_bytes())}


@pytest.fixture
def fake_s3(tmp_path, monkeypatch):
    s3 = FakeS3(tmp_path)
    monkeypatch.setattr(storage, "_client", lambda: s3)
    return s3


def test_etl_completo(fake_s3):
    raw_uri = etl.extract()
    assert raw_uri == f"s3://data/{S3_KEYS['raw']}"

    summary = etl.split(etl.validate_raw(raw_uri))
    assert summary["rows"] == 50_000
    assert (summary["train_rows"], summary["test_rows"]) == (40_000, 10_000)
    assert abs(sum(summary["class_share"].values()) - 1) < 1e-3

    X_train = storage.read_csv(S3_KEYS["X_train"])
    assert list(X_train.columns) == FEATURE_COLUMNS

    etl.write_data_info(summary)
    info = storage.read_json(S3_KEYS["data_info"])
    assert info["labels"] == ["Low", "Medium", "High"]


def test_validate_raw_corta_con_datos_malos(fake_s3):
    etl.extract()
    raw = storage.read_csv(S3_KEYS["raw"])
    raw.loc[0, "Institutional_Policy"] = "Strictly_Ban"
    storage.write_csv(raw, S3_KEYS["raw"])
    with pytest.raises(ValueError, match="Institutional_Policy"):
        etl.validate_raw("s3://data/x")


def test_read_json_con_default(fake_s3):
    assert storage.read_json("no/existe.json", default={}) == {}
