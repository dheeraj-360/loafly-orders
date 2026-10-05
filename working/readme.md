# Loafly Orders Pipeline

A production-ready refactor of Loafly's nightly order-processing script.

## Background

The original script (starter/legacy_orders.py) read the day's orders, cleaned
prices, applied a discount, and saved each order — but lived in one file, had no
error handling, crashed on the first missing price, and had the API key hardcoded
in the source. This package fixes all of that.

## What changed

- **Functions** — price cleaning and discount logic pulled into clean_price()
  and apply_discount() instead of being copy-pasted inline.
- **OOP** — orders are modeled as an Order class (order_id, customer,
  items, add_item(), total()) instead of loose dictionaries.
- **Package structure** — split into one module per responsibility.
- **Config-driven** — currency, discount %, file paths, and retry settings all
  live in config.py, not scattered through the logic.
- **Logging** — every print() replaced with proper logging (INFO/WARNING/
  ERROR), written both to the console and to logs/loafly.log.
- **Error handling** — a missing or invalid price is caught, logged as a
  warning, and skipped — the run no longer crashes on one bad row.
- **Retry + secrets** — the flaky save_to_orders_api() call is retried a few
  times before giving up; the API key is read from the environment via
  os.getenv, never hardcoded.

## Project structure

working/
├── data/
│   └── raw_orders.csv       # the day's raw orders
├── logs/
│   └── loafly.log           # written automatically on each run
├── loafly/                  # the package
│   ├── __init__.py
│   ├── config.py            # all settings, reads .env
│   ├── models.py            # Order class
│   ├── extract.py           # CSV -> Order objects
│   ├── transform.py         # clean_price, apply_discount, skip bad items
│   ├── load.py               # save each order, with retry
│   └── gateway.py           # provided flaky API client (not edited)
├── run_pipeline.py          # entry point: extract -> transform -> load
├── .env                     # real API key (never committed)
├── .env.example             # template, safe to commit
├── .gitignore
├── requirements.txt
└── README.md

## Setup

1. Create a virtual environment:
   python -m venv .venv
2. Activate it:
   - Windows: .venv\Scripts\Activate.ps1
   - Mac/Linux: source .venv/bin/activate
3. Copy .env.example to .env and fill in the real LOAFLY_API_KEY.
4. No external packages needed — standard library only (see requirements.txt).

## Run

From this folder:
    py run_pipeline.py

## What to expect

- 15 orders are read from the CSV.
- 3 items have missing prices on purpose — each is skipped with a logged
  warning, the rest of that order still processes normally.
- Saving to the orders API fails randomly about 30% of the time by design;
  each save is retried up to MAX_RETRIES times (set in config.py) before
  giving up and logging an error for that order.
- Full details of every run are written to logs/loafly.log.