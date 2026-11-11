# Primera entrega (clase 5)

La cátedra pide entregar en la clase 5 el link al repositorio con el avance. Definimos el alcance como todo
lo visto hasta esa clase, y el nivel al que apuntamos es **en contenedores**.

## Checklist

| # | Ítem | Estado | Dónde |
|---|---|---|---|
| 1 | Repositorio en GitHub con los tres integrantes | ✅ | este repo |
| 2 | Modelo de AMq1 refactorizado en un paquete con docstrings y *type hints* | ✅ | `src/burnout/` |
| 3 | Tests automáticos: datos, ETL con S3 falso, reproducibilidad del modelo, predicción por lotes | ✅ | `tests/` (`pytest`) |
| 4 | Linter y formato | ✅ | `ruff check .` / `ruff format .` |
| 5 | Entorno reproducible: versiones exactas, semilla y cantidad de hilos de XGBoost fijas | ✅ | `requirements.txt`, `config.py` |
| 6 | Ambiente productivo en Docker (Airflow, MLflow, MinIO, PostgreSQL, Valkey, FastAPI) | ✅ archivos / ⏳ probar con Docker | `docker-compose.yaml` |
| 7 | **DAG de ETL** en Airflow: crudo → validación → split → MinIO + registro en MLflow | ✅ código / ⏳ correr en Docker | `airflow/dags/etl_burnout.py` |
| 8 | **Experimento de búsqueda de hiperparámetros en MLflow** (Optuna, 40 pruebas, runs anidados) | ✅ ejecutado en modo local | `notebooks/experimento_mlflow_optuna.ipynb` |
| 9 | Modelo registrado en el Model Registry con alias `champion` | ✅ ejecutado en modo local | notebook del punto 8, DAG `train_burnout` |
| 10 | DAG de entrenamiento con los mejores hiperparámetros de MLflow | ✅ código / ⏳ correr en Docker | `airflow/dags/train_burnout.py` |
| 11 | DAG de predicción por lotes con el champion (clase 5) | ✅ código / ⏳ correr en Docker | `airflow/dags/batch_predict_burnout.py` |
| 12 | Documentación | ✅ | `README.md`, `docs/`, docstrings, `doc_md` de cada DAG |

⏳ = falta verificarlo con Docker. Hoy Docker no está instalado en la máquina donde armamos el repo.

## Para cerrar la entrega con Docker

1. Instalar Docker Desktop: ver [instalacion_docker_windows.md](instalacion_docker_windows.md).
2. `docker compose --profile all up -d` y esperar a que todos los servicios estén *healthy*.
3. En Airflow (http://localhost:8080, usuario y clave `airflow`), activar y disparar `etl_burnout`.
4. Correr `notebooks/experimento_mlflow_optuna.ipynb`. Detecta solo que Docker está levantado y registra
   en http://localhost:5001.
5. Disparar `train_burnout` y luego `batch_predict_burnout`.
6. Sacar capturas de Airflow (vista Grid), MLflow (runs y modelo) y MinIO (bucket `data/burnout/`), y
   agregarlas a `docs/img/` y al README.

## Para la segunda entrega

- API REST con FastAPI que cargue `burnout_model_prod@champion`, con un esquema pydantic que documente
  cada feature (rangos y categorías válidas) y ejemplos en `/docs`.
- DAG de reentrenamiento champion/challenger: entrena un challenger y lo promueve si mejora el F1 macro.
- Opcional: un tablero con los resultados del lote, o servir las predicciones por lotes desde Valkey.
