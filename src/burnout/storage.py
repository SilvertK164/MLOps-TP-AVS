"""Lectura y escritura en el Data Lake (MinIO, compatible con S3) usando boto3.

boto3 toma las credenciales y el endpoint de las variables de entorno
``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY`` y ``AWS_ENDPOINT_URL_S3``. Dentro de
Docker el endpoint es ``http://s3:9000``; desde tu máquina, ``http://localhost:9000``.
"""

import io
import json

import boto3
import pandas as pd
from botocore.exceptions import ClientError

from burnout.config import BUCKET


def _client():
    return boto3.client("s3")


def read_csv(key: str, bucket: str = BUCKET, **kwargs) -> pd.DataFrame:
    """Lee ``s3://bucket/key`` como DataFrame."""
    obj = _client().get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj["Body"].read()), **kwargs)


def write_csv(df: pd.DataFrame, key: str, bucket: str = BUCKET) -> str:
    """Escribe un DataFrame en ``s3://bucket/key`` (sin índice) y devuelve la URI."""
    _client().put_object(Bucket=bucket, Key=key, Body=df.to_csv(index=False).encode())
    return f"s3://{bucket}/{key}"


def read_json(key: str, bucket: str = BUCKET, default: dict | None = None) -> dict:
    """Lee un JSON; si no existe y se pasó ``default``, devuelve ``default``."""
    try:
        obj = _client().get_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if default is not None and e.response["Error"]["Code"] in {"NoSuchKey", "404"}:
            return default
        raise
    return json.loads(obj["Body"].read().decode())


def write_json(data: dict, key: str, bucket: str = BUCKET) -> str:
    """Escribe un diccionario como JSON indentado y devuelve la URI."""
    body = json.dumps(data, indent=2, ensure_ascii=False).encode()
    _client().put_object(Bucket=bucket, Key=key, Body=body)
    return f"s3://{bucket}/{key}"
