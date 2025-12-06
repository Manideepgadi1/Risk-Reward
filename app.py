from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Use relative path for production deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data.csv")

def calculate_metrics(duration='all'):
    """Calculate CAGR, Volatility, Risk, and Momentum for all index columns.
    
    Args:
        duration: '3years', '5years', or 'all'
    """
    df = pd.read_csv(CSV_PATH)
    
    if "DATE" not in df.columns:
        raise ValueError("Expected a 'DATE' column in the CSV.")
    
    # Parse DATE and sort
    df["DATE"] = pd.to_datetime(df["DATE"], format='%d/%m/%y', errors="coerce")
    df = df.dropna(subset=["DATE"]).sort_values("DATE")
    
    # Set DATE as index
    df = df.set_index("DATE")
    
    # Keep full dataset for V1 calculation
    df_full = df.copy()
    
    # Filter by duration for other metrics
    if duration == '3years':
        cutoff_date = df.index.max() - pd.DateOffset(years=3)
        df = df[df.index >= cutoff_date]
    elif duration == '5years':
        cutoff_date = df.index.max() - pd.DateOffset(years=5)
        df = df[df.index >= cutoff_date]
    # 'all' uses full dataset
    
    # All remaining columns are index price series
    price_cols = df.columns
    
    results = []
    
    for col in price_cols:
        prices = df[col].astype(float)
        
        # Drop missing prices
        non_na = prices.dropna()
        if len(non_na) < 2:
            continue
        
        # Get full price series for V1 calculation (need 9+ years of data)
        full_prices = df_full[col].astype(float).dropna()
        
        p_start = non_na.iloc[0]
        p_end = non_na.iloc[-1]
        n_days = (non_na.index[-1] - non_na.index[0]).days
        if n_days <= 0 or p_start == 0:
            continue
        
        # Trading years approximation
        n_years = n_days / 365.0
        if n_years == 0:
            continue
        
        # 1. Return (CAGR)
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
        
        # 3. Risk = Std * 3.45
        risk = (annual_vol * 100) * 3.45
        if not np.isfinite(risk):
            continue
        
        # 4. Calculate 12-month return for momentum (store raw value for now)
        if len(non_na) >= 252:  # At least 1 year of trading data (252 trading days)
            p_current = non_na.iloc[-1]
            p_12m_ago = non_na.iloc[-252]
            if p_12m_ago != 0:
                momentum_12m = ((p_current - p_12m_ago) / p_12m_ago) * 100
            else:
                momentum_12m = None
        else:
            momentum_12m = None
        
        if momentum_12m is not None and not np.isfinite(momentum_12m):
            momentum_12m = None
        
        # 5. Calculate 3-year simple return for V1 ranking (will be ranked later)
        # Return = (Current Price - Price 3 Years Ago) / Price 3 Years Ago * 100
        return_3y = None
        
        latest_date = full_prices.index.max()
        latest_value = full_prices.iloc[-1]
        
        # Find value 3 years ago
        target_date_3y_ago = latest_date - pd.DateOffset(years=3)
        dates_before_target = full_prices.index[full_prices.index <= target_date_3y_ago]
        
        if len(dates_before_target) > 0:
            closest_date_3y_ago = dates_before_target[-1]
            value_3y_ago = full_prices.loc[closest_date_3y_ago]
            
            if value_3y_ago > 0:
                # Simple Return = (Current - Past) / Past * 100
                return_3y = ((latest_value - value_3y_ago) / value_3y_ago) * 100
        
        # 6. Calculate Average Monthly Profit (4 years)
        # = Sum of all monthly returns in last 4 years / Number of months
        avg_monthly_profit_4y = None
        
        four_year_cutoff = latest_date - pd.DateOffset(years=4)
        four_year_prices = full_prices[full_prices.index >= four_year_cutoff]
        
        if len(four_year_prices) > 1:
            # Resample to monthly (end of month prices)
            monthly_prices = four_year_prices.resample('M').last().dropna()
            
            if len(monthly_prices) > 1:
                # Calculate monthly returns
                monthly_returns = monthly_prices.pct_change().dropna() * 100  # as percentage
                
                if len(monthly_returns) > 0:
                    # Average = Sum of monthly returns / Number of months
                    avg_monthly_profit_4y = monthly_returns.sum() / len(monthly_returns)
        
        # 7. Mean (average of return and risk)
        mean = (cagr * 100 + risk * 100) / 2
        
        results.append({
            "Index Name": col,
            "Ret": round(cagr * 100, 1),
            "Return_3y": return_3y,  # Will be used for V1 ranking
            "AvgMonthlyProfit_4y": round(avg_monthly_profit_4y, 2) if avg_monthly_profit_4y is not None else None,
            "Risk": round(risk, 1),  # Std * 3.45
            "Mean": round(mean, 1),
            "Momentum_12m": momentum_12m  # Store raw 12-month return
        })
    
    # Calculate V1: Percentile based on 3-year simple return across ALL indices
    # Step 1: Get all valid 3-year returns and sort
    valid_return_3y = [(i, r['Return_3y']) for i, r in enumerate(results) if r['Return_3y'] is not None]
    
    # Sort by return value to get ranks
    sorted_returns = sorted(valid_return_3y, key=lambda x: x[1])
    
    # Create rank mapping
    rank_map = {}
    for rank, (idx, val) in enumerate(sorted_returns, start=1):
        rank_map[idx] = rank
    
    for i, result in enumerate(results):
        if result['Return_3y'] is not None and len(valid_return_3y) > 1:
            # Get rank (1 = lowest, n = highest)
            rank = rank_map[i]
            total = len(valid_return_3y)
            
            # Percentile = (rank - 1) / (total - 1)
            percentile = (rank - 1) / (total - 1)
            
            result['V1'] = round(percentile, 3)
        else:
            result['V1'] = None
        
        # Remove temporary field
        del result['Return_3y']
    
    # Calculate momentum ratio (z-score) and absolute momentum after collecting all 12-month returns
    valid_momentum_12m = [r['Momentum_12m'] for r in results if r['Momentum_12m'] is not None]
    
    if len(valid_momentum_12m) > 1:
        avg_momentum = np.mean(valid_momentum_12m)
        sd_momentum = np.std(valid_momentum_12m, ddof=1)
        
        for result in results:
            if result['Momentum_12m'] is not None and sd_momentum > 0:
                # Momentum ratio = (momentum - avg_momentum) / sd_momentum
                momentum_ratio = (result['Momentum_12m'] - avg_momentum) / sd_momentum
                result['Momentum'] = round(momentum_ratio, 2)
                
                # Absolute Momentum = momentum / sd_momentum
                abs_momentum = result['Momentum_12m'] / sd_momentum
                result['AbsMom'] = round(abs_momentum, 2)
            else:
                result['Momentum'] = None
                result['AbsMom'] = None
    else:
        for result in results:
            result['Momentum'] = None
            result['AbsMom'] = None
    
    # Remove temporary Momentum_12m field
    for result in results:
        del result['Momentum_12m']
    
    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/heatmap")
def heatmap():
    return render_template("heatmap.html")

@app.route("/api/metrics")
def api_metrics():
    duration = request.args.get('duration', 'all')
    metrics = calculate_metrics(duration)
    return jsonify(metrics)

@app.route("/api/heatmap_data")
def api_heatmap_data():
    """Generate trailing/rolling return heatmap data for a specific index."""
    index_name = request.args.get('index')
    duration = request.args.get('duration', 'all')
    mode = request.args.get('mode', 'trailing')  # 'trailing' or 'rolling'
    timeline = float(request.args.get('timeline', '3'))  # years (e.g., 1, 3, 3.5, 4, 4.5, 5)
    
    if not index_name:
        return jsonify({"error": "Index name required"}), 400
    
    df = pd.read_csv(CSV_PATH)
    
    if "DATE" not in df.columns:
        return jsonify({"error": "Invalid CSV format"}), 500
    
    # Parse DATE and sort
    df["DATE"] = pd.to_datetime(df["DATE"], format='%d/%m/%y', errors="coerce")
    df = df.dropna(subset=["DATE"]).sort_values("DATE")
    
    # Check if index exists
    if index_name not in df.columns:
        return jsonify({"error": f"Index '{index_name}' not found"}), 404
    
    # Set DATE as index
    df = df.set_index("DATE")
    
    # Apply duration filter
    if duration == '1year':
        cutoff_date = df.index.max() - pd.DateOffset(years=1)
        df = df[df.index >= cutoff_date]
    elif duration == '3years':
        cutoff_date = df.index.max() - pd.DateOffset(years=3)
        df = df[df.index >= cutoff_date]
    elif duration == '5years':
        cutoff_date = df.index.max() - pd.DateOffset(years=5)
        df = df[df.index >= cutoff_date]
    # 'all' uses full dataset
    
    # Get price series for the index
    prices = df[index_name].astype(float).dropna()
    
    if len(prices) < 2:
        return jsonify({"error": "Insufficient data"}), 400
    
    # Find the first date where we have data
    first_data_date = prices.index[0]
    
    # Resample to monthly data (last day of month)
    monthly_prices = prices.resample('M').last().dropna()
    
    # Calculate the earliest valid date for the selected timeline
    # For trailing X years, we need X years of data before we can show any result
    earliest_valid_date = first_data_date + pd.DateOffset(years=int(timeline)) + pd.DateOffset(months=int((timeline % 1) * 12))
    
    print(f"DEBUG: Index={index_name}, First data date={first_data_date}, Timeline={timeline}yrs, Earliest valid={earliest_valid_date}")
    
    # Calculate trailing or rolling returns
    lookback_months = int(timeline * 12)  # Convert years to months
    
    heatmap_data = {}
    
    for i, (date, price) in enumerate(monthly_prices.items()):
        date_ts = pd.to_datetime(date)
        year = str(date_ts.year)
        month = str(date_ts.month)
        
        if year not in heatmap_data:
            heatmap_data[year] = {}
        
        # Calculate return based on mode
        if mode == 'trailing':
            # Trailing: Look BACK X years from this month
            # Formula: (Current Price - Price X years ago) / Price X years ago * 100
            if i >= lookback_months:
                past_price = monthly_prices.iloc[i - lookback_months]
                if past_price > 0 and pd.notna(price) and pd.notna(past_price):
                    # Simple return (not annualized)
                    simple_return = ((price - past_price) / past_price) * 100
                    heatmap_data[year][month] = float(simple_return)
                else:
                    heatmap_data[year][month] = None
            else:
                # Not enough historical data before this month
                heatmap_data[year][month] = None
        else:
            # Rolling (Forward): Look FORWARD X years from this month
            # Formula: (Future Price / Current Price)^(1/years) - 1
            # Check if we have enough future data
            if i + lookback_months < len(monthly_prices):
                future_price = monthly_prices.iloc[i + lookback_months]
                if price > 0 and pd.notna(price) and pd.notna(future_price):
                    # Annualized return: (Future/Current)^(1/years) - 1
                    annualized_return = ((future_price / price) ** (1.0 / timeline) - 1.0) * 100
                    heatmap_data[year][month] = float(annualized_return)
                else:
                    heatmap_data[year][month] = None
            else:
                # Not enough future data (too close to present)
                heatmap_data[year][month] = None
    
    # Calculate metrics based on timeline
    if timeline and timeline > 0:
        # Use only the last X years of data for metrics (convert to days)
        days_back = int(timeline * 365)
        cutoff_date = prices.index.max() - pd.Timedelta(days=days_back)
        timeline_prices = prices[prices.index >= cutoff_date]
        
        if len(timeline_prices) >= 2:
            p_start = timeline_prices.iloc[0]
            p_end = timeline_prices.iloc[-1]
            n_days = (timeline_prices.index[-1] - timeline_prices.index[0]).days
            n_years = n_days / 365.0
            
            cagr = None
            if n_years > 0 and p_start > 0:
                cagr = float((p_end / p_start) ** (1.0 / n_years) - 1.0)
            
            # Volatility for the timeline period
            timeline_daily_returns = timeline_prices.pct_change().dropna()
            timeline_daily_vol = timeline_daily_returns.std(ddof=1)
            annual_vol = float(timeline_daily_vol * np.sqrt(252)) if np.isfinite(timeline_daily_vol) else None
        else:
            cagr = None
            annual_vol = None
    else:
        # Fallback to full dataset
        p_start = prices.iloc[0]
        p_end = prices.iloc[-1]
        n_days = (prices.index[-1] - prices.index[0]).days
        n_years = n_days / 365.0
        
        cagr = None
        if n_years > 0 and p_start > 0:
            cagr = float((p_end / p_start) ** (1.0 / n_years) - 1.0)
        
        # Volatility
        daily_returns = prices.pct_change().dropna()
        daily_vol = daily_returns.std(ddof=1)
        annual_vol = float(daily_vol * np.sqrt(252)) if np.isfinite(daily_vol) else None
    
    # Latest values
    current_price = float(prices.iloc[-1]) if len(prices) > 0 else None
    
    # Get latest return from heatmap data
    latest_return = None
    if len(heatmap_data) > 0:
        latest_year = str(max([int(y) for y in heatmap_data.keys()]))
        if latest_year in heatmap_data:
            latest_months = [m for m in heatmap_data[latest_year].values() if m is not None]
            if latest_months:
                latest_return = latest_months[-1]
    
    result = {
        "indexName": index_name,
        "heatmapData": heatmap_data,
        "cagr": cagr,
        "volatility": annual_vol,
        "risk": annual_vol,
        "currentPrice": current_price,
        "latestReturn": latest_return,
        "mode": mode,
        "timeline": timeline
    }
    
    print(f"DEBUG: Returning heatmap for {index_name}, mode: {mode}, timeline: {timeline}yrs, years: {sorted(heatmap_data.keys())}")
    
    response = jsonify(result)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
