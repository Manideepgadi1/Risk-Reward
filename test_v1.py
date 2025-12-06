import pandas as pd
import numpy as np
import urllib.request
import json

# Test API response
print("=== Testing API Response ===")
try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
    data = json.loads(r.read())
    print(f"Total indices returned: {len(data)}")
    print("\nFirst 10 indices from API:")
    for d in data[:10]:
        print(f"  {d['Index Name']}: V1={d['V1']}, Ret={d['Ret']}, Momentum={d.get('Momentum')}, AbsMom={d.get('AbsMom')}")
except Exception as e:
    print(f"API Error: {e}")
    print("\nTesting calculation manually...")

CSV_PATH = r'd:\Risk reward - Copy\data.csv'
df = pd.read_csv(CSV_PATH)
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y', errors='coerce')
df = df.dropna(subset=['DATE']).sort_values('DATE')
df = df.set_index('DATE')

# Filter to 3 years
cutoff_date = df.index.max() - pd.DateOffset(years=3)
df_filtered = df[df.index >= cutoff_date]

print(f"Date range: {df_filtered.index.min()} to {df_filtered.index.max()}")
print(f"Total columns: {len(df_filtered.columns)}")

# Calculate 4-year returns for V1
results = []
for col in df.columns[:10]:
    prices = df[col].astype(float).dropna()
    if len(prices) < 2:
        continue
    
    four_year_cutoff = prices.index.max() - pd.DateOffset(years=4)
    four_year_prices = prices[prices.index >= four_year_cutoff]
    
    if len(four_year_prices) >= 2:
        p_start = four_year_prices.iloc[0]
        p_end = four_year_prices.iloc[-1]
        n_days = (four_year_prices.index[-1] - four_year_prices.index[0]).days
        n_years = n_days / 365.0
        if n_years > 0 and p_start > 0:
            return_4y = ((p_end / p_start) ** (1.0 / n_years) - 1.0) * 100
            results.append({'name': col, 'return_4y': return_4y})

print("\n4-Year Returns:")
for r in results:
    print(f"  {r['name']}: {r['return_4y']:.2f}%")

# Calculate V1
print("\nV1 Values (lower is better - means higher rank):")
valid_returns = [r['return_4y'] for r in results]
for r in results:
    rank = sum(1 for val in valid_returns if val > r['return_4y'])
    v1 = rank / len(valid_returns)
    print(f"  {r['name']}: V1 = {v1:.3f} (rank {rank+1}/{len(valid_returns)})")
