import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Step 1: Feature extraction including volatility
def extract_features(asks, bids, quantity, volatility):
    """
    Extract features from order book data, quantity, and volatility.
    
    Parameters:
    - asks: list of [price, qty] for ask side
    - bids: list of [price, qty] for bid side
    - quantity: float, order size
    - volatility: float, current market volatility
    
    Returns:
    - list of features: [spread, depth_imbalance, quantity, volatility]
    """
    if not asks or not bids:
        return [0, 0, 0, volatility]

    best_ask = float(asks[0][0])
    best_bid = float(bids[0][0])
    spread = best_ask - best_bid

    bid_qty_sum = sum(float(qty) for _, qty in bids)
    ask_qty_sum = sum(float(qty) for _, qty in asks)
    depth_imbalance = (bid_qty_sum - ask_qty_sum) / (bid_qty_sum + ask_qty_sum + 1e-9)

    return [spread, depth_imbalance, quantity, volatility]

# Step 2: Generate synthetic training data including volatility
def generate_synthetic_data(n=1000):
    """
    Generate synthetic data for slippage prediction including volatility.
    
    Parameters:
    - n: int, number of samples
    
    Returns:
    - X: np.array, features matrix
    - y: np.array, target vector (slippage)
    """
    np.random.seed(42)
    spreads = np.random.uniform(0.01, 0.1, n)
    depth_imbalances = np.random.uniform(-1, 1, n)
    quantities = np.random.uniform(10, 500, n)
    volatilities = np.random.uniform(0.005, 0.03, n)  # Typical intraday volatility range

    # Slippage formula with noise and volatility effect
    slippage = (
        0.4 * spreads
        + 0.3 * np.abs(depth_imbalances)
        + 0.0005 * quantities
        + 0.2 * volatilities  # Volatility contribution
        + np.random.normal(0, 0.005, n)
    )
    slippage = np.maximum(slippage, 0)  # Slippage can't be negative

    X = np.column_stack((spreads, depth_imbalances, quantities, volatilities))
    y = slippage
    return X, y

# Step 3: Train model
X, y = generate_synthetic_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Prediction function using trained model including volatility
def estimate_slippage(asks, bids, quantity=100, volatility=0.015):
    """
    Estimate slippage given order book, quantity, and volatility.
    
    Parameters:
    - asks: list of [price, qty] for ask side
    - bids: list of [price, qty] for bid side
    - quantity: float, order size
    - volatility: float, current market volatility
    
    Returns:
    - float: predicted slippage rounded to 6 decimals
    """
    features = extract_features(asks, bids, quantity, volatility)
    slippage_pred = model.predict([features])[0]
    return round(slippage_pred, 6)
