"""
config.py — Central configuration for Mutual Fund Analytics
All scheme codes, paths, and constants live here.
"""

# ── API ──────────────────────────────────────────────────────────
MFAPI_BASE = "https://api.mfapi.in/mf"

# ── Key Schemes ──────────────────────────────────────────────────
KEY_SCHEMES = {
    125497: "HDFC Top 100 Direct",
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip",
}

# ── Expected CSV Files ───────────────────────────────────────────
EXPECTED_CSVS = [
    "fund_master",
    "nav_history",
    "scheme_returns",
    "benchmark_returns",
    "category_avg",
    "risk_metrics",
    "aum_data",
    "redemption_data",
    "sip_data",
    "portfolio_holdings",
]

# ── Paths ─────────────────────────────────────────────────────────
DATA_RAW       = "data/raw"
DATA_PROCESSED = "data/processed"
REPORTS_DIR    = "reports"
SQL_DIR        = "sql"
DASH_DIR       = "dashboard"
NOTEBOOKS_DIR  = "notebooks"

DIRS = [DATA_RAW, DATA_PROCESSED, REPORTS_DIR, SQL_DIR, DASH_DIR, NOTEBOOKS_DIR]
