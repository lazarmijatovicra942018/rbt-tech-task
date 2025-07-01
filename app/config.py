import os
from pathlib import Path

class Config:
    """
    Application-wide configuration settings for Flask, APScheduler,
    database connection, file paths, and conversion constants.
    """

    # Scheduler
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE     = os.getenv('SCHEDULER_TIMEZONE', 'UTC')
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1,
    }
    JOBS = [
        {
            'id': 'import_job',
            'func': 'app.services.csv_service:CSVService.import_all',
            'trigger': 'interval',
            'hours': 1,
        },
    ]

    # Database
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST]):
        raise RuntimeError("Missing one or more required database environment variables.")

    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"


    # --- Data directories (all absolute) ---
    HERE         = Path(__file__).resolve().parent
    PROJECT_ROOT = HERE.parents[0]
    DATA_DIR     = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
    PROCESSED_DIR= DATA_DIR / "processed"
    ERRORED_DIR  = DATA_DIR / "errored"

    # --- Conversion rates ---
    NEURO_PER_USD = float(os.getenv("NEURO_PER_USD", 0.90))
    SQM_PER_ACRE  = float(os.getenv("SQM_PER_ACRE", 4047.0))
    SQM_PER_SQFT  = float(os.getenv("SQM_PER_SQFT", 0.092903))