# Clases interactivas

Notebooks para repasar AMq1 y aprender cada tema de MLOps **usando nuestro propio TP**. Cada clase
mezcla teoría corta, controles interactivos 🎛️ (deslizadores y menús), preguntas de opción múltiple y
ejercicios ✏️ con verificación automática (✅ / ⏳ con pista). La solución está plegada debajo de cada
ejercicio.

| Notebook | Tema | Duración aprox. |
|---|---|---|
| [R1_repaso_datos_y_preprocesamiento](R1_repaso_datos_y_preprocesamiento.ipynb) | Repaso AMq1: el problema, fuga de información, codificación, split estratificado | 30 min |
| [R2_repaso_modelos_y_optuna](R2_repaso_modelos_y_optuna.ipynb) | Repaso AMq1: métricas, sobreajuste, hiperparámetros de XGBoost, Optuna | 40 min |
| [C1_mlops_buenas_practicas](C1_mlops_buenas_practicas.ipynb) | Clase 1: MLOps, del notebook al paquete, tests, linters, reproducibilidad, Git | 40 min |
| [C2_docker](C2_docker.ipynb) | Clase 2: imágenes, contenedores, Dockerfile, el docker-compose del TP | 40 min |
| [C3_mlflow](C3_mlflow.ipynb) | Clase 3: tracking, autolog, runs anidados, Model Registry champion/challenger | 45 min |
| [C4_airflow](C4_airflow.ipynb) | Clase 4: DAGs, TaskFlow, XCom, cron; corremos la lógica del ETL con un S3 falso | 40 min |
| [C5_batch_y_despliegue](C5_batch_y_despliegue.ipynb) | Clase 5: batch vs online, almacén clave-valor, estrategias de despliegue | 35 min |

## Cómo usarlas

Desde la raíz del repo, con el entorno activado (ver el README principal):

```bash
jupyter lab clases/
```

- Abrí la clase y ejecutá las celdas en orden (`Shift + Enter`).
- Los controles 🎛️ necesitan Jupyter (Lab, Notebook o VS Code). En la vista de GitHub se ven
  estáticos.
- Si un ejercicio queda sin resolver, el notebook igual corre hasta el final.
- Todo lo que generan las clases (bases de MLflow, archivos del "S3 falso") va a `clases/_salidas/`,
  que está en `.gitignore`. Se puede borrar cuando quieras.

Ninguna clase necesita Docker. La C2 y la C4 explican cómo correr lo mismo con el entorno de Docker.
