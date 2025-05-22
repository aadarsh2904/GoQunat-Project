def estimate_fees(asks, bids, quantity_usd=100, fee_tier=1, is_maker=False, volatility=0.02):
    """
    Estimate trading fees based on notional amount, fee tier, order type, and market volatility.
    
    Parameters:
        asks (list): Order book asks [[price, qty], ...]
        bids (list): Order book bids [[price, qty], ...]
        quantity_usd (float): Trade size in USD
        fee_tier (int): Fee tier level (1, 2, 3, ...)
        is_maker (bool): True if maker order, False if taker order
        volatility (float): Current market volatility (e.g., realized volatility)
    
    Returns:
        float: Estimated fee amount in USD, adjusted by volatility
    """
    # Return zero fee if order book data is missing
    if not asks or not bids:
        return 0.0
    
    # Fee tiers example (OKX-like), adjusted for demonstration
    fee_structure = {
        1: {'maker': 0.0009, 'taker': 0.0011},
        2: {'maker': 0.0007, 'taker': 0.0009},
        3: {'maker': 0.0005, 'taker': 0.0007},
    }
    
    # Use best ask price for notional calculation (assuming buy order)
    best_ask = float(asks[0][0])
    
    # Notional trade value in USD (assuming quantity_usd is already USD)
    notional = quantity_usd
    
    # Select fee rate based on fee tier and order type (maker/taker)
    tier_fees = fee_structure.get(fee_tier, fee_structure[1])
    fee_rate = tier_fees['maker'] if is_maker else tier_fees['taker']
    
    # Adjust fee rate by volatility factor (example: fee increases by up to 20% if volatility is high)
    volatility_adjustment = 1 + min(max(volatility / 0.05, 0), 0.2)  # Caps adjustment between 0 and 20%
    
    # Calculate total fee with volatility adjustment
    fee = notional * fee_rate * volatility_adjustment
    
    # Round fee to 6 decimal places for precision
    return round(fee, 6)
