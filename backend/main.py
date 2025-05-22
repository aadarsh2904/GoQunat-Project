from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import time

import okx.MarketData as MarketData

from models.slippage import estimate_slippage
from models.fees import estimate_fees
from models.market_impact import estimate_market_impact
from models.maker_taker import estimate_maker_taker
from utils.latency import measure_latency

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

flag = "0"  # Production trading:0 , demo trading:1
marketDataAPI = MarketData.MarketAPI(flag=flag)


class InputParams(BaseModel):
    exchange: str
    spotAsset: str
    orderType: str
    quantity: float
    volatility: float
    feeTier: str


@app.post("/")
async def compute(params: InputParams):
    start_time = time.perf_counter()
    try:
        # Fetch tickers for SWAP instruments
        result = marketDataAPI.get_tickers(instType="SWAP")
        if result.get("code") != "0":
            raise HTTPException(status_code=502, detail="Failed to fetch market data")

        # Find the instrument matching spotAsset (e.g. "BTC-USDT-SWAP")
        inst_id = f"{params.spotAsset}-SWAP"
        instrument_data = next(
            (item for item in result["data"] if item["instId"] == inst_id), None
        )
        if instrument_data is None:
            raise HTTPException(status_code=404, detail="Instrument not found")

        # Construct asks and bids for model inputs
        # Here we approximate asks and bids from best ask/bid prices and sizes
        asks = [[instrument_data["askPx"], instrument_data["askSz"]]]
        bids = [[instrument_data["bidPx"], instrument_data["bidSz"]]]

        # Calculate outputs
        slippage = estimate_slippage(asks, bids, quantity=params.quantity,volatility=params.volatility)
        fees = estimate_fees(asks, bids,volatility=params.volatility)
        market_impact = estimate_market_impact(asks, bids, quantity=params.quantity ,volatility=params.volatility)
        net_cost = slippage + fees + market_impact
        maker_taker = estimate_maker_taker(asks, bids,volatility=params.volatility)
        latency_ms = measure_latency(start_time)

        return {
            "slippage": slippage,
            "fees": fees,
            "marketImpact": market_impact,
            "cost": net_cost,
            "makerTaker": maker_taker,
            "latency": latency_ms,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
