from pathlib import Path
import pandas as pd
from app.models import Building
import shutil
from app.database import transactional_session
from app.services import BuildingService
import numpy as np
import logging

class CSVService:
    """
    Service to import CSV files into the Building model.
    """

    DATA_DIR      = None
    PROCESSED_DIR = None
    ERRORED_DIR   = None
    NEURO_PER_USD = None
    SQM_PER_ACRE  = None
    SQM_PER_SQFT  = None

    @classmethod
    def init_app(cls, app):
        """Pull in all config values once, at app startup."""
        cfg = app.config
        cls.DATA_DIR      = cfg["DATA_DIR"]
        cls.PROCESSED_DIR = cfg["PROCESSED_DIR"]
        cls.ERRORED_DIR   = cfg["ERRORED_DIR"]
        cls.NEURO_PER_USD   = cfg["NEURO_PER_USD"]
        cls.SQM_PER_ACRE  = cfg["SQM_PER_ACRE"]
        cls.SQM_PER_SQFT  = cfg["SQM_PER_SQFT"]

        # grab Flask's logger
        cls.logger = app.logger
        cls.logger.setLevel(logging.INFO)

        cls.logger.info(f"CSVService configured: DATA={cls.DATA_DIR}, PROCESSED={cls.PROCESSED_DIR}, ERRORED={cls.ERRORED_DIR}")


        # Ensure the directories are there before any import runs
        for directory in (
            cls.DATA_DIR,
            cls.PROCESSED_DIR,
            cls.ERRORED_DIR,
        ):
            Path(directory).mkdir(parents=True, exist_ok=True)

    @classmethod
    def _clean_transform(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter rows for sale and compute the desired columns.
        """
        return (
            df.query("status == 'for_sale'")
              .loc[:, ['price', 'bed', 'bath', 'acre_lot', 'house_size']]
              .assign(
                  price=lambda d: d.price * cls.NEURO_PER_USD,
                  rooms=lambda d: d.bed.astype('Float64'),
                  bathrooms=lambda d: d.bath.astype('Int64'),
                  land_area=lambda d: d.acre_lot * cls.SQM_PER_ACRE,
                  square_footage=lambda d: d.house_size * cls.SQM_PER_SQFT,
              )
              .loc[:, ['price', 'rooms', 'bathrooms', 'land_area', 'square_footage']]
        )

    @staticmethod
    def _to_python(v: any, target: type | None = None) -> any:
        """
        Convert pandas/NumPy scalars and NAs into native Python types.
        Optionally cast to int or float.
        """
        if pd.isna(v):
            return None
        if isinstance(v, np.generic):
            v = v.item()
        if target is int and v is not None:
            return int(v)
        if target is float and v is not None:
            return float(v)
        return v

    @classmethod
    def import_all(cls) -> None:
        """
        Process every CSV in DATA_DIR and move it based on result.
        """
        cls.logger.info("Starting import_all")
        for csv_path in cls.DATA_DIR.glob("*.csv"):
            destination = cls._process_file(csv_path)
            cls._move_file(csv_path, destination)
        cls.logger.info("Finished import_all")

    @classmethod
    def _process_file(cls, path: Path) -> Path:
        try:
            cls.logger.info(f"Processing {path.name}")
            df = pd.read_csv(path)
            df_clean = cls._clean_transform(df)


            buildings = [
                Building(
                    offer_id=1,
                    price=cls._to_python(rec['price'], float),
                    rooms=cls._to_python(rec['rooms'], float),
                    bathrooms=cls._to_python(rec['bathrooms'], int),
                    land_area=cls._to_python(rec['land_area'], float),
                    square_footage=cls._to_python(rec['square_footage'], float),
                )
                for rec in df_clean.to_dict(orient="records")
            ]

            with transactional_session() as db:
                BuildingService.bulk_create(db=db, buildings_orm=buildings)

            cls.logger.info(f" → Success importing {path.name}")
            return cls.PROCESSED_DIR / path.name

        except Exception as e:
            cls.logger.error(f"Error processing {path.name}: {e}", exc_info=True)
            return cls.ERRORED_DIR / path.name

    @staticmethod
    def _move_file(src: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))