import next from "next";
import Image from "next/image";
import { Geist, Geist_Mono } from "next/font/google";
import { useState, useEffect } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const defaultResults = {
  slippage: "-",
  fees: "-",
  marketImpact: "-",
  cost: "-",
  makerTaker: {
    maker: "-",
    taker: "-",
  },
  latency: "-",
}

export default function Home() {
  const [form, setForm] = useState({
    exchange: "OKX",
    spotAsset: "BTC-USDT",
    orderType: "market",
    quantity: 100,
    volatility: 0,
    feeTier: "standard",
  });

  const [results, setResults] = useState(defaultResults);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  console.log("Form data:", form);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setResults(defaultResults);
    try {
      const res = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          quantity: Number(form.quantity),
          volatility: Number(form.volatility),
        }),
      });

      console.log("Response:", res);

      if (!res.ok) throw new Error("Failed to fetch data");
      const data = await res.json();

      console.log("Data:", data);

      setResults(data);
    } catch (err) {
      setResults({ error: err.message });
    }
  };

  return (
    <div
      className={`${geistSans.className} ${geistMono.className} h-screen p-6 pb-14 gap-12 sm:p-14 font-[family-name:var(--font-geist-sans)] flex flex-col items-center
      bg-[url('/abstract-futuristic.jpg')] bg-cover bg-center bg-no-repeat filter hue-rotate-300 overflow-hidden`}
    >
      <div className="font-bold text-4xl text-center mt-2 mb-2">GetQuant</div>
      <div className="w-full flex gap-6 max-w-4xl">
        <div className="flex-1 p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/10 shadow-lg text-blue-400 saturate-100 text-sm">
            <div className="flex flex-col gap-3">
              <label className="flex flex-col gap-1">
                <span>Exchange (OKX)</span>
                <input
                  value={form.exchange} onChange={handleChange}
                  type="text"
                  name="exchange"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Spot Asset</span>
                <input
                  value={form.spotAsset} onChange={handleChange}
                  type="text"
                  name="spotAsset"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Order Type (market)</span>
                <input
                  value={form.orderType}
                  type="text"
                  name="orderType"
                  defaultValue="market"
                  disabled
                  className="border border-solid dark:border-white/[.145] transition-colors bg-[#f2f2f2] dark:bg-[#1a1a1a] border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Quantity (~100 USD equivalent)</span>
                <input
                  value={form.quantity}
                  type="text"
                  name="quantity"
                  defaultValue="100$"
                  disabled
                  className="border border-solid dark:border-white/[.145] transition-colors bg-[#f2f2f2] dark:bg-[#1a1a1a] border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Volatility (market parameter)</span>
                <input
                  value={form.volatility} onChange={handleChange}
                  type="text"
                  name="volatility"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Fee Tier</span>
                <input
                  value={form.feeTier} onChange={handleChange}
                  type="text"
                  name="feeTier"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-28"
                />
              </label>
            </div>
            <button
              onClick={(e) => {
                handleSubmit(e);
              }}
              className="mt-3 rounded-full border border-solid border-transparent transition-colors bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 w-28"
            >
              Submit
            </button>
        </div>
        <div className="flex-1 p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/10 shadow-lg">
              <div className="flex flex-col gap-3">
              <label className="flex flex-col gap-1">
                <span>Expected Slippage</span>
                <input
                  value={results.slippage}
                  type="text"
                  name="slippage"
                  disabled
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Expected Fees</span>
                <input
                  value={results.fees}
                  type="text"
                  disabled
                  name="expectedFees"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Expected Market Impact</span>
                <input
                  value={results.marketImpact}
                  type="text"
                  name="marketImpact"
                  disabled
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Net Cost</span>
                <input
                  value={results.cost}
                  type="text"
                  name="cost"
                  disabled
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Maker Taker Proportion</span>
                <input
                  value={`${results.makerTaker.maker} vs ${results.makerTaker.taker}`}
                  type="text"
                  name="makerTaker"
                  readOnly
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
              <label className="flex flex-col gap-1">
                <span>Internal Latency (ms)</span>
                <input
                  value={results.latency}
                  type="text"
                  disabled
                  name="latency"
                  className="border border-solid border-black/[.08] dark:border-white/[.145] transition-colors hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-xs sm:text-sm h-7 sm:h-8 px-3 sm:px-4 rounded-full w-56"
                />
              </label>
            </div>
        </div>
      </div>
    </div>
  );
}
