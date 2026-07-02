"""
Incrementally ingest new customer data into the training dataset.
"""

import logging
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA = BASE_DIR / "data/raw/telco_customer_churn.csv"
INCOMING_DIR = BASE_DIR / "data/incoming"
ARCHIVE_DIR = BASE_DIR / "data/archive"
CLEAN_SCRIPT = Path(__file__).with_name("clean_data.py")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def ingest():

    RAW_DATA.parent.mkdir(parents=True, exist_ok=True)
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    incoming_files = sorted(INCOMING_DIR.glob("*.csv"))

    if not incoming_files:
        logging.info("No new datasets found.")
        return

    if RAW_DATA.exists():
        dataset = pd.read_csv(RAW_DATA)
    else:
        dataset = pd.DataFrame()

    for file in incoming_files:
        logging.info("Merging %s", file.name)

        new_data = pd.read_csv(file)

        dataset = (
            pd.concat([dataset, new_data], ignore_index=True)
            .drop_duplicates()
        )

        shutil.move(file, ARCHIVE_DIR / file.name)

    dataset.to_csv(RAW_DATA, index=False)

    logging.info("Raw dataset updated (%d rows).", len(dataset))

    subprocess.run(
        [sys.executable, str(CLEAN_SCRIPT)],
        check=True,
    )

    logging.info("Processed dataset regenerated.")


if __name__ == "__main__":
    ingest()