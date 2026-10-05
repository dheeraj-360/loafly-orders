import os


def _load_env_file(path=".env"):
    """Minimal .env file reader — stdlib only, no external packages."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


_load_env_file()

CURRENCY = "INR"
DISCOUNT_PERCENT = 10
INPUT_CSV_PATH = "data/raw_orders.csv"
LOG_FILE_PATH = "logs/loafly.log"
MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 1

API_KEY = os.getenv("LOAFLY_API_KEY")