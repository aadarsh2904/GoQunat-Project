# 📈 Real-Time Crypto Trade Simulator

A high-performance, real-time trade simulator for cryptocurrency markets that estimates slippage, fees, market impact, and more — built using Python for backend and modeling, and Next.js for the frontend UI.

## 📝 Description

This project is a real-time cryptocurrency trade simulator built for developers, traders, and finance enthusiasts who want to dive deep into how trades behave in live markets. Whether you're learning about algorithmic trading, exploring market microstructure, or just curious about transaction costs — this tool gives you a clear, interactive way to see it all in action.

By connecting to the OKX WebSocket feed, it streams live Level 2 order book data and uses advanced models like Almgren-Chriss, logistic regression, and linear regression to estimate parameters like slippage, expected fees, and net cost. You can tweak inputs like the trading asset, order type, quantity, and volatility through an intuitive interface, and the system instantly reacts to show how each choice affects your trade outcomes.

Perfect for students, quants, or engineers building intelligent trading systems.

---

## 🚀 Features

- 📡 Real-time WebSocket streaming from OKX
- ⚙️ Backend modeling in Python with:
  - Almgren-Chriss for market impact
  - Linear regression for slippage
  - Logistic regression for maker/taker classification
- 🌐 Clean and responsive UI built with Next.js and Tailwind CSS
- 💰 Customizable inputs (asset, order type, fee tier, volatility, etc.)
- 📊 Live output updates for:
  - Expected Slippage
  - Expected Fees
  - Market Impact
  - Net Transaction Cost
  - Maker/Taker Proportion
  - Internal Latency

---

## 🧠 Models Used

- **Almgren-Chriss Model**: Used to estimate market impact cost during order execution.
- **Linear/Quantile Regression**: Used to predict expected slippage based on current order book conditions.
- **Logistic Regression**: Used to predict whether an order is likely to be filled as a maker or taker.
- **Synthetic Data**: Employed for training models like logistic regression due to the absence of labeled real data.

---

## 🧪 Handling Data Imbalance

To avoid issues like class imbalance in classification (e.g., predicting maker/taker), synthetic datasets were carefully generated using logistic transformations. Thresholds were applied on the probability outputs to simulate realistic distributions of maker and taker labels.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js, Tailwind CSS
- **Backend**: Python
- **Machine Learning**: scikit-learn (Logistic & Linear Regression)
- **WebSocket**: Native Python + OKX L2 Order Book Feed
- **Hosting**: Runs locally

---

## ⚙️ Local Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- A VPN (to access OKX WebSocket in some regions)

---

### 🧩 Steps to Run the Project Locally

```bash
# Clone the repository
git clone https://github.com/aadarsh2904/GoQunat-Simulator.git
cd your-GoQunat-Simulator

📦 Backend Setup (Python)
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the backend (adjust path if necessary)
fastapi run main.py

🌐 Frontend Setup (Next.js)
# Navigate to frontend directory
cd go-quant

# Install frontend dependencies
npm install

# Start the development server
npm run dev
