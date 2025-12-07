import pandas as pd
import numpy as np
import urllib.request
import json

# Test API
print("=== Testing API Response ===")
try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
    data = json.loads(r.read())
    print(f"Total indices: {len(data)}")
    print("\nFirst 10 indices:")
    for d in data[:10]:
        print(f"  {d['Index Name']}: V1={d['V1']}, Ret={d['Ret']}")
except Exception as e:
    print(f"API Error: {e}")

print("\n" + "="*50)
print("=== Manual V1 Calculation ===")

CSV_PATH = r'd:\Risk reward - Copy\data.csv'
df = pd.read_csv(CSV_PATH)
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y', errors='coerce')
df = df.dropna(subset=['DATE']).sort_values('DATE')
df = df.set_index('DATE')

# Test with first column (N50)
col = 'N50'
prices = df[col].astype(float).dropna()

print(f'Index: {col}')
print(f'Date range: {prices.index.min()} to {prices.index.max()}')
print(f'Total data points: {len(prices)}')

# Latest 4-year CAGR
latest_date = prices.index.max()
latest_value = prices.iloc[-1]
print(f'\nLatest date: {latest_date}, Latest value: {latest_value}')

target_date_4y_ago = latest_date - pd.DateOffset(years=4)
print(f'Target 4y ago: {target_date_4y_ago}')

dates_before_target = prices.index[prices.index <= target_date_4y_ago]
print(f'Dates before target: {len(dates_before_target)}')

latest_4y_perf = None
if len(dates_before_target) > 0:
    closest_date_4y_ago = dates_before_target[-1]
    value_4y_ago = prices.loc[closest_date_4y_ago]
    print(f'Closest 4y ago: {closest_date_4y_ago}, Value: {value_4y_ago}')
    
    latest_4y_perf = ((latest_value / value_4y_ago) ** (1.0 / 4.0) - 1.0) * 100
    print(f'Latest 4Y CAGR: {latest_4y_perf:.2f}%')

# Historical 4-year performances from past 5 years
print('\n--- Historical 4-year performances ---')
historical_4y_perfs = []

five_year_lookback_start = latest_date - pd.DateOffset(years=5)
earliest_valid_start = latest_date - pd.DateOffset(years=4)

print(f'5-year lookback start: {five_year_lookback_start}')
print(f'Earliest valid start (for 4y calc): {earliest_valid_start}')

# Get monthly samples
monthly_dates = prices.resample('M').last().dropna().index
print(f'Total monthly dates: {len(monthly_dates)}')

valid_start_dates = [d for d in monthly_dates if d >= five_year_lookback_start and d <= earliest_valid_start]
print(f'Valid start dates in window: {len(valid_start_dates)}')

for start_date in valid_start_dates[:5]:  # Show first 5
    end_date_target = start_date + pd.DateOffset(years=4)
    dates_after_target = prices.index[prices.index >= end_date_target]
    
    if len(dates_after_target) > 0:
        end_date = dates_after_target[0]
        start_value = prices.asof(start_date)
        end_value = prices.asof(end_date)
        # Extract scalar if Series
        if isinstance(start_value, pd.Series):
            start_value = start_value.values[0]
        if isinstance(end_value, pd.Series):
            end_value = end_value.values[0]
        if isinstance(start_value, (int, float, np.integer, np.floating)) and isinstance(end_value, (int, float, np.integer, np.floating)):
            sv = float(start_value)
            ev = float(end_value)
            if sv > 0:
                hist_4y_perf = ((ev / sv) ** (1.0 / 4.0) - 1.0) * 100
                historical_4y_perfs.append(hist_4y_perf)
                print(f'  {start_date.date()} -> {end_date.date()}: {hist_4y_perf:.2f}%')

print(f'\nTotal historical 4Y perfs: {len(historical_4y_perfs)}')

if latest_4y_perf is not None and len(historical_4y_perfs) > 0:
    count_less = sum(1 for h in historical_4y_perfs if h < latest_4y_perf)
    v1_score = count_less / len(historical_4y_perfs)
    print(f'V1 Score: {v1_score:.3f}')
else:
    print('V1 Score: None (missing data)')
