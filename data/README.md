# Datos

## Fuente

- **Dataset:** Impact of AI on Students — *"Is AI a Tutor or a Cheat Code? 50,000 Student Records on GenAI Usage and Burnout"*
- **Autor:** Lavesh Jadon
- **URL:** https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students
- **Versión:** 1.0 (mayo de 2026)
- **Licencia:** CC0 1.0 (dominio público): se puede versionar y redistribuir.

## Archivo

`raw/ai_student_impact_dataset.csv`: 50.000 filas × 16 columnas, sin nulos, 5.892.478 bytes.

SHA-256: `4D911088C4B12D60A450A9ACAE6B606F4119EBBB48679518E427A4FC00778472`

Para verificar que tenés el mismo archivo (PowerShell):

    Get-FileHash data\raw\ai_student_impact_dataset.csv

**No editar el CSV.** Toda transformación la hacemos en código, dentro de los notebooks.

## Diccionario de columnas

| Columna | Tipo | Valores | Descripción |
|---|---|---|---|
| `Student_ID` | entero | 100001–150000 | Identificador (no se usa como feature) |
| `Major_Category` | nominal | STEM, Business, Humanities, Medical, Arts | Área de estudio |
| `Year_of_Study` | ordinal | Freshman < Sophomore < Junior < Senior < Graduate | Año de cursada |
| `Pre_Semester_GPA` | real | 1.18–4.00 | Promedio al inicio del semestre |
| `Weekly_GenAI_Hours` | real | 0–40 | Horas semanales usando IA generativa |
| `Primary_Use_Case` | nominal | Copywriting/Drafting, Summarizing_Reading, Debugging/Troubleshooting, Ideation, Direct_Answer_Generation | Uso principal de la IA |
| `Prompt_Engineering_Skill` | ordinal | Beginner < Intermediate < Advanced | Habilidad autopercibida para escribir prompts |
| `Tool_Diversity` | entero | 1–5 | Cantidad de herramientas de IA distintas |
| `Paid_Subscription` | booleano | True / False | Tiene suscripción paga |
| `Traditional_Study_Hours` | real | 1–35.9 | Horas semanales de estudio sin IA |
| `Perceived_AI_Dependency` | entero | 1–10 | Dependencia autopercibida de la IA |
| `Institutional_Policy` | nominal | Allowed_With_Citation, Strict_Ban, Actively_Encouraged | Política de la institución sobre IA |
| `Anxiety_Level_During_Exams` | entero | 1–10 | Ansiedad autorreportada en exámenes |
| `Post_Semester_GPA` | real | 1.00–4.00 | Promedio al final del semestre (**objetivo posible**, regresión) |
| `Skill_Retention_Score` | real | 10.8–100 | Retención de habilidades (**objetivo posible**, regresión) |
| `Burnout_Risk_Level` | ordinal | Low (33 %) < Medium (42 %) < High (25 %) | Riesgo de burnout (**objetivo posible**, clasificación) |

## Advertencias

- En el CSV la política restrictiva es `Strict_Ban`; la descripción de Kaggle dice `Strictly_Ban`. El código usa el valor real.
- Los datos son **probablemente sintéticos** (sin faltantes, distribuciones prolijas, publicación reciente). Hay que decirlo en la propuesta y en la reflexión final.
- `Post_Semester_GPA` tiene techo en 4.0.
