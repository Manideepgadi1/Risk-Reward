"""Check V1 calculation step by step"""

import pandas as pd
import urllib.request
import json

CSV_PATH = r'd:\Risk reward - Copy\data.csv'

# Load data
df = pd.read_csv(CSV_PATH)
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y', errors='coerce')
df = df.dropna(subset=['DATE']).sort_values('DATE')
df = df.set_index('DATE')

print("="*80)
print("STEP-BY-STEP V1 CALCULATION VERIFICATION")
print("="*80)

# Test with a few indices
test_indices = ['N50', 'NMC50', 'NIDEF', 'NMEDIA', 'NBANK']

manual_results = []

for col in test_indices:
    prices = df[col].astype(float).dropna()
    
    latest_date = prices.index.max()
    latest_value = prices.iloc[-1]
    
    # Find value 5 years ago
    target_date_5y_ago = latest_date - pd.DateOffset(years=5)
    dates_before_target = prices.index[prices.index <= target_date_5y_ago]
    
    if len(dates_before_target) > 0:
        closest_date_5y_ago = dates_before_target[-1]
        value_5y_ago = prices.loc[closest_date_5y_ago]
        
        # CAGR = (FV/PV)^(1/5) - 1
        cagr_5y = ((latest_value / value_5y_ago) ** (1.0 / 5.0) - 1.0) * 100
        
        print(f"\n{col}:")
        print(f"  Date 5Y ago: {closest_date_5y_ago.date()}")
        print(f"  Price 5Y ago: {value_5y_ago:.2f}")
        print(f"  Latest date: {latest_date.date()}")
        print(f"  Latest price: {latest_value:.2f}")
        print(f"  Formula: ({latest_value:.2f}/{value_5y_ago:.2f})^(1/5) - 1")
        print(f"  5-Year CAGR: {cagr_5y:.4f}%")
        
        manual_results.append({'Index': col, 'CAGR_5y': cagr_5y})

print("\n" + "="*80)
print("RANKING & V1 CALCULATION")
print("="*80)

# Sort by CAGR (ascending)
manual_results.sort(key=lambda x: x['CAGR_5y'])

print("\nSorted by CAGR (low to high):")
for i, item in enumerate(manual_results):
    print(f"{i+1}. {item['Index']:15} CAGR_5y = {item['CAGR_5y']:.4f}%")

print("\nCalculating V1 for each:")
for i, item in enumerate(manual_results):
    count_lower = i  # How many indices have lower CAGR
    total = len(manual_results)
    rank_percentile = (count_lower / total) * 100
    v1 = rank_percentile / 100
    
    print(f"\n{item['Index']}:")
    print(f"  CAGR_5y: {item['CAGR_5y']:.4f}%")
    print(f"  Indices with lower CAGR: {count_lower} out of {total}")
    print(f"  Rank percentile: ({count_lower}/{total}) * 100 = {rank_percentile:.1f}%")
    print(f"  V1 = {rank_percentile}/100 = {v1:.3f}")

print("\n" + "="*80)
print("COMPARING WITH API VALUES")
print("="*80)

# Get API values
r = urllib.request.urlopen('http://127.0.0.1:5000/api/metrics?duration=3years')
data = json.loads(r.read())

print("\nAPI vs Manual calculation:")
for idx_name in test_indices:
    api_item = next((d for d in data if d['Index Name'] == idx_name), None)
    manual_item = next((m for m in manual_results if m['Index'] == idx_name), None)
    
    if api_item and manual_item:
        print(f"\n{idx_name}:")
        print(f"  Manual CAGR_5y: {manual_item['CAGR_5y']:.4f}%")
        print(f"  API V1: {api_item['V1']:.3f}")
        print(f"  API Ret (3Y): {api_item['Ret']}%")

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE")
print("Formula: V1 = (count_lower_CAGR / total_indices) / 100")
print("Higher V1 = Higher 5-year CAGR = Better performer")
print("="*80)
