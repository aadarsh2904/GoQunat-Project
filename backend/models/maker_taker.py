import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Step 1: Feature extraction including volatility
def extract_features(asks, bids, volatility):
    """
    Extract features: spread and volatility.
    
    Parameters:
    - asks: List of [price, quantity] for ask side
    - bids: List of [price, quantity] for bid side
    - volatility: Current market volatility (float)
    
    Returns:
    - List of features: [spread, volatility]
    """
    if not asks or not bids:
        return [0.0, volatility]
    best_ask = float(asks[0][0])
    best_bid = float(bids[0][0])
    spread = best_ask - best_bid
    return [spread, volatility]

# Step 2: Generate synthetic data with spread and volatility
def generate_synthetic_maker_taker_data(n=1200):
    """
    Generate synthetic data with spread and volatility features.
    
    Returns:
    - X: Feature matrix with columns [spread, volatility]
    - y: Binary labels (1=maker, 0=taker)
    """
    np.random.seed(42)
    
    # Generate spreads uniformly between 0.002 and 0.12
    spreads = np.random.uniform(0.002, 0.12, n)
    
    # Generate volatilities uniformly between 0.005 and 0.03 (typical intraday vol range)
    volatilities = np.random.uniform(0.005, 0.03, n)
    
    # Simulate logits with both spread and volatility influencing maker probability
    logits = -4 + 40 * spreads - 20 * volatilities  # Volatility negatively impacts maker probability here
    
    probs = 1 / (1 + np.exp(-logits))
    
    labels = np.random.binomial(1, probs)
    
    print("Class distribution (0=taker, 1=maker):", np.bincount(labels))
    
    X = np.column_stack((spreads, volatilities))
    y = labels
    return X, y

# Step 3: Train logistic regression model
X, y = generate_synthetic_maker_taker_data()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# Step 4: Prediction function including volatility input
def estimate_maker_taker(asks, bids, volatility):
    """
    Predict maker/taker probabilities using spread and volatility features.
    
    Parameters:
    - asks: List of [price, quantity] for ask side
    - bids: List of [price, quantity] for bid side
    - volatility: Current market volatility (float)
    
    Returns:
    - Dictionary with keys 'maker' and 'taker' containing probabilities.
    """
    features = extract_features(asks, bids, volatility)
    prob_maker = logreg.predict_proba([features])[0][1]
    prob_taker = 1 - prob_maker
    return {"maker": prob_maker, "taker": prob_taker}
