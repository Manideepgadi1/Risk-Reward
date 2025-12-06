# Risk-Reward Analysis Dashboard

A quantitative finance web application for analyzing Indian market indices with interactive heatmaps and detailed metrics.

## Features

- **Risk-Return Heatmap**: Visual distribution of indices across risk and return buckets
- **Detailed Metrics Table**: CAGR, Volatility, and Risk for all 122+ indices
- **Interactive Controls**: Search, sort, and filter indices
- **Click-to-Explore**: Click heatmap cells to see which indices fall in each bucket

## Metrics Calculated

### 1. Return (CAGR)
Compound Annual Growth Rate:
```
CAGR = (P_end / P_start)^(1/n) - 1
```

### 2. Volatility
Annualized Standard Deviation:
```
daily_return[t] = close[t] / close[t-1] - 1
daily_volatility = std(daily_return)
annual_volatility = daily_volatility × √252
```

### 3. Risk
Equal to Annualized Volatility

## Setup & Run

### 1. Install Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run the Application
```powershell
python app.py
```

### 3. Open in Browser
Navigate to: `http://127.0.0.1:5000/`

## Project Structure

```
d:\Risk reward\
├── app.py                  # Flask backend with analytics
├── data.csv                # Market indices price data
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   └── index.html          # Main HTML template
└── static/
    ├── styles.css          # UI styling
    └── script.js           # Frontend interactivity
```

## Data Source

CSV file contains:
- **DATE** column in dd/mm/yy format
- 122+ index price columns (NIFTY 50, NIFTY BANK, etc.)
- 7380 rows of daily price data

## Technology Stack

- **Backend**: Python 3, Flask
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom dark theme with gradient effects

## Usage Tips

1. **Heatmap**: Click any cell to see which indices belong to that risk-return bucket
2. **Search**: Type in the search box to filter indices by name
3. **Sort**: Use the dropdown to sort by Return, Risk, or Name
4. **Metrics**: All values are displayed as percentages rounded to 2 decimals

## Notes

- Uses 252 trading days per year for annualization
- Handles missing data automatically
- Sorts data by date before calculations
- Color intensity in heatmap represents the count of indices in each bucket
