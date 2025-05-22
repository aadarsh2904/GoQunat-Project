import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import okx.MarketData as MarketData

flag = "0"  # Production trading:0 , demo trading:1

marketDataAPI =  MarketData.MarketAPI(flag=flag)

result = marketDataAPI.get_tickers(
    instType="SWAP"
)

data = result['data']

# Convert raw data to DataFrame
df = pd.DataFrame(data)

# Convert numeric columns
numeric_cols = ['last', 'lastSz', 'askPx', 'askSz', 'bidPx', 'bidSz', 
                'open24h', 'high24h', 'low24h', 'volCcy24h', 'vol24h',
                'sodUtc0', 'sodUtc8']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Remove non-essential columns
df_clean = df.drop(columns=['instType', 'instId', 'ts']).dropna()

df_clean['expected_slippage'] = (df_clean['askPx'] - df_clean['bidPx']) / df_clean['last']

from sklearn.linear_model import LinearRegression

features = ['last', 'lastSz', 'askPx', 'askSz', 'bidPx', 'bidSz',
            'open24h', 'high24h', 'low24h', 'volCcy24h', 'vol24h',
            'sodUtc0', 'sodUtc8']

X = df_clean[features]
y = df_clean['expected_slippage']

model = LinearRegression()
model.fit(X, y)

import pickle

filename = 'linear.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)