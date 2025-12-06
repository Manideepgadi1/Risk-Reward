import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%y', errors='coerce')
df = df.dropna(subset=['DATE']).sort_values('DATE')
df = df.set_index('DATE')

prices = df['N50'].astype(float).dropna()
latest_date = prices.index.max()

print(f'Latest date: {latest_date}')
print(f'5-year lookback start: {latest_date - pd.DateOffset(years=5)}')
print(f'4-year calc end (earliest valid start): {latest_date - pd.DateOffset(years=4)}')
print()
print('This means start dates can only be between:')
print(f'  {latest_date - pd.DateOffset(years=5)} and {latest_date - pd.DateOffset(years=4)}')
print('  = 12 months of valid start dates!')
print()
print('With monthly sampling, we only get ~12 historical 4-year returns.')
print('So V1 can only be: 0/12, 1/12, 2/12... = 0, 0.083, 0.167...')
print()

# To get more granular V1, we need DAILY sampling instead of monthly
five_year_start = latest_date - pd.DateOffset(years=5)
four_year_end = latest_date - pd.DateOffset(years=4)

# Daily sampling
daily_dates = prices[(prices.index >= five_year_start) & (prices.index <= four_year_end)].index
print(f'Daily samples in valid window: {len(daily_dates)}')
print(f'This would give V1 values like: 0/{len(daily_dates)}, 1/{len(daily_dates)}...')
print(f'Much more granular percentiles!')
