import numpy as np
import pandas as pd

def calculate_pnl(data: pd.DataFrame):
    # Assume data contains 'asset_value' and 'quantity' columns
    data['pnl'] = data['asset_value'] * data['quantity']
    total_pnl = np.sum(data['pnl'])
    return total_pnl

def calculate_risk_exposure(data: pd.DataFrame):
    # Simple VaR calculation using historical method (for demonstration)
    returns = data['asset_value'].pct_change().dropna()
    var = np.percentile(returns, 5) * np.sqrt(len(returns))
    return var
