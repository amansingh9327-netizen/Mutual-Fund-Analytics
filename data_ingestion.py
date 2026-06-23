"""
data_ingestion.py — Day 1: Project Setup + Data Ingestion (ETL)
Capstone Project I — Mutual Fund Analytics

Runs end-to-end:
  1. Creates all project folders
  2. Loads & profiles every CSV dataset
  3. Fetches live NAV for 6 key schemes from mfapi.in
  4. Explores fund_master structure
  5. Validates AMFI codes across datasets
  6. Writes a data-quality report to reports/
"""

import os
import json
import sys
import pandas as pd
from datetime import datetime

from config import (
    KEY_SCHEMES, EXPECTED_CSVS,
    DATA_RAW, DATA_PROCESSED, REPORTS_DIR,
)
from utils import (
    ensure_dirs, fetch_nav, quality_report, save_csv,
    ok, warn, err, info, hdr, C,
)


# ══════════════════════════════════════════════════════════════════
# STEP 1 — FOLDER STRUCTURE
# ══════════════════════════════════════════════════════════════════
def step_folders():
    hdr("STEP 1 — Creating Folder Structure")
    ensure_dirs()
    ok("data/raw  data/processed  notebooks  sql  dashboard  reports")


# ══════════════════════════════════════════════════════════════════
# STEP 2 — LOAD CSV DATASETS
# ══════════════════════════════════════════════════════════════════
def step_load_csvs() -> dict[str, pd.DataFrame]:
    hdr("STEP 2 — Loading CSV Datasets")
    dataframes: dict[str, pd.DataFrame] = {}
    missing = []

    for name in EXPECTED_CSVS:
        path = os.path.join(DATA_RAW, f"{name}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            dataframes[name] = df
            print(f"\n  📂 {C.BOLD}{name}{C.RESET}")
            info(f"Shape   : {df.shape}")
            info(f"Columns : {list(df.columns)}")
            info(f"Dtypes  :\n{df.dtypes.to_string()}")
            info(f"Head(3) :\n{df.head(3).to_string()}")
            nulls = df.isnull().sum()
            if nulls.any():
                warn(f"Nulls   :\n{nulls[nulls > 0].to_string()}")
            else:
                ok("No null values found")
        else:
            missing.append(name)
            warn(f"{name}.csv not found in {DATA_RAW}/ — skipping")

    if missing:
        print(f"\n  {C.YELLOW}Place these CSVs in {DATA_RAW}/ and re-run:{C.RESET}")
        for m in missing:
            print(f"    • {m}.csv")

    return dataframes


# ══════════════════════════════════════════════════════════════════
# STEP 3 — FETCH LIVE NAV
# ══════════════════════════════════════════════════════════════════
def step_fetch_nav() -> pd.DataFrame | None:
    hdr("STEP 3 — Fetching Live NAV from mfapi.in")
    all_dfs = []
    summary_rows = []

    for code, name in KEY_SCHEMES.items():
        print(f"\n  📡 {C.BOLD}{name}{C.RESET}  (code: {code})")
        print(f"     GET https://api.mfapi.in/mf/{code}")
        df = fetch_nav(code, name)
        if df is not None:
            # Save individual scheme CSV
            out = os.path.join(DATA_RAW, f"nav_{code}.csv")
            save_csv(df, out, f"NAV saved")
            all_dfs.append(df)
            latest = df.iloc[-1]
            ok(f"Latest NAV : ₹{latest['nav']:.4f}  on  {latest['date'].date()}")
            ok(f"Records    : {len(df):,}")
            summary_rows.append({
                "scheme_code":     code,
                "scheme_name":     name,
                "fund_house":      df["fund_house"].iloc[0],
                "scheme_category": df["scheme_category"].iloc[0],
                "latest_date":     str(latest["date"].date()),
                "latest_nav":      round(float(latest["nav"]), 4),
                "total_records":   len(df),
            })
        else:
            summary_rows.append({"scheme_code": code, "scheme_name": name, "error": "fetch_failed"})

    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        save_csv(combined, os.path.join(DATA_RAW, "all_nav_combined.csv"), "Combined NAV saved")

        summary_df = pd.DataFrame(summary_rows)
        save_csv(summary_df, os.path.join(DATA_RAW, "nav_summary.csv"), "NAV summary saved")
        return combined

    err("No NAV data fetched. Check your internet connection.")
    return None


# ══════════════════════════════════════════════════════════════════
# STEP 4 — EXPLORE FUND MASTER
# ══════════════════════════════════════════════════════════════════
def step_explore_fund_master(dataframes: dict):
    hdr("STEP 4 — Exploring Fund Master")
    if "fund_master" not in dataframes:
        warn("fund_master.csv not loaded — skipping exploration")
        return

    df = dataframes["fund_master"]
    explore_cols = {
        "Fund Houses":    "fund_house",
        "Categories":     "category",
        "Sub-Categories": "sub_category",
        "Risk Grades":    "risk_grade",
    }
    for label, col in explore_cols.items():
        if col in df.columns:
            print(f"\n  🔹 {C.BOLD}{label}{C.RESET}  ({df[col].nunique()} unique)")
            print(df[col].value_counts().to_string())
        else:
            warn(f"Column '{col}' not found in fund_master")

    # AMFI code structure
    code_col = next((c for c in ["amfi_code", "scheme_code"] if c in df.columns), None)
    if code_col:
        info(f"\nAMFI Scheme Code column: '{code_col}'")
        info(f"Total schemes  : {len(df)}")
        info(f"Sample codes   : {df[code_col].head(5).tolist()}")
        info(f"Code dtype     : {df[code_col].dtype}")


# ══════════════════════════════════════════════════════════════════
# STEP 5 — VALIDATE AMFI CODES
# ══════════════════════════════════════════════════════════════════
def step_validate_amfi(dataframes: dict) -> dict:
    hdr("STEP 5 — Validating AMFI Codes")

    result = {}
    if "fund_master" not in dataframes or "nav_history" not in dataframes:
        warn("fund_master or nav_history not loaded — skipping AMFI validation")
        return result

    fm  = dataframes["fund_master"]
    nav = dataframes["nav_history"]

    fm_col  = next((c for c in ["amfi_code", "scheme_code", "code"] if c in fm.columns), None)
    nav_col = next((c for c in ["amfi_code", "scheme_code", "code"] if c in nav.columns), None)

    if not fm_col or not nav_col:
        warn("Could not identify scheme-code columns — skipping validation")
        return result

    fm_codes  = set(fm[fm_col].dropna().astype(str))
    nav_codes = set(nav[nav_col].dropna().astype(str))
    matched   = fm_codes & nav_codes
    missing   = fm_codes - nav_codes
    extra     = nav_codes - fm_codes

    result = {
        "fund_master_codes":  len(fm_codes),
        "nav_history_codes":  len(nav_codes),
        "matched":            len(matched),
        "missing_in_nav":     len(missing),
        "extra_in_nav":       len(extra),
        "missing_codes":      sorted(missing)[:50],
    }

    print()
    for k, v in result.items():
        if k == "missing_codes":
            continue
        icon = "✅" if "missing" not in k and "extra" not in k else "⚠️ "
        print(f"  {icon}  {k:30s}: {v}")

    if missing:
        warn(f"First 10 missing codes: {sorted(missing)[:10]}")

    return result


# ══════════════════════════════════════════════════════════════════
# STEP 6 — WRITE DATA QUALITY REPORT
# ══════════════════════════════════════════════════════════════════
def step_write_report(dataframes: dict, amfi_result: dict):
    hdr("STEP 6 — Writing Data Quality Report")

    report = {
        "generated_at": datetime.now().isoformat(),
        "datasets":     [],
        "amfi_validation": amfi_result,
    }

    for name, df in dataframes.items():
        report["datasets"].append(quality_report(df, name))

    # JSON report
    json_path = os.path.join(REPORTS_DIR, "data_quality_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    ok(f"JSON report → {json_path}")

    # Plain-text summary
    txt_path = os.path.join(REPORTS_DIR, "data_quality_summary.txt")
    with open(txt_path, "w") as f:
        f.write("MUTUAL FUND ANALYTICS — DATA QUALITY SUMMARY\n")
        f.write(f"Generated: {report['generated_at']}\n")
        f.write("=" * 60 + "\n\n")
        for ds in report["datasets"]:
            f.write(f"Dataset   : {ds['dataset']}\n")
            f.write(f"  Rows    : {ds['rows']}\n")
            f.write(f"  Cols    : {ds['columns']}\n")
            f.write(f"  Nulls   : {ds['null_cells']}\n")
            f.write(f"  Dupes   : {ds['duplicate_rows']}\n")
            if ds["null_by_col"]:
                f.write(f"  NullCols: {ds['null_by_col']}\n")
            f.write("\n")
        if amfi_result:
            f.write("AMFI CODE VALIDATION\n" + "-" * 40 + "\n")
            for k, v in amfi_result.items():
                if k != "missing_codes":
                    f.write(f"  {k}: {v}\n")
    ok(f"Text report → {txt_path}")


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    print(f"\n{C.BOLD}{C.CYAN}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║   Capstone Project I — Mutual Fund Analytics        ║")
    print("║   Day 1: Project Setup + Data Ingestion (ETL)       ║")
    print(f"║   Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                         ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(C.RESET)

    step_folders()
    dataframes  = step_load_csvs()
    nav_df      = step_fetch_nav()
    step_explore_fund_master(dataframes)
    amfi_result = step_validate_amfi(dataframes)
    step_write_report(dataframes, amfi_result)

    print(f"\n{C.BOLD}{C.GREEN}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║  ✅  Day 1 Complete!                                 ║")
    print("║                                                      ║")
    print('║  Next: git add . && git commit -m                   ║')
    print('║        "Day 1: Data ingestion complete"             ║')
    print("╚══════════════════════════════════════════════════════╝")
    print(C.RESET)


if __name__ == "__main__":
    main()
