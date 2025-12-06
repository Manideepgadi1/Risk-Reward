"""
Standalone script to calculate and display Risk-Reward metrics for all indices.
Run this from command line to see the metrics table without starting the web server.
"""

import pandas as pd
import numpy as np

CSV_PATH = r"d:\Risk reward\data.csv"

def calculate_metrics():
    """Calculate CAGR, Volatility, and Risk for all index columns."""
    df = pd.read_csv(CSV_PATH)
    
    if "DATE" not in df.columns:
        raise ValueError("Expected a 'DATE' column in the CSV.")
    
    # Parse DATE and sort
    df["DATE"] = pd.to_datetime(df["DATE"], format='%d/%m/%y', errors="coerce")
    df = df.dropna(subset=["DATE"]).sort_values("DATE")
    
    # Set DATE as index
    df = df.set_index("DATE")
    
    # All remaining columns are index price series
    price_cols = df.columns
    
    results = []
    
    for col in price_cols:
        prices = df[col].astype(float)
        
        # Drop missing prices
        non_na = prices.dropna()
        if len(non_na) < 2:
            continue
        
        p_start = non_na.iloc[0]
        p_end = non_na.iloc[-1]
        n_days = (non_na.index[-1] - non_na.index[0]).days
        if n_days <= 0 or p_start == 0:
            continue
        
        # Trading years approximation
        n_years = n_days / 365.0
        if n_years == 0:
            continue
        
        # 1. CAGR
        cagr = (p_end / p_start) ** (1.0 / n_years) - 1.0
        if not np.isfinite(cagr):
            continue
        
        # 2. Volatility (Annualized Standard Deviation)
        daily_returns = non_na.pct_change().dropna()
        if len(daily_returns) < 2:
            continue
        daily_vol = daily_returns.std(ddof=1)
        if not np.isfinite(daily_vol):
            continue
        annual_vol = daily_vol * np.sqrt(252)
        
        # 3. Risk = Annualized Volatility
        risk = annual_vol
        if not np.isfinite(risk):
            continue
        
        results.append({
            "Index Name": col,
            "Return": round(cagr * 100, 2),
            "Volatility": round(annual_vol * 100, 2),
            "Risk": round(risk * 100, 2)
        })
    
    return results

def main():
    print("=" * 80)
    print("RISK-REWARD ANALYSIS - INDIAN MARKET INDICES")
    print("=" * 80)
    print()
    
    metrics = calculate_metrics()
    df = pd.DataFrame(metrics)
    
    # Sort by Return descending
    df = df.sort_values("Return", ascending=False)
    
    print(f"Total Indices Analyzed: {len(df)}")
    print()
    
    # Display summary statistics
    print("SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Average Return (CAGR): {df['Return'].mean():.2f}%")
    print(f"Average Risk (Volatility): {df['Risk'].mean():.2f}%")
    print(f"Highest Return: {df['Return'].max():.2f}% ({df.loc[df['Return'].idxmax(), 'Index Name']})")
    print(f"Lowest Return: {df['Return'].min():.2f}% ({df.loc[df['Return'].idxmin(), 'Index Name']})")
    print(f"Highest Risk: {df['Risk'].max():.2f}% ({df.loc[df['Risk'].idxmax(), 'Index Name']})")
    print(f"Lowest Risk: {df['Risk'].min():.2f}% ({df.loc[df['Risk'].idxmin(), 'Index Name']})")
    print()
    
    # Display full table
    print("DETAILED METRICS (Sorted by Return)")
    print("=" * 80)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 120)
    print(df.to_string(index=False))
    print()
    
    # Export to CSV
    output_file = r"d:\Risk reward\metrics_output.csv"
    df.to_csv(output_file, index=False)
    print(f"Results exported to: {output_file}")

if __name__ == "__main__":
    main()
