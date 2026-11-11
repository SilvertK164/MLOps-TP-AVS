"""Banco de tarjetas de repaso y preguntas de los cuestionarios de cada clase.

Vive fuera de los notebooks para que las respuestas no queden a la vista. Formato:

- ``TARJETAS[clave]``: lista de ``(frente, dorso)``.
- ``PREGUNTAS[clave]``: lista de ``(pregunta, opciones, índice_correcto, explicación)``.

Las claves son las de las clases: R1, R2, C1 … C5.
"""

NOMBRES = {
    "R1": "Repaso AMq1 · datos y preprocesamiento",
    "R2": "Repaso AMq1 · modelos, métricas y Optuna",
    "C1": "Clase 1 · MLOps y buenas prácticas",
    "C2": "Clase 2 · Docker",
    "C3": "Clase 3 · MLflow",
    "C4": "Clase 4 · Airflow",
    "C5": "Clase 5 · Despliegue y batch",
}

TARJETAS = {
    "R1": [
        ("¿Qué predice el modelo del TP?",
         "`Burnout_Risk_Level` (Low / Medium / High): clasificación en 3 clases, a partir de cómo usan "
         "la IA generativa 50.000 estudiantes."),
        ("Fuga de información (*data leakage*)",
         "Entrenar con información que **no va a estar disponible al momento de predecir**. La métrica "
         "en validación sale inflada y el modelo se desploma en producción."),
        ("¿Por qué sacamos `Post_Semester_GPA` y `Skill_Retention_Score`?",
         "Se miden al **final** del semestre, junto con el burnout. Cuando queremos predecir (durante la "
         "cursada) todavía no existen: usarlas sería fuga de información."),
        ("Codificación ordinal",
         "Para categorías **con orden** (`Year_of_Study`, `Prompt_Engineering_Skill`): una sola columna "
         "con 0, 1, 2… respetando ese orden."),
        ("Codificación one-hot",
         "Para categorías **sin orden** (`Major_Category`, `Primary_Use_Case`, `Institutional_Policy`): "
         "una columna 0/1 por categoría, así no inventamos un orden que no existe."),
        ("Split estratificado",
         "Divide train/test manteniendo **la misma proporción de cada clase** en ambos (acá 42 % Medium, "
         "33 % Low, 25 % High)."),
        ("¿Por qué el preprocesador se ajusta solo con train?",
         "Porque si ve el test (por ejemplo, para calcular medias o categorías) le filtra información "
         "al modelo y la evaluación deja de ser honesta. Por eso va **dentro del Pipeline**."),
        ("Línea de base (*baseline*) tonta",
         "Predecir siempre la clase más frecuente. Acá tiene accuracy 0,42: cualquier modelo útil tiene "
         "que superarla con claridad."),
        ("¿Qué hace `validate(df)` en el TP?",
         "Revisa columnas, nulos, tipos y categorías antes de usar los datos y levanta `ValueError` si "
         "algo no cuadra: **fallar temprano** en vez de entrenar con datos rotos."),
    ],
    "R2": [
        ("F1 macro",
         "Promedio **sin ponderar** del F1 de cada clase. Una clase chica pesa lo mismo que una grande: "
         "por eso lo usamos con clases desbalanceadas."),
        ("Precisión vs recall",
         "Precisión: de lo que marqué como High, ¿cuánto era High? Recall: de todos los High reales, "
         "¿cuántos encontré?"),
        ("Sobreajuste (*overfitting*)",
         "El modelo memoriza train: score muy alto en train y bastante más bajo en validación. Se combate "
         "con regularización, menos complejidad o más datos."),
        ("Validación cruzada (CV)",
         "Dividir train en *k* partes, entrenar con *k − 1* y evaluar en la restante, *k* veces. Da una "
         "estimación más estable que un solo split y **no toca el test**."),
        ("`max_depth` en XGBoost",
         "Profundidad máxima de cada árbol. Más profundidad = más interacciones y más riesgo de "
         "sobreajuste. AMq1 terminó en 2."),
        ("`learning_rate` y `n_estimators`",
         "Cuánto aporta cada árbol nuevo y cuántos árboles se suman. Van juntos: tasa chica necesita más "
         "árboles."),
        ("`gamma`, `reg_alpha`, `reg_lambda`",
         "Regularización: `gamma` exige una ganancia mínima para dividir un nodo; `reg_alpha` (L1) y "
         "`reg_lambda` (L2) penalizan los pesos de las hojas."),
        ("Optuna y TPE",
         "Optuna busca hiperparámetros. TPE (*Tree-structured Parzen Estimator*) usa las pruebas "
         "anteriores para proponer la siguiente en zonas prometedoras, en vez de probar al azar."),
        ("¿Por qué el test se usa una sola vez?",
         "Si elegimos modelo o hiperparámetros mirando el test, lo convertimos en validación y su "
         "métrica deja de estimar el rendimiento en datos nuevos."),
    ],
    "C1": [
        ("MLOps",
         "Prácticas para **llevar un modelo a producción y mantenerlo ahí**: datos y código "
         "versionados, entrenamiento reproducible, despliegue, monitoreo y reentrenamiento."),
        ("Niveles de madurez de MLOps (Google)",
         "0: todo manual. 1: pipeline de entrenamiento automatizado (entrenamiento continuo). 2: CI/CD "
         "del propio pipeline."),
        ("Deuda técnica en ML (Sculley et al., 2015)",
         "El código del modelo es una parte chica del sistema. Lo que más cuesta mantener es todo lo de "
         "alrededor: datos, configuración, monitoreo, infraestructura."),
        ("DRY",
         "*Don't Repeat Yourself*: cada cosa definida en un solo lugar. En el TP: las constantes en "
         "`config.py`, no copiadas en 7 notebooks."),
        ("Docstring y *type hints*",
         "El docstring dice qué hace la función, qué recibe y qué devuelve. Los *type hints* "
         "(`df: pd.DataFrame -> pd.Series`) documentan los tipos y los chequean las herramientas."),
        ("PEP 8 y linter",
         "PEP 8 es la guía de estilo de Python. Un linter (en el TP, `ruff`) la revisa automáticamente y "
         "encuentra errores comunes, como imports sin usar."),
        ("Test unitario",
         "Función que verifica un comportamiento con un `assert` (en el TP, con `pytest`). Si alguien "
         "rompe algo, el test falla antes de llegar a producción."),
        ("Reproducibilidad",
         "Mismo código + mismos datos = mismo modelo. En el TP: semilla, hilos de XGBoost, versiones "
         "exactas de librerías y datos versionados."),
        ("Flujo de Git en equipo",
         "Una rama por tarea, commits chicos, Pull Request para que otro integrante revise antes de "
         "unir a `main`."),
    ],
    "C2": [
        ("Imagen vs contenedor",
         "La imagen es la plantilla inmutable (como una clase). El contenedor es una instancia que corre "
         "(como un objeto). De una imagen salen muchos contenedores."),
        ("Contenedor vs máquina virtual",
         "La VM virtualiza el hardware y trae su propio sistema operativo. El contenedor comparte el "
         "kernel del host: arranca en segundos y pesa mucho menos."),
        ("Dockerfile",
         "Receta para construir una imagen: `FROM` (base), `WORKDIR`, `COPY`, `RUN` (instalar), `EXPOSE` "
         "y `CMD` (qué ejecutar al arrancar)."),
        ("Capas y caché",
         "Cada instrucción del Dockerfile es una capa cacheada. Se copia `requirements.txt` y se instala "
         "**antes** de copiar el código, así cambiar el código no reinstala todo."),
        ("Volumen",
         "Almacenamiento que sobrevive al contenedor. Sin volumen, al borrar el contenedor se pierden "
         "los datos (por ejemplo, la base de PostgreSQL)."),
        ("`ports: \"5001:5000\"`",
         "Puerto del **host** : puerto del **contenedor**. Desde tu navegador usás 5001; entre "
         "contenedores se usa el nombre del servicio y el puerto interno: `http://mlflow:5000`."),
        ("Docker Compose",
         "Describe en un YAML todos los servicios, redes y volúmenes, y los levanta juntos con "
         "`docker compose up`."),
        ("Perfiles del compose del TP",
         "`--profile all` levanta todo. También hay `mlflow`, `airflow` y `debug`, para levantar solo "
         "una parte."),
        ("Servicios del compose del TP",
         "Airflow (8080), MLflow (5001), MinIO S3 (9000 API, 9001 consola), PostgreSQL, Valkey (broker "
         "de Celery) y FastAPI (8800)."),
    ],
    "C3": [
        ("Run de MLflow",
         "Una ejecución registrada: parámetros, métricas, etiquetas y artefactos (modelos, gráficos)."),
        ("Experimento",
         "Carpeta lógica que agrupa runs del mismo problema. En el TP: **Burnout Risk**."),
        ("Parámetro vs métrica",
         "Parámetro: entrada fija del run (`max_depth=2`). Métrica: resultado numérico, que puede "
         "cambiar por paso (`f1_macro=0.536`)."),
        ("Backend store vs artifact store",
         "Backend: metadatos (runs, params, métricas) en una base, PostgreSQL en Docker. Artifact store: "
         "archivos (modelos, figuras), MinIO `s3://mlflow` en Docker."),
        ("Runs anidados",
         "Un run padre con un run hijo por prueba (`nested=True`). Se usa en búsquedas de "
         "hiperparámetros para verlas agrupadas en la UI."),
        ("Autolog",
         "`mlflow.sklearn.autolog()` registra solo parámetros, métricas y modelo al llamar `fit`. Útil "
         "para explorar; en el TP registramos a mano para controlar qué se guarda."),
        ("Model Registry",
         "Catálogo de modelos con versiones (v1, v2…). Cada versión apunta al run que la generó: "
         "trazabilidad."),
        ("Alias `champion` / `challenger`",
         "Nombres móviles que apuntan a una versión. Producción carga `models:/burnout_model_prod@champion`; "
         "promover un modelo es mover el alias, sin tocar el código."),
        ("¿Por qué `skops_trusted_types` en el TP?",
         "MLflow 3 serializa sklearn con skops, que solo carga tipos confiables. XGBoost no está en la "
         "lista por defecto, así que lo declaramos explícitamente."),
    ],
    "C4": [
        ("Orquestador",
         "Herramienta que ejecuta flujos de tareas con dependencias, horarios, reintentos y monitoreo. "
         "Ejemplos: Airflow, Prefect, Dagster, Metaflow."),
        ("DAG",
         "*Directed Acyclic Graph*: tareas (nodos) con dependencias (flechas) y sin ciclos. Define el "
         "orden de ejecución."),
        ("TaskFlow (`@dag`, `@task`)",
         "Forma moderna de escribir DAGs: cada tarea es una función de Python y las dependencias salen "
         "de pasarse los resultados."),
        ("XCom",
         "Mecanismo para pasar valores **chicos** entre tareas (rutas, conteos, un dict). Los datos "
         "grandes van a S3/MinIO y por XCom solo viaja la ruta."),
        ("`schedule` y cron",
         "Cuándo corre el DAG: `@daily`, `None` (solo manual) o cron `min hora día mes día_semana`, "
         "por ejemplo `30 6 * * *` = todos los días a las 6:30."),
        ("Scheduler, worker, API server",
         "Scheduler: decide qué tarea corre y cuándo. Worker: la ejecuta (con Celery en el TP). API "
         "server: la UI y la API web de Airflow 3."),
        ("Idempotencia",
         "Correr una tarea dos veces deja el mismo resultado que correrla una. Clave para poder "
         "reintentar sin ensuciar los datos."),
        ("Variables y secretos",
         "Configuración externa al código (`Variable.get('burnout_batch_size')`). En el TP salen de "
         "`airflow/secrets/variables.yaml`."),
        ("Imports pesados dentro de las tareas",
         "El scheduler parsea los archivos de DAG seguido: si importan pandas o xgboost arriba de todo, "
         "todo se vuelve lento. Se importan dentro de cada `@task`."),
    ],
    "C5": [
        ("Predicción por lotes (batch)",
         "Se predice para muchos registros de una vez, en horario programado, y se guardan los "
         "resultados. Barato y simple; las predicciones pueden quedar desactualizadas."),
        ("Predicción en línea (online)",
         "Se predice al recibir cada pedido (API). Siempre al día, pero exige baja latencia, el servicio "
         "siempre arriba y más infraestructura."),
        ("¿Por qué el batch es eficiente?",
         "Vectoriza: una llamada a `predict` con 10.000 filas cuesta mucho menos que 10.000 llamadas de "
         "1 fila (se reparte el costo fijo de cada llamada)."),
        ("Almacén clave-valor",
         "Guarda las predicciones precalculadas por clave (`Student_ID`, o un hash de las features). "
         "Servir es una búsqueda O(1): Redis/Valkey, DynamoDB."),
        ("Deploy blue/green",
         "Dos entornos idénticos; se cambia todo el tráfico del viejo (blue) al nuevo (green) de golpe. "
         "Volver atrás es cambiar el tráfico de nuevo."),
        ("Deploy canary",
         "El modelo nuevo recibe primero un porcentaje chico del tráfico (por ejemplo, 5 %). Si las "
         "métricas acompañan, se sube de a poco."),
        ("Shadow deployment",
         "El modelo nuevo recibe una copia del tráfico real y predice, pero **sus respuestas no se usan**. "
         "Sirve para comparar sin riesgo."),
        ("Prueba A/B",
         "Se reparte a los usuarios entre dos modelos y se mide un resultado de negocio para decidir "
         "con estadística cuál es mejor."),
        ("El DAG batch del TP",
         "`batch_predict_burnout` (`@daily`): toma un lote, carga `@champion` de MLflow, predice "
         "probabilidades y clase, y escribe `s3://data/burnout/batch/predictions.csv`."),
    ],
}

PREGUNTAS = {
    "R1": [
        ("¿Qué tipo de problema resuelve el modelo del TP?",
         ["Regresión", "Clasificación binaria", "Clasificación en 3 clases", "Clustering"], 2,
         "Predice Low, Medium o High: clasificación multiclase (3 clases)."),
        ("¿Cuál de estas columnas sería fuga de información si la usáramos como feature?",
         ["`Weekly_GenAI_Hours`", "`Post_Semester_GPA`", "`Year_of_Study`", "`Paid_Subscription`"], 1,
         "El promedio del final del semestre se conoce recién cuando ya pasó lo que queremos predecir."),
        ("`Year_of_Study` (Freshman → Graduate) se codifica con…",
         ["One-hot", "Ordinal", "Se descarta", "Hashing"], 1,
         "Tiene un orden natural, y la codificación ordinal lo conserva en una sola columna."),
        ("`Major_Category` (STEM, Business, Arts…) se codifica con…",
         ["Ordinal: STEM=0, Business=1…", "One-hot", "La media del target", "Se descarta"], 1,
         "No hay un orden entre carreras: ordinal inventaría uno, y one-hot no."),
        ("Un modelo que siempre predice 'Medium', ¿qué accuracy tiene en este dataset?",
         ["≈ 0,25", "≈ 0,33", "≈ 0,42", "≈ 0,54"], 2,
         "Medium es el 42 % de los estudiantes: esa es la línea de base a superar."),
        ("¿Para qué sirve `stratify=y` en `train_test_split`?",
         ["Para mezclar las filas", "Para que train y test tengan la misma proporción de clases",
          "Para balancear las clases al 33 % cada una", "Para hacer validación cruzada"], 1,
         "Estratificar conserva las proporciones; no balancea."),
        ("Escalás las features con la media y el desvío de **todo** el dataset y después dividís en "
         "train/test. ¿Qué problema hay?",
         ["Ninguno", "Fuga de información: el test influyó en el preprocesamiento",
          "El modelo entrena más lento", "Se pierden filas"], 1,
         "Todo lo que se ajusta (escaladores, encoders, imputadores) se ajusta solo con train."),
        ("¿Qué hace el TP si llega un CSV con una categoría desconocida en `Institutional_Policy`?",
         ["La ignora", "La convierte en NaN", "`validate` levanta `ValueError`", "La agrega al encoder"], 2,
         "Mejor frenar el pipeline con un error claro que entrenar o predecir con datos inesperados."),
    ],
    "R2": [
        ("¿Por qué el TP usa F1 macro y no accuracy?",
         ["Es más rápido de calcular", "Las clases están desbalanceadas y queremos que todas pesen igual",
          "Accuracy no existe para 3 clases", "Lo pide XGBoost"], 1,
         "Con accuracy, acertar mucho en Medium tapa los errores en High, que es la clase que más importa."),
        ("Un árbol da F1 0,99 en train y 0,48 en validación. ¿Qué pasa?",
         ["Subajuste", "Sobreajuste", "Fuga de información", "Está perfecto"], 1,
         "La gran diferencia train-validación es la firma del sobreajuste: el árbol memorizó."),
        ("¿Qué hiperparámetro de XGBoost limita directamente la complejidad de cada árbol?",
         ["`learning_rate`", "`max_depth`", "`subsample`", "`n_estimators`"], 1,
         "`max_depth` acota cuántas divisiones seguidas puede hacer cada árbol."),
        ("Bajás `learning_rate` de 0,2 a 0,02. ¿Qué conviene hacer con `n_estimators`?",
         ["Bajarlo", "Subirlo", "Dejarlo igual", "Ponerlo en 1"], 1,
         "Cada árbol aporta menos, así que hacen falta más árboles para llegar al mismo nivel."),
        ("¿Qué hace TPE, el muestreador de Optuna?",
         ["Prueba todas las combinaciones", "Elige al azar sin memoria",
          "Usa las pruebas anteriores para proponer zonas prometedoras", "Hace descenso por gradiente"], 2,
         "Por eso la búsqueda es más eficiente que la búsqueda en grilla o la aleatoria."),
        ("En la búsqueda con Optuna, ¿con qué datos se calcula el puntaje de cada prueba?",
         ["Con el test", "Con validación cruzada sobre train", "Con todo el dataset", "Con train sin CV"], 1,
         "El test queda guardado para evaluar una sola vez el modelo final."),
        ("El F1 macro final de AMq1 fue ≈ 0,54. ¿Cómo se interpreta?",
         ["El modelo no sirve", "Supera claramente la línea de base, pero estas features tienen un techo",
          "Hay fuga de información", "Falta entrenar más épocas"], 1,
         "Varios modelos distintos llegaron al mismo nivel: el límite está en la información de los datos."),
        ("¿Qué tiene de malo elegir hiperparámetros mirando el F1 en test?",
         ["Nada", "El test deja de ser una estimación honesta del rendimiento en datos nuevos",
          "Es más lento", "XGBoost no lo permite"], 1,
         "Usar el test para decidir lo convierte en un conjunto de validación más."),
    ],
    "C1": [
        ("¿Qué describe mejor a MLOps?",
         ["Un framework de deep learning", "Prácticas para llevar modelos a producción y mantenerlos",
          "Un lenguaje de programación", "Un servicio de la nube"], 1,
         "Combina ML, ingeniería de software y operaciones."),
        ("Un equipo reentrena a mano cada mes corriendo notebooks. ¿Nivel de madurez?",
         ["0", "1", "2", "3"], 0,
         "Si el pipeline no está automatizado, es nivel 0."),
        ("Según 'Hidden Technical Debt in ML Systems', ¿qué parte de un sistema de ML es el código del "
         "modelo?",
         ["Casi todo", "La mitad", "Una parte chica", "Nada"], 2,
         "El resto (datos, configuración, monitoreo, infraestructura) es lo que más deuda acumula."),
        ("Las constantes del TP (semilla, features) estaban copiadas en 7 notebooks. ¿Qué principio "
         "violaba eso?",
         ["KISS", "DRY", "YAGNI", "SOLID"], 1,
         "*Don't Repeat Yourself*: ahora viven solo en `config.py`."),
        ("¿Qué herramienta del TP detecta imports sin usar y problemas de estilo PEP 8?",
         ["pytest", "ruff", "MLflow", "Docker"], 1,
         "`ruff check .` es el linter; `pytest` corre los tests."),
        ("¿Qué asegura el test `test_entrenamiento_determinista`?",
         ["Que el modelo sea el mejor posible", "Que entrenar dos veces dé exactamente el mismo resultado",
          "Que no haya nulos", "Que MLflow esté levantado"], 1,
         "Vigila la reproducibilidad: misma semilla, mismos hilos, mismo modelo."),
        ("¿Por qué el TP fija `XGB_N_JOBS = 4` en lugar de usar `n_jobs=-1`?",
         ["Para entrenar más rápido", "Porque con `hist` la cantidad de hilos cambia levemente el resultado",
          "Porque Docker solo tiene 4 CPUs", "Por una regla de PEP 8"], 1,
         "El orden de las sumas de punto flotante depende de los hilos; fijarlos da el mismo modelo en "
         "cualquier máquina."),
        ("¿Cuál es el flujo recomendado para que dos integrantes trabajen en paralelo?",
         ["Editar los dos en `main`", "Una rama cada uno y Pull Requests revisados",
          "Turnarse por días", "Copiar el repo en un pendrive"], 1,
         "Las ramas aíslan los cambios y el PR permite revisar antes de unir."),
    ],
    "C2": [
        ("¿Cuál es la relación entre imagen y contenedor?",
         ["Son lo mismo", "El contenedor es una instancia en ejecución de una imagen",
          "La imagen es una instancia del contenedor", "La imagen es una VM"], 1,
         "Imagen = plantilla inmutable; contenedor = proceso corriendo a partir de ella."),
        ("¿Por qué un contenedor arranca mucho más rápido que una máquina virtual?",
         ["Usa menos RAM por magia", "Comparte el kernel del sistema anfitrión",
          "Está escrito en Go", "No tiene sistema de archivos"], 1,
         "No tiene que arrancar un sistema operativo completo."),
        ("En un Dockerfile, ¿por qué se copia `requirements.txt` y se instala **antes** de `COPY . .`?",
         ["Por orden alfabético", "Para aprovechar la caché de capas: cambiar el código no reinstala todo",
          "Porque es obligatorio", "Para que la imagen pese menos"], 1,
         "Las capas se reconstruyen desde la primera que cambió."),
        ("El compose tiene `ports: \"5001:5000\"` en MLflow. ¿Qué URL usa **Airflow** (otro contenedor)?",
         ["http://localhost:5001", "http://localhost:5000", "http://mlflow:5000", "http://mlflow:5001"], 2,
         "Entre contenedores se usa el nombre del servicio y el puerto interno. 5001 es solo para el host."),
        ("¿Qué pasa con los datos de PostgreSQL si borrás el contenedor y no hay volumen?",
         ["Se guardan en la imagen", "Se pierden", "Se suben a GitHub", "Pasan a MinIO"], 1,
         "El sistema de archivos del contenedor es descartable: lo persistente va en volúmenes."),
        ("¿Qué comando levanta todos los servicios del TP en segundo plano?",
         ["`docker run all`", "`docker compose --profile all up -d`", "`docker build .`",
          "`docker start airflow`"], 1,
         "`-d` (*detached*) los deja corriendo en segundo plano."),
        ("En el TP, ¿qué hace el montaje `./src:/opt/airflow/src:ro`?",
         ["Copia el código a la imagen", "Comparte el paquete del TP con Airflow, solo lectura",
          "Instala dependencias", "Abre un puerto"], 1,
         "Los DAGs importan `burnout` desde ahí, y `:ro` evita que el contenedor lo modifique."),
        ("¿Qué necesita Docker Desktop en Windows para correr contenedores Linux?",
         ["Nada", "WSL 2 (y virtualización activa)", "Una GPU", "Python 3.12"], 1,
         "Docker Desktop usa una VM liviana de Linux a través de WSL 2."),
    ],
    "C3": [
        ("¿Qué se guarda como **parámetro** en MLflow?",
         ["El F1 en test", "`max_depth=2`", "El gráfico de importancia", "El modelo serializado"], 1,
         "Los parámetros son entradas; el F1 es una métrica; el gráfico y el modelo, artefactos."),
        ("En el docker-compose del TP, ¿dónde quedan los artefactos de MLflow?",
         ["En PostgreSQL", "En MinIO, bucket `s3://mlflow`", "En Valkey", "En el contenedor de Airflow"], 1,
         "PostgreSQL guarda metadatos; MinIO, los archivos."),
        ("¿Para qué sirven los runs anidados en la búsqueda con Optuna?",
         ["Para entrenar más rápido", "Para agrupar las pruebas bajo un run padre",
          "Para que Optuna funcione", "Para registrar el modelo"], 1,
         "En la UI se ve el run `optuna_search` con un hijo por prueba."),
        ("¿Qué URI carga siempre el modelo de producción, sin cambiar el código?",
         ["`runs:/<id>/model`", "`models:/burnout_model_prod/1`", "`models:/burnout_model_prod@champion`",
          "`s3://mlflow/model.pkl`"], 2,
         "El alias se mueve a la versión nueva y el código sigue igual."),
        ("Entrenás un modelo nuevo, mejor que el actual. ¿Cómo lo promovés a producción?",
         ["Borrando la versión vieja", "Moviendo el alias `champion` a la versión nueva",
          "Renombrando el experimento", "Reiniciando MLflow"], 1,
         "Promover es mover un alias. Volver atrás también."),
        ("¿Qué ventaja da el Model Registry respecto de guardar un `.pkl` en una carpeta?",
         ["Ninguna", "Versionado y trazabilidad: cada versión apunta al run, sus datos y métricas",
          "Los modelos pesan menos", "Entrena solo"], 1,
         "Sabés qué datos, código y parámetros produjeron cada versión."),
        ("¿Cuándo conviene `mlflow.autolog()`?",
         ["Siempre en producción", "Para explorar rápido sin escribir cada `log_*`",
          "Nunca", "Solo con deep learning"], 1,
         "En el TP registramos a mano para controlar exactamente qué queda guardado."),
        ("Al registrar el XGBoost con MLflow 3 apareció `MlflowException` por tipos no confiables. "
         "¿Cómo se resolvió?",
         ["Bajando de versión", "Declarando `skops_trusted_types` con los tipos de XGBoost",
          "Guardándolo con pickle a mano", "Usando otro modelo"], 1,
         "skops solo carga tipos declarados como confiables."),
    ],
    "C4": [
        ("¿Qué significa la A de DAG y por qué importa?",
         ["Automático: corre solo", "Acíclico: sin ciclos, para que exista un orden de ejecución",
          "Asíncrono", "Airflow"], 1,
         "Con un ciclo, ninguna tarea podría empezar."),
        ("¿Qué conviene pasar por XCom entre `split` y `train`?",
         ["El DataFrame completo", "La ruta en S3 del dataset y un resumen chico",
          "El modelo entrenado", "Nada, no se puede"], 1,
         "XCom es para metadatos chicos. Los datos viajan por MinIO."),
        ("¿Qué expresión cron corre un DAG todos los lunes a las 8:00?",
         ["`0 8 * * 1`", "`8 0 * * 1`", "`0 8 1 * *`", "`* 8 * * 1`"], 0,
         "Minuto 0, hora 8, cualquier día del mes, cualquier mes, día de semana 1 (lunes)."),
        ("En Airflow 3, ¿cómo se indica que un DAG solo corre a mano?",
         ["`schedule_interval=None`", "`schedule=None`", "`manual=True`", "No se puede"], 1,
         "`schedule_interval` ya no existe en Airflow 3."),
        ("¿Por qué `import xgboost` va **dentro** de la tarea y no arriba del archivo del DAG?",
         ["Por estilo", "Porque el scheduler parsea los DAGs seguido y los imports pesados lo frenan",
          "Porque Airflow no soporta xgboost", "Para que falle menos"], 1,
         "Arriba solo van imports livianos."),
        ("La tarea `split` falla por un corte de red y Airflow la reintenta. ¿Qué propiedad hace que "
         "eso sea seguro?",
         ["Concurrencia", "Idempotencia", "Paralelismo", "Escalabilidad"], 1,
         "Si reescribe los mismos archivos con el mismo resultado, reintentar no ensucia nada."),
        ("En el TP, ¿qué componente ejecuta realmente cada tarea?",
         ["El scheduler", "El worker de Celery", "PostgreSQL", "MinIO"], 1,
         "El scheduler decide y encola (en Valkey); el worker ejecuta."),
        ("¿Por qué los DAGs del TP son 'envoltorios finos' de funciones de `burnout.etl`?",
         ["Por moda", "Para poder testear la lógica con pytest sin levantar Airflow",
          "Porque Airflow lo exige", "Para que corran más rápido"], 1,
         "Así la lógica se prueba con un S3 falso, como en esta clase y en `tests/test_etl.py`."),
    ],
    "C5": [
        ("Un banco calcula cada noche el riesgo crediticio de todos sus clientes. ¿Qué tipo de "
         "predicción es?",
         ["Online", "Batch", "Streaming", "Shadow"], 1,
         "Se precalcula en lote y en horario fijo."),
        ("Detectar fraude en una compra con tarjeta, antes de aprobarla, requiere…",
         ["Batch semanal", "Predicción online de baja latencia", "Un DAG mensual", "Nada de ML"], 1,
         "La decisión se toma en milisegundos, con datos de esa transacción."),
        ("¿Por qué 10.000 predicciones en una llamada son más rápidas que 10.000 llamadas de 1 fila?",
         ["Por la caché del disco", "Se reparte el costo fijo de cada llamada y se vectoriza",
          "Porque XGBoost hace trampa", "No son más rápidas"], 1,
         "Lo viste en el control 🎛️ de la clase."),
        ("En el patrón de la clase 5, ¿cómo responde el servicio cuando le piden una predicción?",
         ["Entrena el modelo", "Busca la predicción precalculada en un almacén clave-valor",
          "Llama a Airflow", "Lee el CSV crudo"], 1,
         "Servir es una búsqueda O(1), sin cargar el modelo."),
        ("¿Cuál es la principal desventaja del batch?",
         ["Es caro", "Las predicciones pueden quedar desactualizadas o faltar para registros nuevos",
          "Necesita GPU", "No se puede automatizar"], 1,
         "Un estudiante nuevo no tiene predicción hasta la próxima corrida."),
        ("Querés probar un modelo nuevo con el tráfico real, **sin** que sus respuestas afecten a nadie. "
         "¿Qué estrategia usás?",
         ["Blue/green", "Canary", "Shadow", "Big bang"], 2,
         "En shadow el modelo predice en paralelo y solo se compara."),
        ("Pasás el 5 % del tráfico al modelo nuevo y lo subís de a poco si va bien. Eso es…",
         ["Canary", "Shadow", "Blue/green", "Batch"], 0,
         "Como el canario en la mina: avisa temprano si algo anda mal."),
        ("¿Qué modelo carga el DAG `batch_predict_burnout`?",
         ["El último entrenado", "`models:/burnout_model_prod@champion`", "Un `.pkl` del repo",
          "El de AMq1 directamente"], 1,
         "Así, cuando se promueve un challenger, el batch lo toma solo en la próxima corrida."),
    ],
}
