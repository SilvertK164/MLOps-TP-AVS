"""Constantes del proyecto: esquema del dataset, features, semilla y nombres de MLflow/S3.

Todo lo que en el TP de Aprendizaje de Máquina I estaba repetido al principio de cada
notebook vive acá, en un solo lugar.
"""

from pathlib import Path

SEED = 42
TEST_SIZE = 0.2

# --- Rutas locales -----------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw" / "ai_student_impact_dataset.csv"

# --- Esquema del dataset -----------------------------------------------------
ID_COL = "Student_ID"
TARGET_COL = "Burnout_Risk_Level"

NUMERIC = [
    "Pre_Semester_GPA",
    "Weekly_GenAI_Hours",
    "Tool_Diversity",
    "Traditional_Study_Hours",
    "Perceived_AI_Dependency",
    "Anxiety_Level_During_Exams",
    "Post_Semester_GPA",
    "Skill_Retention_Score",
]
BOOLEAN = ["Paid_Subscription"]
# Categorías de menor a mayor: el orden define la codificación ordinal.
ORDINAL = {
    "Year_of_Study": ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
    "Prompt_Engineering_Skill": ["Beginner", "Intermediate", "Advanced"],
    TARGET_COL: ["Low", "Medium", "High"],
}
NOMINAL = {
    "Major_Category": ["STEM", "Business", "Humanities", "Medical", "Arts"],
    "Primary_Use_Case": [
        "Copywriting/Drafting",
        "Summarizing_Reading",
        "Debugging/Troubleshooting",
        "Ideation",
        "Direct_Answer_Generation",
    ],
    # En el CSV es "Strict_Ban" (la descripción de Kaggle dice "Strictly_Ban").
    "Institutional_Policy": ["Allowed_With_Citation", "Strict_Ban", "Actively_Encouraged"],
}
EXPECTED_COLUMNS = {ID_COL, *NUMERIC, *BOOLEAN, *ORDINAL, *NOMINAL}

LABELS = ORDINAL[TARGET_COL]

# Variables de resultado: se miden al final del semestre, a la vez que el burnout.
# Usarlas como features sería fuga de información.
OUTCOMES = ["Post_Semester_GPA", "Skill_Retention_Score", TARGET_COL]

FEATURES = {
    "numeric": [c for c in NUMERIC if c not in OUTCOMES],
    "boolean": list(BOOLEAN),
    "ordinal": [c for c in ORDINAL if c not in OUTCOMES],
    "nominal": list(NOMINAL),
}
FEATURE_COLUMNS = [col for cols in FEATURES.values() for col in cols]

# --- Modelo ------------------------------------------------------------------
# Mejores hiperparámetros encontrados con Optuna (40 pruebas, F1 macro CV = 0,5385)
# en notebooks/06_xgboost.ipynb del TP de AMq1.
BEST_PARAMS_AMQ1 = {
    "n_estimators": 250,
    "learning_rate": 0.20120427602913063,
    "max_depth": 2,
    "min_child_weight": 4,
    "subsample": 0.6105185401792286,
    "colsample_bytree": 0.6887516072173432,
    "reg_alpha": 0.09529571803968918,
    "reg_lambda": 0.010075954466353133,
    "gamma": 3.6505474359101213,
}
# Hilos de XGBoost fijos: con tree_method="hist" el resultado cambia levemente según la
# cantidad de hilos (el orden de las sumas de punto flotante). Con n_jobs=-1, una laptop y
# un contenedor con otra cantidad de CPUs darían F1 distintos (vimos de 0,5358 a 0,5380).
XGB_N_JOBS = 4

# --- MLflow ------------------------------------------------------------------
EXPERIMENT_NAME = "Burnout Risk"
REGISTERED_MODEL = "burnout_model_prod"
CHAMPION_ALIAS = "champion"
# MLflow 3 serializa los modelos de scikit-learn con skops, que solo carga tipos declarados
# como confiables: XGBoost no está en su lista por defecto.
SKOPS_TRUSTED_TYPES = ["xgboost.core.Booster", "xgboost.sklearn.XGBClassifier"]

# --- Data Lake (MinIO / S3) --------------------------------------------------
BUCKET = "data"
S3_PREFIX = "burnout"
S3_KEYS = {
    "raw": f"{S3_PREFIX}/raw/ai_student_impact_dataset.csv",
    "X_train": f"{S3_PREFIX}/final/train/X_train.csv",
    "y_train": f"{S3_PREFIX}/final/train/y_train.csv",
    "X_test": f"{S3_PREFIX}/final/test/X_test.csv",
    "y_test": f"{S3_PREFIX}/final/test/y_test.csv",
    "data_info": f"{S3_PREFIX}/data_info/data.json",
    "batch_input": f"{S3_PREFIX}/batch/input.csv",
    "batch_output": f"{S3_PREFIX}/batch/predictions.csv",
}
