# Clases interactivas

Notebooks para repasar AMq1 y aprender cada tema de MLOps **usando nuestro propio TP**. Cada clase
tiene la misma estructura:

| Parte | Qué hay |
|---|---|
| 📖 **Teoría** | los conceptos explicados con diagramas (Mermaid) y tablas comparativas |
| 🎛️ **Práctica guiada** | código del TP con controles interactivos (deslizadores y menús) y preguntas rápidas |
| ✏️ **Ejercicios** | con verificación automática (✅ / ⏳ con pista) y la solución plegada debajo |
| 🏭 **Casos de uso y ejemplos** | casos reales de la industria, problemas típicos para resolver (con respuesta plegada) y ejemplos de comandos y código |
| 🔁 **Tarjetas de repaso** | concepto → respuesta; marcás cuáles sabías y al final te dice qué repasar |
| 📝 **Cuestionario final** | 8 preguntas con puntaje y la explicación de cada respuesta |

La clase **C6** es un repaso integrador para la primera entrega: mapa de todo el TP, el recorrido de un
día del pipeline, glosario, un examen al azar con preguntas de todas las clases, todas las tarjetas,
preguntas de defensa oral con respuesta modelo y el checklist de la entrega.

| Notebook | Tema | Duración aprox. |
|---|---|---|
| [R1_repaso_datos_y_preprocesamiento](R1_repaso_datos_y_preprocesamiento.ipynb) | Repaso AMq1: el problema, fuga de información, codificación, split estratificado | 45 min |
| [R2_repaso_modelos_y_optuna](R2_repaso_modelos_y_optuna.ipynb) | Repaso AMq1: métricas, sobreajuste, hiperparámetros de XGBoost, Optuna | 55 min |
| [C1_mlops_buenas_practicas](C1_mlops_buenas_practicas.ipynb) | Clase 1: MLOps, del notebook al paquete, tests, linters, reproducibilidad, Git | 55 min |
| [C2_docker](C2_docker.ipynb) | Clase 2: imágenes, contenedores, Dockerfile, el docker-compose del TP | 55 min |
| [C3_mlflow](C3_mlflow.ipynb) | Clase 3: tracking, autolog, runs anidados, Model Registry champion/challenger | 60 min |
| [C4_airflow](C4_airflow.ipynb) | Clase 4: DAGs, TaskFlow, XCom, cron; corremos la lógica del ETL con un S3 falso | 55 min |
| [C5_batch_y_despliegue](C5_batch_y_despliegue.ipynb) | Clase 5: batch vs online, almacén clave-valor, estrategias de despliegue | 50 min |
| [C6_repaso_integrador_entrega_1](C6_repaso_integrador_entrega_1.ipynb) | Repaso integrador: mapa del TP, examen mezclado, tarjetas, defensa oral, checklist | 45 min |

## Cómo usarlas

Desde la raíz del repo, con el entorno activado (ver el README principal):

```bash
jupyter lab clases/
```

- Abrí la clase y ejecutá las celdas en orden (`Shift + Enter`).
- Los controles 🎛️ necesitan Jupyter (Lab, Notebook o VS Code). En la vista de GitHub se ven
  estáticos.
- Si un ejercicio queda sin resolver, el notebook igual corre hasta el final.
- Las preguntas y tarjetas están en `banco.py` (fuera de los notebooks, así no ves las respuestas
  antes de tiempo). Los widgets están en `helpers.py`.
- Los diagramas usan Mermaid: se ven en JupyterLab 4.1 o posterior (el entorno del TP trae la 4.6).
- Todo lo que generan las clases (bases de MLflow, archivos del "S3 falso") va a `clases/_salidas/`,
  que está en `.gitignore`. Se puede borrar cuando quieras.

Ninguna clase necesita Docker. La C2 y la C4 explican cómo correr lo mismo con el entorno de Docker.
