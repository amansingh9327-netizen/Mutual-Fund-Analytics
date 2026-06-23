"""
generate_datasets.py
Generates all 10 realistic dummy CSV datasets for
Capstone Project I — Mutual Fund Analytics
"""

import os
import numpy as np
import pandas as pd
from datetime import date, timedelta

np.random.seed(42)
OUT = "/home/claude/mutual_fund_analytics/data/raw"
os.makedirs(OUT, exist_ok=True)

# ── Shared master lists ───────────────────────────────────────────
SCHEMES = [
    (125497, "HDFC Top 100 Direct",        "HDFC Mutual Fund",      "Equity",    "Large Cap",    "LOW",    "L001"),
    (119551, "SBI Bluechip Direct",         "SBI Mutual Fund",       "Equity",    "Large Cap",    "LOW",    "L002"),
    (120503, "ICICI Pru Bluechip Direct",   "ICICI Prudential MF",   "Equity",    "Large Cap",    "LOW",    "L003"),
    (118632, "Nippon Large Cap Direct",     "Nippon India MF",       "Equity",    "Large Cap",    "LOW",    "L004"),
    (119092, "Axis Bluechip Direct",        "Axis Mutual Fund",      "Equity",    "Large Cap",    "LOW",    "L005"),
    (120841, "Kotak Bluechip Direct",       "Kotak Mahindra MF",     "Equity",    "Large Cap",    "LOW",    "L006"),
    (130503, "Mirae Asset Large Cap",       "Mirae Asset MF",        "Equity",    "Large Cap",    "LOW",    "L007"),
    (122639, "Canara Robeco Bluechip",      "Canara Robeco MF",      "Equity",    "Large Cap",    "LOW",    "L008"),
    (101206, "UTI Mastershare Direct",      "UTI Mutual Fund",       "Equity",    "Large Cap",    "MEDIUM", "L009"),
    (112090, "DSP Top 100 Equity Direct",   "DSP Mutual Fund",       "Equity",    "Large Cap",    "MEDIUM", "L010"),
    (118989, "Franklin Bluechip Direct",    "Franklin Templeton MF", "Equity",    "Large Cap",    "MEDIUM", "L011"),
    (119834, "IDFC Large Cap Direct",       "IDFC Mutual Fund",      "Equity",    "Large Cap",    "MEDIUM", "L012"),
    (120716, "Tata Large Cap Direct",       "Tata Mutual Fund",      "Equity",    "Large Cap",    "MEDIUM", "L013"),
    (148740, "Parag Parikh Flexi Cap",      "PPFAS Mutual Fund",     "Equity",    "Flexi Cap",    "MEDIUM", "F001"),
    (135781, "HDFC Flexi Cap Direct",       "HDFC Mutual Fund",      "Equity",    "Flexi Cap",    "MEDIUM", "F002"),
    (119598, "SBI Contra Direct",           "SBI Mutual Fund",       "Equity",    "Contra",       "HIGH",   "C001"),
    (120594, "ICICI Pru Value Discovery",   "ICICI Prudential MF",   "Equity",    "Value",        "HIGH",   "V001"),
    (125354, "Mirae Asset ELSS",            "Mirae Asset MF",        "Equity",    "ELSS",         "HIGH",   "E001"),
    (100033, "HDFC Liquid Direct",          "HDFC Mutual Fund",      "Debt",      "Liquid",       "VERY LOW","D001"),
    (119271, "SBI Liquid Direct",           "SBI Mutual Fund",       "Debt",      "Liquid",       "VERY LOW","D002"),
]

SCHEME_CODES = [s[0] for s in SCHEMES]
DATES_5Y = pd.date_range("2019-06-01", "2024-06-01", freq="B")   # business days
DATES_3Y = pd.date_range("2021-06-01", "2024-06-01", freq="B")


def pct(x): return round(float(x), 4)


# ══════════════════════════════════════════════════════════════════
# 1. fund_master.csv
# ══════════════════════════════════════════════════════════════════
def make_fund_master():
    rows = []
    for code, name, house, stype, subcat, risk, isin in SCHEMES:
        rows.append({
            "amfi_code":        code,
            "scheme_name":      name,
            "fund_house":       house,
            "scheme_type":      stype,
            "category":         subcat,
            "sub_category":     subcat,
            "risk_grade":       risk,
            "isin":             isin,
            "launch_date":      pd.Timestamp("2013-01-01") + pd.DateOffset(days=int(np.random.randint(0,1000))),
            "aum_cr":           round(np.random.uniform(500, 50000), 2),
            "expense_ratio":    round(np.random.uniform(0.1, 1.5), 4),
            "exit_load_pct":    round(np.random.choice([0.0, 0.5, 1.0]), 2),
            "min_investment":   int(np.random.choice([500, 1000, 5000])),
            "benchmark":        "Nifty 100 TRI" if subcat == "Large Cap" else "Nifty 500 TRI",
            "fund_manager":     np.random.choice(["Prashant Jain","Neelesh Surana","Jinesh Gopani",
                                                   "Sohini Andani","Shreyash Devalkar","R Janakiraman"]),
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/fund_master.csv", index=False)
    print(f"✅ fund_master.csv          ({len(df)} rows)")


# ══════════════════════════════════════════════════════════════════
# 2. nav_history.csv
# ══════════════════════════════════════════════════════════════════
def make_nav_history():
    rows = []
    for code, name, house, stype, subcat, risk, isin in SCHEMES:
        nav = np.random.uniform(20, 200)
        drift  = 0.0003          # ~7.5% annual drift
        vol    = 0.012 if stype == "Equity" else 0.001
        for dt in DATES_5Y:
            nav = max(nav * np.exp(np.random.normal(drift, vol)), 1)
            rows.append({
                "amfi_code":    code,
                "scheme_name":  name,
                "date":         dt.date(),
                "nav":          round(nav, 4),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/nav_history.csv", index=False)
    print(f"✅ nav_history.csv          ({len(df):,} rows)")


# ══════════════════════════════════════════════════════════════════
# 3. scheme_returns.csv
# ══════════════════════════════════════════════════════════════════
def make_scheme_returns():
    rows = []
    for code, name, house, stype, subcat, risk, isin in SCHEMES:
        rows.append({
            "amfi_code":       code,
            "scheme_name":     name,
            "fund_house":      house,
            "category":        subcat,
            "return_1m":       pct(np.random.uniform(-5, 8)),
            "return_3m":       pct(np.random.uniform(-3, 15)),
            "return_6m":       pct(np.random.uniform(0, 20)),
            "return_1y":       pct(np.random.uniform(5, 35)),
            "return_3y_cagr":  pct(np.random.uniform(8, 25)),
            "return_5y_cagr":  pct(np.random.uniform(10, 22)),
            "return_since_inception": pct(np.random.uniform(12, 18)),
            "as_of_date":      "2024-06-01",
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/scheme_returns.csv", index=False)
    print(f"✅ scheme_returns.csv       ({len(df)} rows)")


# ══════════════════════════════════════════════════════════════════
# 4. benchmark_returns.csv
# ══════════════════════════════════════════════════════════════════
def make_benchmark_returns():
    benchmarks = ["Nifty 50 TRI", "Nifty 100 TRI", "Nifty 500 TRI",
                  "BSE Sensex TRI", "Nifty Midcap 150 TRI"]
    rows = []
    for b in benchmarks:
        base = 10000.0
        for dt in DATES_5Y:
            base *= np.exp(np.random.normal(0.0003, 0.01))
            rows.append({
                "benchmark":   b,
                "date":        dt.date(),
                "index_value": round(base, 2),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/benchmark_returns.csv", index=False)
    print(f"✅ benchmark_returns.csv    ({len(df):,} rows)")


# ══════════════════════════════════════════════════════════════════
# 5. category_avg.csv
# ══════════════════════════════════════════════════════════════════
def make_category_avg():
    categories = ["Large Cap", "Flexi Cap", "Mid Cap", "Small Cap",
                  "ELSS", "Value", "Contra", "Liquid", "Short Duration"]
    rows = []
    for cat in categories:
        rows.append({
            "category":             cat,
            "avg_return_1y":        pct(np.random.uniform(5, 35)),
            "avg_return_3y_cagr":   pct(np.random.uniform(8, 22)),
            "avg_return_5y_cagr":   pct(np.random.uniform(10, 20)),
            "avg_expense_ratio":    pct(np.random.uniform(0.3, 1.8)),
            "avg_sharpe":           pct(np.random.uniform(0.4, 1.5)),
            "total_schemes":        int(np.random.randint(10, 60)),
            "total_aum_cr":         round(np.random.uniform(10000, 300000), 2),
            "as_of_date":           "2024-06-01",
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/category_avg.csv", index=False)
    print(f"✅ category_avg.csv         ({len(df)} rows)")


# ══════════════════════════════════════════════════════════════════
# 6. risk_metrics.csv
# ══════════════════════════════════════════════════════════════════
def make_risk_metrics():
    rows = []
    for code, name, house, stype, subcat, risk, isin in SCHEMES:
        rows.append({
            "amfi_code":          code,
            "scheme_name":        name,
            "std_dev_1y":         pct(np.random.uniform(8, 22)),
            "beta":               pct(np.random.uniform(0.7, 1.2)),
            "alpha":              pct(np.random.uniform(-2, 6)),
            "sharpe_ratio":       pct(np.random.uniform(0.3, 1.8)),
            "sortino_ratio":      pct(np.random.uniform(0.4, 2.2)),
            "treynor_ratio":      pct(np.random.uniform(0.05, 0.25)),
            "information_ratio":  pct(np.random.uniform(-0.5, 1.2)),
            "max_drawdown_pct":   pct(np.random.uniform(-35, -5)),
            "r_squared":          pct(np.random.uniform(0.75, 0.99)),
            "as_of_date":         "2024-06-01",
        })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/risk_metrics.csv", index=False)
    print(f"✅ risk_metrics.csv         ({len(df)} rows)")


# ══════════════════════════════════════════════════════════════════
# 7. aum_data.csv
# ══════════════════════════════════════════════════════════════════
def make_aum_data():
    months = pd.date_range("2021-01-01", "2024-06-01", freq="MS")
    rows = []
    for code, name, house, *_ in SCHEMES:
        aum = np.random.uniform(1000, 40000)
        for m in months:
            aum = max(aum * np.random.uniform(0.97, 1.06), 100)
            rows.append({
                "amfi_code":   code,
                "scheme_name": name,
                "fund_house":  house,
                "month":       m.date(),
                "aum_cr":      round(aum, 2),
                "no_of_folios": int(aum * np.random.uniform(50, 150)),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/aum_data.csv", index=False)
    print(f"✅ aum_data.csv             ({len(df):,} rows)")


# ══════════════════════════════════════════════════════════════════
# 8. redemption_data.csv
# ══════════════════════════════════════════════════════════════════
def make_redemption_data():
    months = pd.date_range("2021-01-01", "2024-06-01", freq="MS")
    rows = []
    for code, name, house, *_ in SCHEMES:
        for m in months:
            inflow  = round(np.random.uniform(10, 2000), 2)
            outflow = round(np.random.uniform(5, inflow * 0.9), 2)
            rows.append({
                "amfi_code":       code,
                "scheme_name":     name,
                "month":           m.date(),
                "gross_inflow_cr": inflow,
                "redemption_cr":   outflow,
                "net_flow_cr":     round(inflow - outflow, 2),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/redemption_data.csv", index=False)
    print(f"✅ redemption_data.csv      ({len(df):,} rows)")


# ══════════════════════════════════════════════════════════════════
# 9. sip_data.csv
# ══════════════════════════════════════════════════════════════════
def make_sip_data():
    months = pd.date_range("2021-01-01", "2024-06-01", freq="MS")
    rows = []
    for code, name, house, *_ in SCHEMES:
        sip_accounts = int(np.random.randint(5000, 200000))
        for m in months:
            sip_accounts = int(sip_accounts * np.random.uniform(0.99, 1.04))
            rows.append({
                "amfi_code":           code,
                "scheme_name":         name,
                "month":               m.date(),
                "sip_accounts":        sip_accounts,
                "sip_amount_cr":       round(sip_accounts * np.random.uniform(0.0005, 0.002), 2),
                "new_sip_registered":  int(np.random.randint(100, 5000)),
                "sip_discontinued":    int(np.random.randint(50, 2000)),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/sip_data.csv", index=False)
    print(f"✅ sip_data.csv             ({len(df):,} rows)")


# ══════════════════════════════════════════════════════════════════
# 10. portfolio_holdings.csv
# ══════════════════════════════════════════════════════════════════
STOCKS = [
    ("RELIANCE",  "Reliance Industries",    "Energy"),
    ("HDFCBANK",  "HDFC Bank",              "Financial Services"),
    ("INFY",      "Infosys",                "IT"),
    ("TCS",       "TCS",                    "IT"),
    ("ICICIBANK", "ICICI Bank",             "Financial Services"),
    ("KOTAKBANK", "Kotak Mahindra Bank",    "Financial Services"),
    ("LT",        "Larsen & Toubro",        "Capital Goods"),
    ("ITC",       "ITC Ltd",                "FMCG"),
    ("HINDUNILVR","Hindustan Unilever",      "FMCG"),
    ("SBIN",      "State Bank of India",    "Financial Services"),
    ("AXISBANK",  "Axis Bank",              "Financial Services"),
    ("BAJFINANCE","Bajaj Finance",           "Financial Services"),
    ("ASIANPAINT","Asian Paints",            "Consumer Durables"),
    ("MARUTI",    "Maruti Suzuki",           "Automobile"),
    ("TITAN",     "Titan Company",           "Consumer Durables"),
]

def make_portfolio_holdings():
    quarter = "2024-Q1"
    rows = []
    for code, name, *_ in SCHEMES:
        # pick 8-12 stocks per scheme
        holdings = np.random.choice(len(STOCKS), size=np.random.randint(8, 13), replace=False)
        weights  = np.random.dirichlet(np.ones(len(holdings))) * 100
        for idx, w in zip(holdings, weights):
            sym, sname, sector = STOCKS[idx]
            rows.append({
                "amfi_code":         code,
                "scheme_name":       name,
                "quarter":           quarter,
                "stock_symbol":      sym,
                "stock_name":        sname,
                "sector":            sector,
                "holding_pct":       round(w, 4),
                "value_cr":          round(w * np.random.uniform(10, 500), 2),
                "no_of_shares":      int(np.random.randint(10000, 5000000)),
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/portfolio_holdings.csv", index=False)
    print(f"✅ portfolio_holdings.csv   ({len(df)} rows)")


# ── Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🔧 Generating all 10 datasets...\n")
    make_fund_master()
    make_nav_history()
    make_scheme_returns()
    make_benchmark_returns()
    make_category_avg()
    make_risk_metrics()
    make_aum_data()
    make_redemption_data()
    make_sip_data()
    make_portfolio_holdings()
    print(f"\n✅ All datasets saved to: {OUT}/\n")
