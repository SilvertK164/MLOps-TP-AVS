# Primera entrega (clase 5)

**Autores:** Victoria Villalba Tevez, Silvert Kevin Quispe Pacompia y Hernando Alexis González.

La cátedra pide entregar el link al repositorio con el avance, junto con lo que falta y cómo pensamos
continuar. Definimos el alcance como todo lo visto hasta la clase 5. El nivel al que apuntamos es
**en contenedores**.

## Checklist

| # | Ítem | Estado | Dónde |
|---|---|---|---|
| 1 | Repositorio en GitHub con los tres integrantes | ✅ | este repo |
| 2 | Modelo de AMq1 refactorizado en un paquete con docstrings y *type hints* | ✅ | `src/burnout/` |
| 3 | Tests automáticos: datos, ETL con S3 falso, reproducibilidad del modelo, predicción por lotes | ✅ 15 tests | `tests/` (`pytest`) |
| 4 | Linter y formato | ✅ | `ruff check .` / `ruff format .` |
| 5 | Integración continua: linter, formato y tests en cada push y pull request | ✅ | `.github/workflows/ci.yml` |
| 6 | Entorno reproducible: versiones exactas, semilla y cantidad de hilos de XGBoost fijas | ✅ | `requirements.txt`, `config.py` |
| 7 | Ambiente productivo en Docker (Airflow, MLflow, MinIO, PostgreSQL, Valkey, FastAPI) | ✅ probado | `docker-compose.yaml` |
| 8 | **DAG de ETL** en Airflow: crudo → validación → split → MinIO + registro del dataset en MLflow | ✅ probado | `airflow/dags/etl_burnout.py` |
| 9 | **Búsqueda de hiperparámetros registrada en MLflow** (Optuna, 40 pruebas, runs anidados) | ✅ probado contra el MLflow del compose | `notebooks/experimento_mlflow_optuna.ipynb` |
| 10 | Modelo en el Model Registry (`burnout_model_prod`) con alias `champion` | ✅ probado | notebook del punto 9, DAG `train_burnout` |
| 11 | DAG de entrenamiento con los mejores hiperparámetros de MLflow | ✅ probado | `airflow/dags/train_burnout.py` |
| 12 | Encadenamiento de DAGs con *Assets*: el ETL dispara solo el entrenamiento | ✅ probado | `etl_burnout` → `s3://data/burnout/final` → `train_burnout` |
| 13 | DAG de predicción por lotes diaria con el champion (clase 5) | ✅ probado | `airflow/dags/batch_predict_burnout.py` |
| 14 | Documentación | ✅ | `README.md`, `docs/`, docstrings, `doc_md` de cada DAG |
| 15 | Material de estudio del equipo: teoría, casos, ejercicios, tarjetas y cuestionarios por clase | ✅ | `clases/` (C6 = repaso integrador) |

## Qué verificamos en Docker

Con `docker compose --profile all up -d` levantan los 12 servicios y todos quedan *healthy*. Los tres DAGs
cargan sin errores de importación. Corrimos el flujo completo:

| Paso | Resultado |
|---|---|
| `etl_burnout` (manual) | 50.000 filas validadas; en `s3://data/burnout/` quedan `raw/`, `final/train` (40.000), `final/test` (10.000) y `data_info/data.json`. Tarda unos 13 s |
| Notebook de Optuna contra `http://localhost:5001` | 40 runs hijos en el experimento *Burnout Risk*; mejor F1 macro en CV 0,5382 (`trial_36`), igual que en la corrida local. Registra `burnout_model_prod` v1 como champion |
| `etl_burnout` → `train_burnout` (por *Asset*) | El entrenamiento arranca solo (`asset_triggered__…`), toma los hiperparámetros de `trial_36` y obtiene **F1 macro 0,5380** en test. Registra la v2 y le pasa el alias `champion` |
| `batch_predict_burnout` | Carga `models:/burnout_model_prod@champion`, predice 500 estudiantes y escribe `s3://data/burnout/batch/predictions.csv` con la probabilidad de cada clase y la clase predicha |

### Hallazgo: reproducibilidad entre sistemas operativos

El notebook en Windows obtuvo 0,5362 en test y el DAG en el contenedor 0,5380, con los mismos datos y los
mismos hiperparámetros. Lo medimos:

| Entorno | 4 hilos | 1 hilo |
|---|---|---|
| Windows 11 (entorno local) | 0,5362 | 0,5381 |
| Linux (contenedor de Airflow) | 0,5380 | 0,5380 |

Fijar los hilos de XGBoost hace que cada entorno sea reproducible, pero no iguala resultados entre
sistemas operativos. La diferencia (≤ 0,002) es mucho menor que el IC 95 % (±0,01). Conclusión: la
métrica oficial del modelo es la que registra el DAG en el contenedor, que es el ambiente productivo.

## Capturas

⏳ Pendiente: guardarlas en `docs/img/` y enlazarlas acá.

- Airflow: vista Grid de los tres DAGs y la vista de *Assets*.
- MLflow: experimento *Burnout Risk* con los runs anidados de Optuna y el modelo `burnout_model_prod`
  con el alias `champion`.
- MinIO: bucket `data/burnout/` con `raw/`, `final/`, `data_info/` y `batch/`.

## Qué falta y cómo seguimos (segunda entrega)

| # | Tarea | Clase | Detalle |
|---|---|---|---|
| 1 | **API REST con FastAPI** | 6 | Cargar `burnout_model_prod@champion` al iniciar; `POST /predict` con un esquema pydantic que valide cada feature (rangos y categorías de `data_info/data.json`) y devuelva clase y probabilidades; ejemplos en `/docs`; endpoint `/health` y recarga del modelo cuando cambia el champion |
| 2 | Tests de la API | 6 | `TestClient` de FastAPI con un modelo falso: entrada válida, categoría inválida y rangos fuera de dominio |
| 3 | **Reentrenamiento champion/challenger** | 7 | Que `train_burnout` registre un *challenger* y le pase el alias `champion` solo si mejora el F1 macro en test; si no, queda registrado pero sin promover |
| 4 | Servir las predicciones por lotes | 5 | Guardar `predictions.csv` también en Valkey (clave = `Student_ID`) y consultarlo desde la API, como en el ejemplo de la clase 5 |
| 5 | Monitoreo simple | 7 | Que el DAG de lotes registre en MLflow la distribución de clases predichas por día, para detectar *drift* |
| 6 | Documentación final | — | Diagrama de arquitectura, guía de uso de la API y capturas actualizadas |

Prioridad: 1 → 3 → 2 → 4 → 5. Los puntos 1 a 3 son el mínimo para el nivel en contenedores. Los 4 y 5
suman si llegamos con tiempo.

## Cómo reproducir esta entrega

Ver la sección *Ambiente productivo (Docker)* del [README](../README.md#2-ambiente-productivo-docker).
