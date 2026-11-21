# Riesgo de burnout en producción: TP de MLOps

Trabajo práctico de **Operaciones de Aprendizaje Automático I** (CEIA, FIUBA). Llevamos a un entorno
productivo el modelo de nuestro TP de Aprendizaje de Máquina I
([AM-TP-SVA](https://github.com/SilvertK164/AM-TP-SVA)): un **XGBoost que predice el riesgo de burnout**
(Low / Medium / High) de un estudiante a partir de cómo usa la IA generativa.

## Integrantes

| Nombre | Usuario de GitHub |
|---|---|
| Victoria Villalba Tevez | [vivillalbatevez](https://github.com/vivillalbatevez) |
| Silvert Kevin Quispe Pacompia | [SilvertK164](https://github.com/SilvertK164) |
| Hernando Alexis González | [halexisgonzalez](https://github.com/halexisgonzalez) |

## Estado

**Primera entrega (clase 5)**: el checklist completo está en [docs/entrega_1.md](docs/entrega_1.md).
Apuntamos al nivel **en contenedores**.

**Alcance de este avance:** se implementan el ETL, el entrenamiento y el registro del modelo, y las
predicciones por lotes. FastAPI está incluido en Docker como servicio base, pero todavía no expone
un endpoint para predecir; la API de inferencia y las demás tareas de la segunda entrega están pendientes.

```
CSV (data/raw) ──► DAG etl_burnout ──► MinIO s3://data/burnout/{raw,final}
                                            │
            notebook experimento_mlflow_optuna (Optuna, 40 pruebas) ──► MLflow
                                            │                         │
     (Asset s3://data/burnout/final) ──► DAG train_burnout ──► burnout_model_prod@champion
                                                                       │
                      DAG batch_predict_burnout (@daily) ──► s3://data/burnout/batch/predictions.csv
```

## El modelo

| | |
|---|---|
| Dataset | [Impact of AI on Students](https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students) (Kaggle, CC0), 50.000 estudiantes. Diccionario en [data/README.md](data/README.md) |
| Objetivo | `Burnout_Risk_Level`: clasificación en 3 clases |
| Features | 12: hábitos de uso de IA y contexto. Excluimos `Post_Semester_GPA` y `Skill_Retention_Score` por fuga de información |
| Modelo | Preprocesador (ordinal + one-hot) + XGBoost con los hiperparámetros que encontró Optuna en AMq1 |
| Métrica | F1 macro en test: **0,5365** con los hiperparámetros de AMq1 (AMq1 informó 0,5405; IC 95 % de 0,531 a 0,550) |
| Búsqueda en MLflow | 40 pruebas de Optuna con runs anidados: mejor F1 macro en CV 0,5382 y en test **0,5362** (Windows) / **0,5380** (contenedor de Airflow), con otros hiperparámetros. El techo práctico es el mismo |

¿Por qué no da exactamente 0,5405? XGBoost (`hist`) da resultados levemente distintos según la cantidad
de hilos y el sistema operativo, y en AMq1 usamos `n_jobs=-1`. Ahora fijamos `XGB_N_JOBS = 4`, así cada
entorno da siempre el mismo resultado. Lo explicamos en la clase interactiva C1, §5.

Lo medimos con los mismos datos y los mismos hiperparámetros (la mejor prueba de Optuna):

| Entorno | 4 hilos | 1 hilo |
|---|---|---|
| Windows 11 (entorno local) | 0,5362 | 0,5381 |
| Linux (contenedor de Airflow) | 0,5380 | 0,5380 |

En el contenedor, que es el ambiente productivo, el resultado no depende de la cantidad de hilos. Entre
sistemas operativos hay una diferencia de hasta 0,002, muy por debajo del ancho del IC 95 % (±0,01): no
cambia ninguna conclusión, pero por eso el F1 que registra el DAG `train_burnout` no es idéntico al del
notebook corrido en Windows.

## Estructura

```
├── src/burnout/             # el modelo de AMq1 como paquete
│   ├── config.py            #   esquema, features, hiperparámetros, nombres de MLflow y S3
│   ├── data.py              #   carga, validación y split
│   ├── model.py             #   preprocesador, pipeline de XGBoost y métricas
│   ├── train.py             #   entrenamiento y registro en MLflow (también como CLI)
│   ├── etl.py               #   pasos del DAG de ETL
│   ├── batch.py             #   predicción por lotes
│   └── storage.py           #   lectura y escritura en MinIO/S3 con boto3
├── airflow/
│   ├── dags/                # etl_burnout, train_burnout, batch_predict_burnout
│   └── secrets/             # variables y conexiones de Airflow
├── notebooks/
│   └── experimento_mlflow_optuna.ipynb   # búsqueda de hiperparámetros registrada en MLflow
├── clases/                  # clases interactivas: repaso de AMq1, clases 1 a 5 y repaso integrador
├── tests/                   # pytest: datos, ETL (con S3 falso), modelo y predicción por lotes
├── .github/workflows/       # CI: linter y tests en cada push
├── dockerfiles/             # imágenes de Airflow, MLflow, PostgreSQL y FastAPI
├── docker-compose.yaml      # el ambiente productivo (basado en amq2-service-ml)
├── data/raw/                # CSV original (no se edita)
└── docs/                    # entrega 1, instalación de Docker, guía de la materia
```

## Cómo correrlo

### 1. Entorno local (sin Docker)

Requisito: Python 3.12.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt   # incluye el paquete del TP (pip install -e .)
```

Con el entorno activado:

```bash
pytest                       # tests (unos 10 segundos)
ruff check .                 # linter
python -m burnout.train      # entrena y evalúa el modelo final
jupyter lab                  # clases/ y notebooks/
```

En cada push y pull request, GitHub Actions corre `ruff check`, `ruff format --check` y `pytest`
([.github/workflows/ci.yml](.github/workflows/ci.yml)).

El notebook `notebooks/experimento_mlflow_optuna.ipynb` funciona sin Docker: usa un MLflow local con
SQLite. Para ver la UI:

```bash
mlflow ui --backend-store-uri sqlite:///notebooks/_salidas/mlflow.db --port 5001
```

### 2. Ambiente productivo (Docker)

Primero hay que instalar Docker Desktop: ver [docs/instalacion_docker_windows.md](docs/instalacion_docker_windows.md).

```bash
docker compose --profile all up -d
```

| Servicio | URL |
|---|---|
| Airflow | http://localhost:8080 (airflow / airflow) |
| MLflow | http://localhost:5001 |
| MinIO | http://localhost:9001 (minio / minio123) |
| FastAPI (servicio base, sin inferencia) | http://localhost:8800/ (`/docs` documenta solo la ruta de bienvenida) |

Orden de ejecución:

1. Activar `etl_burnout` y `train_burnout` en la UI de Airflow (los DAGs se crean pausados).
2. Disparar el DAG `etl_burnout`. Al terminar publica el *Asset* `s3://data/burnout/final` y Airflow
   dispara solo `train_burnout`.
3. (Opcional, para usar los hiperparámetros de la búsqueda) Correr
   `notebooks/experimento_mlflow_optuna.ipynb`: detecta Docker y registra en el MLflow del compose. Después
   volver a disparar `train_burnout`, que toma la mejor prueba de Optuna.
4. Cuando ya hay un modelo `champion`, activar `batch_predict_burnout`: corre todos los días (al activarlo
   corre una vez enseguida).

Lo mismo desde la terminal:

```bash
docker exec airflow-apiserver airflow dags unpause etl_burnout
docker exec airflow-apiserver airflow dags unpause train_burnout
docker exec airflow-apiserver airflow dags trigger etl_burnout
# cuando train_burnout terminó:
docker exec airflow-apiserver airflow dags unpause batch_predict_burnout
```

### Diferencias con el repositorio base de la cátedra

Partimos de [amq2-service-ml](https://github.com/facundolucianna/amq2-service-ml) (licencia Apache 2.0,
copia en [LICENSE.amq2-service-ml](LICENSE.amq2-service-ml)). Lo que cambiamos:

- `docker-compose.yaml`: monta `src/` y `data/` en Airflow, define `PYTHONPATH` y
  `MLFLOW_TRACKING_URI` y desactiva los DAGs de ejemplo.
- `dockerfiles/airflow/requirements.txt`: scikit-learn, xgboost y mlflow con **las mismas versiones**
  que el entorno local, para que un modelo registrado desde el notebook cargue en Airflow.
- `dockerfiles/mlflow/Dockerfile`: MLflow 3.18.0, la misma versión que usan los clientes.

## Clases interactivas

En [clases/](clases/README.md) hay 8 notebooks para aprender con nuestro propio TP: dos de repaso de AMq1,
uno por cada clase de MLOps hasta la 5 y un repaso integrador para la entrega. Cada uno tiene teoría con
diagramas, práctica con controles interactivos, ejercicios con verificación automática, casos de uso
reales, tarjetas de repaso y un cuestionario final con puntaje. El análisis del material de la cátedra está en [docs/guia_materia.md](docs/guia_materia.md).
