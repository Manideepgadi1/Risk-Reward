"""Core metrics calculation module"""

import pandas as pd
import numpy as np
import os


class RiskRewardAPI:
    """API class for calculating risk-reward metrics for stock indices"""
    
    def __init__(self, csv_path=None, excel_path=None):
        """
        Initialize the API with data file path
        
        Args:
            csv_path: Path to CSV file with price data. If None, uses default data.csv
            excel_path: Path to Excel file with V1 values. If None, uses default heatmap values.xlsx
        """
        if csv_path is None:
            # Use package's default data file
            package_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(package_dir, 'data.csv')
        
        if excel_path is None:
            # Use default Excel file in parent directory
            package_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(os.path.dirname(package_dir), 'heatmap values.xlsx')
        
        self.csv_path = csv_path
        self.excel_path = excel_path
        self._df = None
        self._v1_df = None
        self._load_v1_values()
    
    def load_data(self):
        """Load and prepare data from CSV"""
        if self._df is None:
            self._df = pd.read_csv(self.csv_path)
            if "DATE" not in self._df.columns:
                raise ValueError("Expected a 'DATE' column in the CSV.")
            
            # Parse DATE and sort
            self._df["DATE"] = pd.to_datetime(self._df["DATE"], format='%d/%m/%y', errors="coerce")
            self._df = self._df.dropna(subset=["DATE"]).sort_values("DATE")
            self._df = self._df.set_index("DATE")
        
        return self._df
    
    def _load_v1_values(self):
        """Load V1 (percentile) values from Excel file"""
        try:
            # Load mapping
            import sys
            mapping_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index_name_mapping.py')
            if os.path.exists(mapping_path):
                import importlib.util
                spec = importlib.util.spec_from_file_location("index_name_mapping", mapping_path)
                mapping_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mapping_module)
                fullname_to_column = mapping_module.FULLNAME_TO_COLUMN
                column_to_fullname = mapping_module.COLUMN_TO_FULLNAME
            else:
                fullname_to_column = {}
                column_to_fullname = {}
            
            self._v1_df = pd.read_excel(self.excel_path)
            # Create mapping from CSV column name (short code) to Percentile Value and Full Name
            self._v1_map = {}
            self._fullname_map = {}
            
            for idx, row in self._v1_df.iterrows():
                full_name = row['Full Name']
                percentile = row['Percentile Value']
                
                # Try to map full name to column name
                column_name = fullname_to_column.get(full_name, full_name)
                
                self._v1_map[column_name] = round(percentile, 2)
                self._fullname_map[column_name] = full_name
                
        except Exception as e:
            print(f"Warning: Could not load V1 values from Excel: {e}")
            self._v1_map = {}
            self._fullname_map = {}
    
    def get_metrics(self, duration='all', indices=None):
        """
        Calculate metrics for indices
        
        Args:
            duration: '3years', '5years', or 'all'
            indices: List of specific index names to calculate. None = all indices
            
        Returns:
            List of dictionaries with metrics for each index
        """
        df_full = self.load_data()
        df = df_full.copy()
        
        # Filter by duration
        if duration == '3years':
            cutoff_date = df.index.max() - pd.DateOffset(years=3)
            df = df[df.index >= cutoff_date]
        elif duration == '5years':
            cutoff_date = df.index.max() - pd.DateOffset(years=5)
            df = df[df.index >= cutoff_date]
        
        price_cols = df.columns
        if indices:
            price_cols = [col for col in price_cols if col in indices]
        
        results = []
        
        for col in price_cols:
            prices = df[col].astype(float)
            non_na = prices.dropna()
            
            if len(non_na) < 2:
                continue
            
            full_prices = df_full[col].astype(float).dropna()
            
            p_start = non_na.iloc[0]
            p_end = non_na.iloc[-1]
            n_days = (non_na.index[-1] - non_na.index[0]).days
            
            if n_days <= 0 or p_start == 0:
                continue
            
            n_years = n_days / 365.0
            if n_years == 0:
                continue
            
            # 1. Return (CAGR)
            cagr = (p_end / p_start) ** (1.0 / n_years) - 1.0
            if not np.isfinite(cagr):
                continue
            
            # 2. Volatility
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
            
            # 4. 12-month momentum
            momentum_12m = None
            if len(non_na) >= 252:
                p_current = non_na.iloc[-1]
                p_12m_ago = non_na.iloc[-252]
                if p_12m_ago != 0:
                    momentum_12m = ((p_current - p_12m_ago) / p_12m_ago) * 100
                
                if momentum_12m is not None and not np.isfinite(momentum_12m):
                    momentum_12m = None
            
            # 5. 5-year cumulative return for V1
            cumulative_return_5y = None
            latest_date = full_prices.index.max()
            latest_value = full_prices.iloc[-1]
            target_date_5y_ago = latest_date - pd.DateOffset(years=5)
            dates_before_target = full_prices.index[full_prices.index <= target_date_5y_ago]
            
            if len(dates_before_target) > 0:
                closest_date_5y_ago = dates_before_target[-1]
                value_5y_ago = full_prices.loc[closest_date_5y_ago]
                
                if value_5y_ago > 0:
                    cumulative_return_5y = ((latest_value / value_5y_ago) - 1.0) * 100
            
            # 6. Average Monthly Profit (4 years)
            avg_monthly_profit_4y = None
            four_year_cutoff = latest_date - pd.DateOffset(years=4)
            four_year_prices = full_prices[full_prices.index >= four_year_cutoff]
            
            if len(four_year_prices) > 1:
                monthly_prices = four_year_prices.resample('M').last().dropna()
                
                if len(monthly_prices) > 1:
                    monthly_returns = monthly_prices.pct_change().dropna() * 100
                    
                    if len(monthly_returns) > 0:
                        avg_monthly_profit_4y = monthly_returns.sum() / len(monthly_returns)
            
            # 7. Mean
            mean = (cagr * 100 + risk * 100) / 2
            
            results.append({
                "Index Name": col,
                "Ret": round(cagr * 100, 1),
                "Cumulative_5y": cumulative_return_5y,
                "AvgMonthlyProfit_4y": round(avg_monthly_profit_4y, 2) if avg_monthly_profit_4y is not None else None,
                "Risk": round(risk, 1),
                "Mean": round(mean, 1),
                "Momentum_12m": momentum_12m
            })
        
        # Get V1 values from Excel file and add full names
        for result in results:
            index_name = result['Index Name']
            # Get V1 from Excel mapping
            result['V1'] = self._v1_map.get(index_name, None)
            if result['V1'] is not None:
                result['V1'] = round(result['V1'], 3)
            
            # Add full display name
            result['Full Name'] = self._fullname_map.get(index_name, index_name)
            
            del result['Cumulative_5y']
        
        # Calculate momentum ratio
        valid_momentum_12m = [r['Momentum_12m'] for r in results if r['Momentum_12m'] is not None]
        
        if len(valid_momentum_12m) > 1:
            avg_momentum = np.mean(valid_momentum_12m)
            sd_momentum = np.std(valid_momentum_12m, ddof=1)
            
            for result in results:
                if result['Momentum_12m'] is not None and sd_momentum > 0:
                    momentum_ratio = (result['Momentum_12m'] - avg_momentum) / sd_momentum
                    result['Momentum'] = round(momentum_ratio, 2)
                    
                    abs_momentum = result['Momentum_12m'] / sd_momentum
                    result['AbsMom'] = round(abs_momentum, 2)
                else:
                    result['Momentum'] = None
                    result['AbsMom'] = None
        else:
            for result in results:
                result['Momentum'] = None
                result['AbsMom'] = None
        
        for result in results:
            del result['Momentum_12m']
        
        return results
    
    def get_index_data(self, index_name):
        """
        Get raw price data for a specific index
        
        Args:
            index_name: Name of the index
            
        Returns:
            pandas Series with date index and prices
        """
        df = self.load_data()
        if index_name not in df.columns:
            raise ValueError(f"Index '{index_name}' not found in data")
        
        return df[index_name].dropna()
    
    def get_available_indices(self):
        """
        Get list of all available index names
        
        Returns:
            List of index names
        """
        df = self.load_data()
        return df.columns.tolist()
