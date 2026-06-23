"""
utils.py — Shared helpers for Mutual Fund Analytics
"""

import os
import sys
import json
import time
import requests
import pandas as pd
from datetime import datetime
from config import MFAPI_BASE, KEY_SCHEMES, DIRS


# ── Terminal colours ──────────────────────────────────────────────
class C:
    BOLD  = "\033[1m"
    GREEN = "\033[92m"
    YELLOW= "\033[93m"
    RED   = "\033[91m"
    CYAN  = "\033[96m"
    RESET = "\033[0m"

def ok(msg):   print(f"{C.GREEN}  ✅ {msg}{C.RESET}")
def warn(msg): print(f"{C.YELLOW}  ⚠️  {msg}{C.RESET}")
def err(msg):  print(f"{C.RED}  ❌ {msg}{C.RESET}")
def info(msg): print(f"{C.CYAN}  ℹ  {msg}{C.RESET}")
def hdr(msg):  print(f"\n{C.BOLD}{'═'*60}\n  {msg}\n{'═'*60}{C.RESET}")


# ── Folder setup ──────────────────────────────────────────────────
def ensure_dirs():
    for d in DIRS:
        os.makedirs(d, exist_ok=True)


# ── NAV fetcher ───────────────────────────────────────────────────
def fetch_nav(scheme_code: int, scheme_name: str, retries: int = 3) -> pd.DataFrame | None:
    url = f"{MFAPI_BASE}/{scheme_code}"
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            raw  = r.json()
            meta = raw.get("meta", {})
            df   = pd.DataFrame(raw.get("data", []))
            if df.empty:
                warn(f"No data returned for {scheme_name}")
                return None
            df["scheme_code"]     = scheme_code
            df["scheme_name"]     = scheme_name
            df["fund_house"]      = meta.get("fund_house", "")
            df["scheme_type"]     = meta.get("scheme_type", "")
            df["scheme_category"] = meta.get("scheme_category", "")
            df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
            df["nav"]  = pd.to_numeric(df["nav"], errors="coerce")
            df = df.sort_values("date").reset_index(drop=True)
            return df
        except Exception as e:
            if attempt < retries:
                warn(f"Attempt {attempt} failed for {scheme_name}: {e}. Retrying…")
                time.sleep(2)
            else:
                err(f"All retries failed for {scheme_name}: {e}")
                return None


# ── Data quality check ────────────────────────────────────────────
def quality_report(df: pd.DataFrame, name: str) -> dict:
    nulls      = df.isnull().sum()
    dupes      = df.duplicated().sum()
    null_cols  = nulls[nulls > 0].to_dict()
    return {
        "dataset":        name,
        "rows":           len(df),
        "columns":        len(df.columns),
        "null_cells":     int(nulls.sum()),
        "null_by_col":    null_cols,
        "duplicate_rows": int(dupes),
    }


# ── Save helper ───────────────────────────────────────────────────
def save_csv(df: pd.DataFrame, path: str, label: str = ""):
    df.to_csv(path, index=False)
    ok(f"{'Saved' if not label else label} → {path}  ({len(df):,} rows)")
