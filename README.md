# 📊 Capstone Project I — Mutual Fund Analytics

**Start Date:** 20 Jun 2026 | **Status:** PLANNING | **Priority:** MEDIUM  
**Team:** avantikachauhan46 · ishwarigmadival14 · amansingh9327

---

## 🚀 Quickstart (3 commands — that's it)

```bash
# 1. One-time setup (creates venv + installs all deps + makes folders)
python setup.py

# 2. Activate virtual environment
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# 3. Run full Day-1 ETL pipeline
python data_ingestion.py
```

> ✅ **All 10 datasets are already included** in `data/raw/` — no downloads needed.  
> To regenerate them fresh anytime: `python generate_datasets.py`

---

## 🗂️ Project Structure

```
mutual_fund_analytics/
│
├── 📄 setup.py                  ← Run ONCE to bootstrap everything
├── 📄 config.py                 ← Central config (schemes, paths)
├── 📄 utils.py                  ← Shared helpers
├── 📄 data_ingestion.py         ← Day 1: Full ETL pipeline  ← MAIN SCRIPT
├── 📄 live_nav_fetch.py         ← Standalone live NAV fetcher
├── 📄 generate_datasets.py      ← Regenerate dummy data anytime
├── 📄 requirements.txt
│
├── 📁 data/
│   ├── raw/                     ← All 10 CSVs (included in repo)
│   └── processed/               ← Cleaned data (auto-generated)
│
├── 📁 notebooks/
│   └── Day1_Data_Ingestion.ipynb
│
├── 📁 sql/                      ← SQL queries (Day 2+)
├── 📁 dashboard/                ← Plotly/Dash (Day 3+)
└── 📁 reports/                  ← Auto-generated quality reports
```

---

## 📥 Datasets Included (`data/raw/`)

| File | Rows | Description |
|------|------|-------------|
| `fund_master.csv` | 20 | Master list of schemes, fund houses, categories |
| `nav_history.csv` | 26,100 | Daily NAV for all schemes (5 years) |
| `scheme_returns.csv` | 20 | 1M/3M/6M/1Y/3Y/5Y returns |
| `benchmark_returns.csv` | 6,525 | Nifty/Sensex index values (5 years) |
| `category_avg.csv` | 9 | Category-level average returns |
| `risk_metrics.csv` | 20 | Sharpe, Sortino, Beta, Alpha, Max Drawdown |
| `aum_data.csv` | 840 | Monthly AUM & folio count |
| `redemption_data.csv` | 840 | Monthly inflows & redemptions |
| `sip_data.csv` | 840 | Monthly SIP accounts & amounts |
| `portfolio_holdings.csv` | 191 | Stock-level holdings per scheme |

---

## 🔑 Key Schemes Tracked

| AMFI Code | Scheme |
|-----------|--------|
| 125497 | HDFC Top 100 Direct |
| 119551 | SBI Bluechip Direct |
| 120503 | ICICI Pru Bluechip Direct |
| 118632 | Nippon Large Cap Direct |
| 119092 | Axis Bluechip Direct |
| 120841 | Kotak Bluechip Direct |

Fetch live NAV anytime:
```bash
python live_nav_fetch.py                   # all 6 schemes
python live_nav_fetch.py --scheme 125497   # single scheme
python live_nav_fetch.py --list            # list schemes
```

---

## 📅 Day-wise Progress

| Day | Task | Status |
|-----|------|--------|
| **1** | Project Setup + Data Ingestion (ETL) | ✅ Done |
| 2 | Data Cleaning + EDA | 🔜 |
| 3 | NAV Analysis + Returns | 🔜 |

---

## 📦 Push to GitHub

```bash
git init
git remote add origin https://github.com/<your-username>/mutual_fund_analytics.git
git add .
git commit -m "Day 1: Data ingestion complete"
git push -u origin main
```
