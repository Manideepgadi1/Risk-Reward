# Risk-Reward API Package Usage Guide

## Installation

### From this directory:
```bash
cd "D:\Risk reward - Copy"
pip install -e .
```

This installs the package in "editable" mode, so changes to the code are immediately available.

---

## Usage in Other Projects

### Basic Usage

```python
from riskapp import RiskRewardAPI

# Initialize the API
api = RiskRewardAPI()

# Get metrics for all indices (3 years)
metrics = api.get_metrics(duration='3years')

# Print results
for item in metrics:
    print(f"{item['Index Name']}: V1={item['V1']}, Ret={item['Ret']}%")
```

### Get Specific Indices

```python
# Get metrics for specific indices only
metrics = api.get_metrics(duration='5years', indices=['N50', 'NBANK', 'NTECH'])

for item in metrics:
    print(f"{item['Index Name']}: V1={item['V1']}, Risk={item['Risk']}")
```

### Get Raw Price Data

```python
# Get price history for an index
prices = api.get_index_data('N50')
print(prices.head())
print(f"Latest price: {prices.iloc[-1]}")
```

### List All Available Indices

```python
# Get list of all indices
indices = api.get_available_indices()
print(f"Total indices: {len(indices)}")
print(indices[:10])  # First 10
```

### Use Custom Data File

```python
# Use your own CSV file
api = RiskRewardAPI(csv_path='path/to/your/data.csv')
metrics = api.get_metrics()
```

---

## Example: Integration with Another Project

### Example 1: Data Analysis Script

```python
# my_analysis.py
from riskapp import RiskRewardAPI
import pandas as pd

# Initialize
api = RiskRewardAPI()

# Get all metrics
data = api.get_metrics(duration='all')

# Convert to DataFrame for analysis
df = pd.DataFrame(data)

# Find top performers by V1
top_10 = df.nlargest(10, 'V1')run backend and 
print("Top 10 by V1:")
print(top_10[['Index Name', 'V1', 'Ret', 'Risk']])

# Filter low risk, high return
good_picks = df[(df['Risk'] < 50) & (df['Ret'] > 15)]
print(f"\nFound {len(good_picks)} low-risk, high-return indices")
```

### Example 2: Export to Excel

```python
from riskapp import RiskRewardAPI
import pandas as pd

api = RiskRewardAPI()
metrics = api.get_metrics(duration='3years')

# Convert to DataFrame
df = pd.DataFrame(metrics)

# Export to Excel
df.to_excel('risk_reward_analysis.xlsx', index=False)
print("Exported to Excel!")
```

### Example 3: Build Your Own API

```python
# my_custom_api.py
from flask import Flask, jsonify
from riskapp import RiskRewardAPI

app = Flask(__name__)
api = RiskRewardAPI()

@app.route('/api/top-performers')
def top_performers():
    metrics = api.get_metrics(duration='3years')
    # Sort by V1 and get top 20
    sorted_metrics = sorted(metrics, key=lambda x: x['V1'] or 0, reverse=True)
    return jsonify(sorted_metrics[:20])

@app.route('/api/index/<name>')
def get_index(name):
    try:
        prices = api.get_index_data(name)
        return jsonify({
            'index': name,
            'latest_price': float(prices.iloc[-1]),
            'data_points': len(prices)
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(port=5001)
```

### Example 4: Scheduled Reports

```python
# daily_report.py
from riskapp import RiskRewardAPI
from datetime import datetime

api = RiskRewardAPI()
metrics = api.get_metrics(duration='3years')

# Generate report
print(f"Risk-Reward Report - {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 60)

# Top 5 by V1
top_5 = sorted(metrics, key=lambda x: x['V1'] or 0, reverse=True)[:5]
print("\nTop 5 Performers (V1):")
for i, item in enumerate(top_5, 1):
    print(f"{i}. {item['Index Name']}: V1={item['V1']}, Ret={item['Ret']}%")

# Lowest risk
low_risk = sorted(metrics, key=lambda x: x['Risk'])[:5]
print("\nLowest Risk Indices:")
for i, item in enumerate(low_risk, 1):
    print(f"{i}. {item['Index Name']}: Risk={item['Risk']}")
```

---

## Package Structure

```
riskapp/
├── __init__.py          # Package initialization
├── metrics.py           # Core RiskRewardAPI class
└── data.csv            # Default data file

setup.py                 # Package installation config
```

---

## Return Data Format

Each metric dictionary contains:

```python
{
    'Index Name': 'N50',
    'Ret': 13.5,              # CAGR percentage
    'V1': 0.197,              # Rank percentile (0-1, higher = better)
    'Risk': 45.2,             # Volatility * 3.45
    'Mean': 29.35,            # Average of return and risk
    'AbsMom': 1.23,           # Absolute momentum
    'Momentum': -0.38,        # Momentum ratio (z-score)
    'AvgMonthlyProfit_4y': 1.2  # Average monthly return over 4 years
}
```

---

## Notes

- The package uses the same calculation logic as the Flask app
- All metrics are calculated from the CSV data file
- Supports durations: '3years', '5years', 'all'
- V1 values: Higher = Better performer (based on 5-year cumulative returns)
