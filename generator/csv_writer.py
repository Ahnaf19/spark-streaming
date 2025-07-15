from loguru import logger
import csv
import os
import time
import random
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/input")
os.makedirs(DATA_DIR, exist_ok=True)

def generate_csv(file_index, rows=10):
    """
    Generates a CSV file with random event data.
    Each file contains 10 rows of data with timestamp, user_id, and event type.
    """
    logger.info(f"Generating CSV file {file_index}...")
    file_path = os.path.join(DATA_DIR, f"event_batch_{file_index}.csv")
    with open(file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "user_id", "event"])
        for _ in range(rows):
            writer.writerow([
                datetime.now().isoformat(),
                random.randint(1, 5),
                random.choice(["login", "logout", "purchase", "view"])
            ])
    logger.success(f"Generated CSV: {file_path}")

if __name__ == "__main__":
    logger.info("Starting CSV generation...")
    for i in range(10):
        generate_csv(i)
        time.sleep(3)
    logger.info("CSV generation complete.")
