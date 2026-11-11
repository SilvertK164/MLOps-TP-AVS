# Guía de la materia: qué hay en el repositorio de la cátedra

Resumen del análisis del repositorio
[aprendizaje_maquina_II](https://github.com/FIUBA-Posgrado-Inteligencia-Artificial/aprendizaje_maquina_II)
(Operaciones de Aprendizaje Automático I, CEIA-FIUBA) y del repositorio base del TP,
[amq2-service-ml](https://github.com/facundolucianna/amq2-service-ml). Revisamos las diapositivas, los
hands-on y los notebooks de las clases 1 a 7.

## El trabajo práctico

- **Escenario:** trabajamos para *ML Models and something more Inc.*, que ofrece modelos mediante una
  REST API o predicción por lotes. Internamente usa Apache Airflow, MLflow y un Data Lake en S3
  (simulado con MinIO).
- **Grupal**, de 2 a 6 personas. **Se entrega en dos partes**: la primera en la **clase 5** y la final
  7 días después de la última clase. En el aula virtual solo se envía el link al repositorio.
- **Niveles:** *local* (nota 6 a 8: ciclo de desarrollo del modelo de AMq1 hasta el artefacto, con un
  orquestador y buena documentación) o *en contenedores* (nota 8 a 10: el modelo en el ambiente
  productivo con Airflow, MLflow, PostgreSQL, MinIO y FastAPI en Docker).
- **Mínimos del nivel contenedores** (README de `amq2-service-ml`):
  1. Un DAG en Apache Airflow (ETL, entrenamiento, etc.).
  2. Un experimento en MLflow de búsqueda de hiperparámetros.
  3. Servir el modelo de AMq1 en la REST API.
  4. Documentar: comentarios y docstrings en scripts y notebooks, y documentación de FastAPI acorde al modelo.
- La cátedra no detalla qué incluye la primera parte. Nosotros la definimos como todo lo visto hasta la
  clase 5: buenas prácticas, Docker, MLflow, Airflow y predicción por lotes (ver [entrega_1.md](entrega_1.md)).
- El branch [`example_implementation`](https://github.com/facundolucianna/amq2-service-ml/tree/example_implementation)
  tiene un ejemplo completo con Heart Disease: DAG de ETL, DAG de reentrenamiento champion/challenger,
  notebook de Optuna + MLflow y API.

## Clase por clase

| Clase | Teoría | Hands-on | ¿Corre en Windows sin Docker? |
|---|---|---|---|
| 1 | Ciclo de vida, MLOps y sus niveles, buenas prácticas | Notebook de buenas prácticas; refactor de `svm.ipynb` a `etl.py` / `train_model.py` / `test_model.py` (Heart Disease) | Sí |
| 2 | Desarrollo de modelos, evaluación, contenedores | Dockerfile simple, servidor FastAPI, WordPress con Compose, mini servicio de modelo (Postgres + Streamlit) | Solo el servidor FastAPI |
| 3 | Infraestructura, almacenamiento y cómputo, MLflow | Tracking manual, autolog con GridSearch y Model Registry (iris), en versión local y con contenedores | La versión local, sí |
| 4 | Orquestadores y sincronizadores, Airflow | ETL de Heart Disease en Airflow (TaskFlow y estilo tradicional) y en Metaflow | No (Airflow y Metaflow necesitan Linux: Docker o WSL) |
| 5 | Despliegue, estrategias, predicción por lotes | Batch con Metaflow + MinIO + Valkey; servir buscando por hash | Solo el notebook de consulta |
| 6 | Desplegado online, APIs, REST | Consumir APIs con `requests`; FastAPI con pydantic, validaciones y API key | Sí |
| 7 | Sirviendo modelos en el mundo real | Casos de estudio (forecasting, seguimiento de usuarios) | Solo teoría |

## Detalles del material a tener en cuenta

Encontrados al revisar el código. Ninguno afecta a nuestro TP, pero conviene conocerlos si se reutiliza
el material:

- **Airflow 3:** varios ejemplos usan `from airflow.decorators import ...` (deprecado; lo nuevo es
  `airflow.sdk`) y ponen `schedule_interval` dentro de `default_args`. `schedule_interval` ya no existe en
  Airflow 3 y ahí no tiene efecto; se usa `schedule=` en el DAG.
- **Clase 1:** el `heart.csv` tiene 1025 filas, pero solo 302 son únicas. Las filas duplicadas quedan a
  ambos lados del split y por eso el SVM parece casi perfecto. El ejemplo de la cátedra hace
  `drop_duplicates` antes del split.
- **Clase 2 (mini servicio):** `create_engine("postgresql://...")` necesita psycopg2, pero solo está
  instalado psycopg 3; hace falta `postgresql+psycopg://`. Además, la comparación `"Semi-Senior"` contra
  la opción `"Semi-senior"` nunca coincide.
- **Clase 3:** `plot_roc_curve` llama a `savefig` después de `close` (guardaría una figura vacía). El
  README local levanta MLflow en el puerto 8888, que choca con Jupyter.
- **Clase 4:** en `etl_process_tradicional.py`, `normalize_data` devuelve rutas `*_norm.csv` que nunca
  escribe. El `.env` de esa clase pone la UI de Airflow en el puerto 8000, no en 8080.
- **Clase 5:** `pd.read_csv` sin `header=None` toma la primera fila de iris como encabezado. Además, el
  flujo redondea a 2 decimales y el notebook a 1, así que algunas claves no coinciden.
- **Clase 6:** FastAPI convierte el parámetro `api_key: str = Header()` al header `api-key` (con guion).
  Por eso el `curl` del README con `api_key` responde 422.

## Cómo lo trasladamos a nuestro TP

| Concepto de la materia | Dónde está en este repo |
|---|---|
| Notebook → módulos con docstrings y tests (clase 1) | `src/burnout/`, `tests/` |
| Docker Compose con todos los servicios (clase 2) | `docker-compose.yaml`, `dockerfiles/` |
| Experimento con runs anidados y Model Registry (clase 3) | `notebooks/experimento_mlflow_optuna.ipynb` |
| DAGs con TaskFlow (clase 4) | `airflow/dags/etl_burnout.py`, `train_burnout.py` |
| Predicción por lotes (clase 5) | `airflow/dags/batch_predict_burnout.py`, `src/burnout/batch.py` |
| REST API con FastAPI (clase 6) | 2ª entrega (`dockerfiles/fastapi/`) |
