# 📈 Interactive Algorithmic Trading Strategy Dashboard

This project is a **fully interactive Streamlit-based dashboard** designed to backtest and visualize algorithmic trading strategies like **SMA Crossover**, **RSI**, and **MACD** — using real market data.

---

## ❓ Why This Project?

As the financial world becomes more data-driven, the ability to **code, test, and visualize trading strategies** is an essential skill for aspiring quants and data-driven investors.

I built this project to:
- Transition from healthcare to quantitative finance by building tangible, interview-ready tools
- Learn hands-on how algorithmic strategies behave under real market conditions
- Demonstrate the full data science lifecycle — from ingestion to visualization — in a **production-quality interface**

Whether you're a trader, quant enthusiast, or student, this tool provides a practical gateway into algo strategy research.


---

## Abstract

This project presents the development of an interactive dashboard for backtesting and evaluating algorithmic trading strategies using real financial market data. Built with Python and Streamlit, the tool allows users to simulate and analyze strategies such as SMA Crossover, RSI, and MACD, while adjusting key parameters in real-time. The goal is to bridge the gap between quantitative finance, software engineering, and user-centered design by providing an accessible, visual environment for research and experimentation.

---

## 1. Introduction

The increasing complexity of financial markets and availability of data has elevated the importance of algorithmic trading. Traditional backtesting environments often require deep technical expertise and lack intuitive interfaces for rapid experimentation. This project was initiated as part of my transition from the healthcare domain to quantitative finance, aiming to apply machine learning, data analysis, and programming skills in a financial context.

The core motivation is twofold:
1. To **develop a functional and extensible trading research tool**.
2. To **demonstrate mastery of strategy development, financial modeling, and interactive UI deployment**.

---

## 2. Objectives

- Develop a Streamlit-based dashboard for interactive backtesting
- Implement and visualize common trading strategies (SMA, RSI, MACD)
- Evaluate performance metrics such as Sharpe ratio, drawdown, and win rate
- Make the platform extensible for future strategies and data integrations
- Provide an easy-to-deploy interface suitable for cloud hosting (e.g. Streamlit Cloud)

---

## 3. Methodology

### 3.1 Tools and Libraries
| Technology      | Purpose                             |
|-----------------|-------------------------------------|
| `Streamlit`     | Dashboard UI and interactivity      |
| `Backtrader`    | Trading logic and performance eval  |
| `yFinance`      | Historical financial data           |
| `Plotly`        | Interactive candlestick charting    |
| `Pandas/Numpy`  | Data manipulation and metrics       |

### 3.2 Strategy Logic
Each strategy follows defined rules:
- **SMA Crossover**: Buy when short MA crosses above long MA, sell on opposite crossover.
- **RSI**: Buy when RSI < threshold (e.g., 30), sell when RSI > upper limit (e.g., 70).
- **MACD**: Signal line crossover logic using configurable fast/slow/signal periods.

Backtrader’s internal engine is used to simulate trades and calculate performance analytics.

---

## 4. Implementation

### 4.1 User Interface
The dashboard was built with Streamlit and includes:
- Sidebar controls for stock selection and parameter tuning
- Live data loading from Yahoo Finance via `yFinance`
- Interactive candlestick chart using Plotly
- Summary table of performance metrics post-backtest

### 4.2 Strategy Simulation
Backtrader feeds are created from the downloaded data. Strategies are attached to the `Cerebro` engine dynamically based on user selection. Trade signals are processed and metrics are computed on-the-fly.

### 4.3 Output and Visualization
Results are visualized with:
- Candlestick chart displaying market trends
- Metrics table: Sharpe ratio, drawdown, win rate, total trades
- Console messages for status tracking and user feedback

---

## 5. Results

Example outputs include:
- 📈 AAPL backtested with SMA(10, 30): Sharpe ~1.15, Win Rate ~62%
- 📊 RSI(14) on TSLA: More aggressive trades with frequent signals
- 📉 MACD with tuned parameters reveals trend-following behavior

The visual interface enables users to compare strategies instantly across different tickers and timeframes.

---

## 6. Conclusion

This project successfully demonstrates how open-source tools can be integrated to build a robust, professional-grade trading simulator. Beyond just code, it focuses on usability, interactivity, and real-world application.

### Key Takeaways:
- Strategy logic is modular and reusable
- UI/UX matters in quantitative tools
- Streamlit is a powerful framework for democratizing quant research

---

## 7. Future Work

- Add long/short portfolio strategies with leverage
- Integrate additional data sources (e.g., NewsAPI for sentiment)
- Add chart overlays for trade entry/exit markers
- Incorporate ML-based signal generation



---

## 🚀 How to Run It

### 🧪 1. Clone and Install
```bash
git clone https://github.com/yourusername/algo-trading-dashboard.git
cd algo-trading-dashboard
pip install -r requirements.txt

