"""
live_nav_fetch.py — Fetch live NAV from mfapi.in
Capstone Project I — Mutual Fund Analytics

Usage:
    python live_nav_fetch.py                  # all 6 key schemes
    python live_nav_fetch.py --scheme 125497  # single scheme
    python live_nav_fetch.py --list           # list available schemes
"""

import argparse
import sys
import pandas as pd
from datetime import datetime

from config import KEY_SCHEMES, DATA_RAW
from utils import ensure_dirs, fetch_nav, save_csv, ok, warn, err, hdr, C


def list_schemes():
    hdr("Available Key Schemes")
    print(f"  {'Code':<10} {'Scheme Name'}")
    print(f"  {'-'*8}   {'-'*30}")
    for code, name in KEY_SCHEMES.items():
        print(f"  {code:<10} {name}")


def run(codes: list[int]):
    hdr(f"Live NAV Fetch — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ensure_dirs()
    all_dfs = []

    for code in codes:
        name = KEY_SCHEMES.get(code, f"Scheme {code}")
        print(f"\n  📡 {C.BOLD}{name}{C.RESET}  (code: {code})")
        df = fetch_nav(code, name)
        if df is not None:
            out = f"{DATA_RAW}/nav_{code}.csv"
            save_csv(df, out)
            latest = df.iloc[-1]
            ok(f"Latest NAV : ₹{latest['nav']:.4f}  on  {latest['date'].date()}")
            ok(f"Total records: {len(df):,}")
            all_dfs.append(df)
        else:
            err(f"Could not fetch {name}")

    if len(all_dfs) > 1:
        combined = pd.concat(all_dfs, ignore_index=True)
        save_csv(combined, f"{DATA_RAW}/all_nav_combined.csv", "Combined NAV")

    hdr("Summary Table")
    rows = []
    for df in all_dfs:
        latest = df.iloc[-1]
        rows.append({
            "Code":     df["scheme_code"].iloc[0],
            "Scheme":   df["scheme_name"].iloc[0],
            "Latest":   str(latest["date"].date()),
            "NAV (₹)":  round(float(latest["nav"]), 4),
            "Records":  len(df),
        })
    if rows:
        print(pd.DataFrame(rows).to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description="Fetch live NAV from mfapi.in")
    parser.add_argument("--scheme", type=int, help="Single scheme code to fetch")
    parser.add_argument("--list",   action="store_true", help="List available schemes")
    args = parser.parse_args()

    if args.list:
        list_schemes()
    elif args.scheme:
        run([args.scheme])
    else:
        run(list(KEY_SCHEMES.keys()))


if __name__ == "__main__":
    main()
