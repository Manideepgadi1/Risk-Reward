# Risk-Reward Analysis - Complete Formulas Documentation

## 📊 Metrics Calculated

### 1. **Return (Ret) - CAGR (Compound Annual Growth Rate)**
```
Formula: CAGR = (P_end / P_start)^(1/n) - 1

Where:
- P_end = Final price (most recent date)
- P_start = Initial price (earliest date)
- n = Number of years in the period

Example:
If NIFTY 50 went from 10,000 to 24,000 in 5 years:
CAGR = (24000 / 10000)^(1/5) - 1 = 0.1914 = 19.14%

Display: Multiplied by 100, rounded to 1 decimal place
```

**Purpose**: Measures the annualized rate of return over the investment period

---

### 2. **Std (Standard Deviation) - Volatility**
```
Formula: Annual Volatility = Daily_Std × √252

Where:
- Daily_Std = Standard deviation of daily returns
- Daily returns = (P_today - P_yesterday) / P_yesterday
- 252 = Average trading days per year
- √252 = 15.87 (annualization factor)

Step-by-step:
1. Calculate daily returns: daily_returns = prices.pct_change()
2. Calculate daily standard deviation: daily_std = std(daily_returns)
3. Annualize: annual_volatility = daily_std × 15.87

Example:
If daily_std = 0.015 (1.5%)
Annual volatility = 0.015 × 15.87 = 0.238 = 23.8%

Display: Multiplied by 100, rounded to 1 decimal place
```

**Purpose**: Measures the volatility/variability of returns - higher values indicate more price fluctuation

---

### 3. **Risk**
```
Formula: Risk = Annualized Volatility

Risk = Daily_Std × √252

(Same calculation as Std, but displayed as decimal)

Example:
If daily_std = 0.015 (1.5%)
Annual volatility = 0.015 × 15.87 = 0.238

Display: As decimal value (0.xx format), rounded to 2 decimal places
Example: 0.46, 0.88, 0.92
```

**Purpose**: Quantifies investment risk based on price volatility

---

### 4. **Mom (Momentum) - 12-Month Return**
```
Formula: Momentum = (P_current - P_12months_ago) / P_12months_ago × 100

Where:
- P_current = Most recent price
- P_12months_ago = Price 252 trading days ago (1 year)

Fallback (if less than 12 months of data):
Momentum_6m = (P_current - P_6months_ago) / P_6months_ago × 100

Where:
- P_6months_ago = Price 126 trading days ago (6 months)

If less than 6 months: Momentum = 0

Example:
If current price = 24,000 and 12-month-ago price = 20,000:
Momentum = (24000 - 20000) / 20000 × 100 = 20%

Display: Rounded to 1 decimal place
```

**Purpose**: Measures recent price performance over the last 12 months

---

### 5. **Mean**
```
Formula: Mean = (Return + Risk) / 2

Where:
- Return = CAGR percentage
- Risk = Volatility percentage

Example:
If Return = 19.1% and Risk = 23.8%:
Mean = (19.1 + 23.8) / 2 = 21.45%

Display: Rounded to 1 decimal place
```

**Purpose**: Average of return and risk metrics

---

## 🎨 Color Coding Thresholds

### For Return (Ret):
| Color | Range | Hex Code | Description |
|-------|-------|----------|-------------|
| **Dark Green** | ≥ 25% | `#047857` | Excellent performance |
| **Medium Green** | 19% - 25% | `#10b981` | Very good performance |
| **Light Green** | 15% - 19% | `#6ee7b7` | Good performance |
| **Very Light Green** | 10% - 15% | `#a7f3d0` | Above average |
| **Light Red** | 5% - 10% | `#f87171` | Below average |
| **Red** | < 5% | `#b91c1c` | Poor performance |

### For Std (Standard Deviation - shown as %):
| Color | Range | Hex Code | Description |
|-------|-------|----------|-------------|
| **Dark Green** | ≤ 28% | `#047857` | Very low volatility |
| **Light Green** | 28% - 50% | `#6ee7b7` | Low volatility |
| **Very Light Green** | 50% - 88% | `#a7f3d0` | Moderate volatility |
| **Medium Green** | 88% - 92% | `#10b981` | Moderate-high volatility |
| **Very Light Green** | 92% - 100% | `#a7f3d0` | High volatility |
| **Light Red** | > 100% | `#f87171` | Very high volatility |

### For Risk (shown as decimal 0.xx):
| Color | Range | Hex Code | Description |
|-------|-------|----------|-------------|
| **Dark Green** | ≤ 0.28 | `#047857` | Very low risk |
| **Light Green** | 0.28 - 0.50 | `#6ee7b7` | Low risk |
| **Very Light Green** | 0.50 - 0.88 | `#a7f3d0` | Moderate risk |
| **Medium Green** | 0.88 - 0.92 | `#10b981` | Moderate-high risk |
| **Very Light Green** | 0.92 - 1.0 | `#a7f3d0` | High risk |
| **Light Red** | > 1.0 | `#f87171` | Very high risk |

### For Momentum (Mom):
| Color | Range | Hex Code | Description |
|-------|-------|----------|-------------|
| **Dark Green** | ≥ 25% | `#047857` | Strong upward momentum |
| **Medium Green** | 15% - 25% | `#10b981` | Good momentum |
| **Light Green** | 5% - 15% | `#6ee7b7` | Positive momentum |
| **Very Light Green** | 0% - 5% | `#a7f3d0` | Slight positive |
| **Light Red** | -5% to 0% | `#f87171` | Slight negative |
| **Red** | < -5% | `#b91c1c` | Negative momentum |

---

## 📅 Duration Filtering

The system supports three duration options:

### 1. **3 Years**
- Filters data to last 3 years from most recent date
- Calculation: `cutoff_date = max_date - 3 years`
- All metrics calculated using only data within this period

### 2. **5 Years**
- Filters data to last 5 years from most recent date
- Calculation: `cutoff_date = max_date - 5 years`
- All metrics calculated using only data within this period

### 3. **All Time**
- Uses complete dataset from 2005 to 2025
- No filtering applied
- Calculates metrics across entire available history

---

## 📈 Heatmap Calculations

### Month-over-Month Returns
```
Formula: Monthly_Return = (P_month_end - P_previous_month_end) / P_previous_month_end × 100

Process:
1. Resample daily prices to monthly (last day of each month)
2. Calculate percentage change between consecutive months
3. Structure data by year and month

Display: Color-coded cells with 8-color gradient
```

### Heatmap Color Scale:
| Color | Range | Hex Code |
|-------|-------|----------|
| **Dark Red** | < -5% | `#d32f2f` to `#b71c1c` |
| **Medium Red** | -5% to -3% | `#e57373` to `#ef5350` |
| **Light Red** | -3% to -1% | `#ef9a9a` to `#e57373` |
| **Very Light Red** | -1% to 0% | `#ffcdd2` to `#ef9a9a` |
| **Very Light Yellow** | 0% to 1% | `#fff9c4` to `#fff59d` |
| **Light Green** | 1% to 3% | `#c8e6c9` to `#a5d6a7` |
| **Medium Green** | 3% to 5% | `#81c784` to `#66bb6a` |
| **Dark Green** | > 5% | `#4caf50` to `#388e3c` |

---

## 🔢 Data Processing Details

### Input Data Format:
- CSV file with DATE column (format: dd/mm/yy)
- 126 index price columns
- Daily price data from 2005 to 2025
- Total rows: 7,378 daily records

### Trading Day Assumptions:
- 252 trading days per year (used for annualization)
- 21 trading days per month (average)
- 126 trading days = 6 months
- 252 trading days = 12 months

### Data Cleaning:
- Missing values are dropped (NaN handling)
- Invalid calculations (inf, -inf) are excluded
- Zero prices are skipped to avoid division errors

---

## 📊 Summary for Review Meeting

**Key Points to Note:**

1. **Return (CAGR)** = Annualized growth rate using geometric mean
2. **Std & Risk** = Same value, showing annualized volatility (daily std × √252)
3. **Momentum** = 12-month trailing return percentage
4. **Mean** = Simple average of Return and Risk
5. **Duration Filter** = Dynamically recalculates all metrics for 3Y/5Y/All periods
6. **Color Coding** = Visual indicators for quick performance assessment
7. **Heatmap** = Month-by-month return visualization with gradient colors

All formulas are industry-standard financial metrics used for equity analysis and portfolio management.
