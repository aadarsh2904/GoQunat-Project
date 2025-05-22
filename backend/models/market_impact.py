import numpy as np
from scipy.optimize import curve_fit

# Almgren-Chriss market impact function with volatility
def impact_func_with_volatility(q, sigma, eta, alpha):
    """
    Almgren-Chriss market impact function incorporating volatility.
    
    Parameters:
    - q (float or np.array): Order quantity or array of quantities.
    - sigma (float or np.array): Volatility or array of volatilities corresponding to q.
    - eta (float): Market impact scale coefficient.
    - alpha (float): Market impact exponent.
    
    Returns:
    - float or np.array: Predicted market impact(s).
    """
    return eta * (q ** alpha) * sigma

# Example historical data (replace with your actual historical data)
quantities = np.array([10, 50, 100, 200, 500, 1000])
volatilities = np.array([0.01, 0.012, 0.015, 0.014, 0.018, 0.02])
observed_impacts = np.array([0.0003, 0.0015, 0.003, 0.004, 0.007, 0.010])

# Initial guess for parameters for curve fitting
initial_guess = [0.0001, 0.6]

# Wrapper function for curve_fit to handle multiple inputs
def fit_func(q_sigma, eta, alpha):
    q, sigma = q_sigma
    return impact_func_with_volatility(q, sigma, eta, alpha)

# Prepare combined independent variables for curve_fit
independent_vars = np.vstack((quantities, volatilities))

# Calibrate eta and alpha by fitting the model to historical data
params, covariance = curve_fit(fit_func, independent_vars, observed_impacts, p0=initial_guess)
eta_calibrated, alpha_calibrated = params

print(f"Calibrated eta (scale factor): {eta_calibrated:.8f}")
print(f"Calibrated alpha (exponent): {alpha_calibrated:.4f}")

def estimate_market_impact(asks, bids, quantity=100, volatility=0.015):
    """
    Estimate market impact cost for a given order quantity and volatility.
    
    Parameters:
    - asks (list): Order book asks (not used in this simplified model).
    - bids (list): Order book bids (not used in this simplified model).
    - quantity (float): Order quantity.
    - volatility (float): Market volatility (input from server).
    
    Returns:
    - float: Estimated market impact cost rounded to 6 decimals.
    """
    impact = eta_calibrated * (quantity ** alpha_calibrated) * volatility
    return round(impact, 6)

# Example usage with volatility input from server
asks_example = [[95445.5, 9.06]]
bids_example = [[95445.4, 1104.23]]
server_volatility = 0.018  # Example volatility received from server

predicted_impact = estimate_market_impact(asks_example, bids_example, quantity=500, volatility=server_volatility)
print(f"Predicted market impact for quantity 500 with volatility {server_volatility}: {predicted_impact}")
