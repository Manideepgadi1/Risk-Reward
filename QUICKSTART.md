# Quick Start Guide

## Your Risk-Reward Analysis Dashboard is Ready! 🎉

### What You Have

✅ **Web Application** - Interactive dashboard with heatmap and metrics table  
✅ **Python Backend** - Flask server with quantitative finance calculations  
✅ **Standalone Script** - Command-line analysis tool  
✅ **CSV Export** - Results saved to `metrics_output.csv`

---

## 📊 Key Findings from Your Data

Analyzed **122 Indian Market Indices** over **20+ years** (2005-2025):

- **Highest Return**: NIFTY SME EMERGE at **36.13% CAGR**
- **Lowest Risk**: NIFTY 10 YR BENCHMARK G-SEC at **3.94% volatility**
- **Average Return**: **15.26% CAGR**
- **Average Risk**: **17.77% volatility**

---

## 🚀 How to Use

### Option 1: Web Dashboard (Recommended)

The Flask server is currently running at:
```
http://127.0.0.1:5000
```

**Features:**
- **Risk-Return Heatmap**: Visual distribution showing which indices fall into each risk/return bucket
- **Interactive Table**: Search, sort, and filter all 122 indices
- **Click Cells**: Click any heatmap cell to see which indices belong to that bucket
- **Real-time**: All calculations done on-the-fly from your CSV data

To start the server (if not running):
```powershell
cd "d:\Risk reward"
& ".venv\Scripts\python.exe" app.py
```

### Option 2: Command-Line Analysis

Run the standalone script for a quick terminal output:
```powershell
cd "d:\Risk reward"
& ".venv\Scripts\python.exe" analyze.py
```

This will:
- Print full metrics table to console
- Show summary statistics
- Export results to `metrics_output.csv`

---

## 📁 Project Files

```
d:\Risk reward\
├── app.py                  # Flask web server
├── analyze.py              # Standalone analysis script
├── data.csv                # Your market data (122 indices, 7378 rows)
├── metrics_output.csv      # Exported results
├── requirements.txt        # Python dependencies
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
├── .venv\                  # Python virtual environment
├── templates\
│   └── index.html          # Web dashboard HTML
└── static\
    ├── styles.css          # Dashboard styling
    └── script.js           # Frontend logic
```

---

## 🔬 Metrics Explained

### 1. Return (CAGR)
**Compound Annual Growth Rate** - The annualized rate of return over the entire period.

Formula: `CAGR = (P_end / P_start)^(1/n) - 1`

Example: NIFTY 50 went from ₹2,782 to ₹38,367 over 20.2 years = **13.86% CAGR**

### 2. Volatility (Annualized Standard Deviation)
**Risk measure** - How much the index price fluctuates day-to-day, annualized.

Formula:
```
daily_return[t] = close[t] / close[t-1] - 1
daily_volatility = std(daily_return)
annual_volatility = daily_volatility × √252
```

Example: NIFTY 50 has **17.33% volatility** (moderate risk)

### 3. Risk
Equal to Annualized Volatility. Higher values indicate more price swings.

---

## 🎨 Heatmap Interpretation

The heatmap shows the **distribution of indices** across risk-return buckets:

- **X-axis (columns)**: Return ranges (0-10%, 10-20%, etc.)
- **Y-axis (rows)**: Risk ranges (0-10%, 10-15%, etc.)
- **Cell color intensity**: Number of indices in that bucket
  - Light blue = Few indices (0-2)
  - Medium blue = Moderate (3-8)
  - Dark blue = Many indices (9+)

**What to look for:**
- **Top-right**: High return, high risk (aggressive growth)
- **Top-left**: Low return, high risk (poor risk-adjusted returns)
- **Bottom-right**: High return, low risk (ideal, but rare)
- **Bottom-left**: Low return, low risk (conservative, stable)

---

## 💡 Example Use Cases

### Find Low-Risk, High-Return Indices
1. Look at the heatmap's bottom-right area
2. Or sort the metrics table by Return (descending)
3. Filter for Volatility < 15%

**Result**: Indices like `Nifty500 Flexicap Quality 30` (17.54% return, 12.98% risk)

### Compare Sectors
Search for sector names in the metrics table:
- "BANK" → Shows NIFTY BANK, NIFTY PRIVATE BANK, etc.
- "IT" → Shows NIFTY IT and related indices
- "PHARMA" → Shows pharmaceutical indices

### Export Custom Analysis
The `metrics_output.csv` can be opened in Excel for:
- Custom charts
- Sharpe ratio calculations
- Risk-adjusted return comparisons

---

## 🛠️ Customization

### Change Data Source
Edit `app.py` and `analyze.py`, line 8:
```python
CSV_PATH = r"path\to\your\data.csv"
```

### Adjust Heatmap Bins
Edit `app.py`, lines 72-77:
```python
return_bins = [-100, 0, 10, 20, 30, 40, 50, 100, 200]
risk_bins = [0, 10, 15, 20, 25, 30, 40, 100]
```

### Change Color Scheme
Edit `static\script.js`, `colorScale()` function (lines 93-103)

---

## 📞 Support

If the web server isn't running:
```powershell
cd "d:\Risk reward"
& ".venv\Scripts\python.exe" app.py
```

If you see "module not found" errors:
```powershell
cd "d:\Risk reward"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

To stop the Flask server:
Press `Ctrl+C` in the terminal

---

## 🎯 Next Steps

1. **Explore the heatmap** - Click cells to see which indices are in each bucket
2. **Use the search** - Find specific indices (e.g., "NIFTY 50")
3. **Sort by risk** - Find the most/least volatile indices
4. **Export data** - Use `metrics_output.csv` for further analysis
5. **Compare sectors** - Search for sector keywords to compare performance

Enjoy your quantitative analysis! 📈
