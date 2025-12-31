from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os

# Support deployment under a URL prefix - reads from X-Forwarded-Prefix header
class PrefixMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Check for X-Forwarded-Prefix header from nginx
        prefix = environ.get('HTTP_X_FORWARDED_PREFIX', '')
        if prefix:
            environ['SCRIPT_NAME'] = prefix
        return self.app(environ, start_response)

app = Flask(__name__)

# Always apply prefix middleware to support nginx proxy
app.wsgi_app = PrefixMiddleware(app.wsgi_app)

# Use relative path for production deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data.csv")
V1_XLSX_PATH = os.path.join(BASE_DIR, "heatmap values.xlsx")

# Load V1 values from Excel at startup
def load_v1_values():
    """Load V1 average values from heatmap values.xlsx"""
    try:
        df_v1 = pd.read_excel(V1_XLSX_PATH)
        # Create a dictionary of Full Name to Percentile Value
        v1_percentile = dict(zip(df_v1['Full Name'], df_v1['Percentile Value']))
        
        # Load the name mapping to convert Full Names to CSV column names
        try:
            from index_name_mapping import FULLNAME_TO_COLUMN, COLUMN_TO_FULLNAME
            # Convert Full Name -> Column Name dictionary
            v1_percentile_final = {}
            fullname_map = {}
            for full_name, percentile in v1_percentile.items():
                column_name = FULLNAME_TO_COLUMN.get(full_name, full_name)
                v1_percentile_final[column_name] = round(percentile, 2)
                fullname_map[column_name] = full_name
            return v1_percentile_final, fullname_map
        except ImportError:
            print("Warning: Could not import index_name_mapping")
            return v1_percentile, {}

        # Create name mapping ONLY for indices that have exact or very close matches in heatmap values.xlsx
        name_mapping = {
            'NMCSEL': 'NMIDSEL',
            'NFINS2550': 'NFINS25',
            'NFINSXB': 'NFINSEXB',
            'N100EWT': 'N100EQWT',
            'NHBET50': 'NHBETA50',
            'NT10EWT': 'NT10EQWT',
            'NT15EWT': 'NT15EW',
            'NT20EWT': 'NT20EW',
            'N100QL30': 'N100QLT30',
            'NMC150M50': 'NM150M50',
            'N500FQ30': 'N5FCQ3',
            'N500LV50': 'N5LV5',
            'N500M50': 'N500M50',
            'N500QL50': 'N500QLT50',
            'N500MQLV': 'NMQLV',
            'NMC150Q': 'NMC150Q',
            'N500MQ50': 'N5MCMQ5',
            'N50EQWGT': 'N50EQWGT',
            'N50V20': 'N50V20',
            'N200V30': 'N200V30',
            'N500V50': 'N500V50',
            'N200QL30': 'N200Q30',
            'N100ESG': 'N100ESG',
            'N100ESGE': 'N100ESGE',
            'N100ESGSL': 'N100ESGSL',
            'N100LIQ15': 'NLCLIQ15',
            'N50SH': 'N50SH',
            'N500SH': 'N500SH',
            'NHOUS': 'NHOUSING',
            'NREIT': 'NREiT',
            'NTATA25': 'NTATA25C',
            'NCONTRA': 'NCONTRA',
            'NNACON': 'NNACON',
            'NQLV30': 'NQLV30',
            'NQLLV30': 'NQLV30',
            'NENRGY': 'NENERGY',
            'NIIL': 'NIINT',
            'NMCL15': 'NMIDLIQ15',
            'NRURAL': 'NRRL',
            'NMF5032': 'NMFG532',
            'NINF5032': 'NINFRA532',
            'NIRLPSU': 'NRPSU',
            'NINACON': 'NNACON',
            'NWAVES': 'NWVS',
            'NCAPMRKT': 'NCM',
            'NIFTY500 EQUAL WEIGHT.1': 'N500EQWT',
        }
        
        # Apply name mapping - add mapped names to v1_percentile dictionary
        v1_percentile_final_mapped = v1_percentile_final.copy()
        fullname_map_final = fullname_map.copy()
        for data_name, v1_name in name_mapping.items():
            if v1_name in v1_percentile_final:
                v1_percentile_final_mapped[data_name] = v1_percentile_final[v1_name]
                if v1_name in fullname_map:
                    fullname_map_final[data_name] = fullname_map[v1_name]
        
        return v1_percentile_final_mapped, fullname_map_final
    except Exception as e:
        print(f"Warning: Could not load heatmap values.xlsx: {e}")
        return {}, {}

V1_PERCENTILE_MAP, FULLNAME_MAP = load_v1_values()

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
    
    # Skip duplicate indices (these are the same data with different names)
    skip_indices = ['NIFTY 10 YR BENCHMARK G-SEC.1']  # Same as N10YRGS
    
    results = []
    
    for col in price_cols:
        # Skip duplicate indices
        if col in skip_indices:
            continue
            
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
        
        # 3. Risk = Std * 3.45 * 0.45
        risk = (annual_vol * 100) * 3.45 * 0.45
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
        
        # Store index results with 3-year return for V1 calculation later
        results.append({
            "Index Name": col,
            "Ret": round(cagr * 100, 1),
            "Risk": round(risk, 1),
            "Momentum_12m": momentum_12m,
            "ThreeYearReturn": None  # Will calculate next
        })
    
    # Calculate 3-year returns for V1 calculation
    three_year_cutoff = df_full.index.max() - pd.DateOffset(years=3)
    
    for result in results:
        col = result["Index Name"]
        full_prices = df_full[col].astype(float).dropna()
        
        # Get last 3 years of data
        three_year_prices = full_prices[full_prices.index >= three_year_cutoff]
        
        if len(three_year_prices) >= 2:
            p_start_3y = three_year_prices.iloc[0]
            p_end_3y = three_year_prices.iloc[-1]
            n_days_3y = (three_year_prices.index[-1] - three_year_prices.index[0]).days
            n_years_3y = n_days_3y / 365.0
            
            if n_years_3y > 0 and p_start_3y > 0:
                cagr_3y = (p_end_3y / p_start_3y) ** (1.0 / n_years_3y) - 1.0
                if np.isfinite(cagr_3y):
                    result["ThreeYearReturn"] = cagr_3y
    
    # Assign V1 values directly from heatmap values.xlsx percentile mapping
    for result in results:
        index_name = result['Index Name']
        if index_name in V1_PERCENTILE_MAP:
            result['V1'] = V1_PERCENTILE_MAP[index_name]
        else:
            result['V1'] = None  # No V1 value if not in heatmap values.xlsx
        
        # Add Full Name from mapping
        if index_name in FULLNAME_MAP:
            result['Full Name'] = FULLNAME_MAP[index_name]
        else:
            # Fallback to index name if no mapping
            try:
                from index_name_mapping import COLUMN_TO_FULLNAME
                result['Full Name'] = COLUMN_TO_FULLNAME.get(index_name, index_name)
            except ImportError:
                result['Full Name'] = index_name
    
    # Remove temporary ThreeYearReturn field
    for result in results:
        if 'ThreeYearReturn' in result:
            del result['ThreeYearReturn']
    
    # Calculate Relative Momentum (RMom) as percentile rank
    # Extract all valid momentum values
    valid_momentum_data = [(i, r['Momentum_12m']) for i, r in enumerate(results) if r['Momentum_12m'] is not None]
    
    if len(valid_momentum_data) > 1:
        # Sort by momentum value to get rankings
        sorted_momentum = sorted(valid_momentum_data, key=lambda x: x[1])
        
        # Assign percentile rank (0-100 scale)
        for rank, (original_idx, momentum_value) in enumerate(sorted_momentum):
            # Percentile = (rank / (n-1)) * 100, where rank starts from 0
            n = len(sorted_momentum)
            if n > 1:
                percentile = (rank / (n - 1)) * 100
            else:
                percentile = 50  # Single value gets 50th percentile
            
            results[original_idx]['RMom'] = round(percentile, 1)
    else:
        # Not enough data to calculate percentile
        for result in results:
            result['RMom'] = None
    
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
            # Formula: ((Current Price - Price X years ago) / Price X years ago)^(1/n) * 100
            if i >= lookback_months:
                past_price = monthly_prices.iloc[i - lookback_months]
                if past_price > 0 and pd.notna(price) and pd.notna(past_price):
                    # Annualized return: ((Current - Past) / Past + 1)^(1/years) - 1
                    annualized_return = (((price / past_price) ** (1.0 / timeline)) - 1.0) * 100
                    heatmap_data[year][month] = float(annualized_return)
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
