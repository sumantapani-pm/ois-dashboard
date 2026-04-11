import subprocess
import sys
import os
from dotenv import load_dotenv
from prefect import flow, task
from prefect.logging import get_run_logger

load_dotenv()

@task(retries=2, retry_delay_seconds=30)
def run_ingestion(client_id: str, file_path: str):
    logger = get_run_logger()
    logger.info(f"Starting ingestion for {client_id}")
    result = subprocess.run(
        [sys.executable,
         "ingestion/sources/csv_loader.py",
         client_id, file_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Ingestion failed: {result.stderr}")
    logger.info(result.stdout)

@task(retries=1)
def run_dbt_models():
    logger = get_run_logger()
    logger.info("Running dbt models and tests")
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "ois_models"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

    test_result = subprocess.run(
        ["dbt", "test", "--project-dir", "ois_models"],
        capture_output=True, text=True
    )
    if test_result.returncode != 0:
        raise Exception(f"dbt tests FAILED: {test_result.stderr}")
    logger.info("All dbt tests passed")

@task(retries=1)
def run_anomaly_detection():
    logger = get_run_logger()
    logger.info("Running anomaly detection")
    result = subprocess.run(
        [sys.executable,
         "backend/api/services/threshold-engine/detector.py"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Detection failed: {result.stderr}")
    logger.info(result.stdout)

@flow(name="OIS Daily Pipeline")
def daily_pipeline(
    client_id: str = "client_001",
    file_path: str = "data/sample_inventory.csv"
):
    run_ingestion(client_id, file_path)
    run_dbt_models()
    run_anomaly_detection()

if __name__ == "__main__":
    daily_pipeline()