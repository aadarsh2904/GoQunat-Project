import okx.MarketData as MarketData
import time

flag = "0"  # Production trading:0 , demo trading:1

start_tick = time.perf_counter()

marketDataAPI =  MarketData.MarketAPI(flag=flag)

# Retrieve order book of the instrument
result = marketDataAPI.get_tickers(
    instType="SWAP"
)
print(result)
print(len(result['data']))
print((time.perf_counter() - start_tick) * 1000)