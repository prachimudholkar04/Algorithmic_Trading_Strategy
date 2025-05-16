# streamlit_app.py (with interactive Plotly chart)

import streamlit as st
import yfinance as yf
import pandas as pd
import backtrader as bt
import datetime
import plotly.graph_objects as go

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")
st.title("📈 Interactive Algo Trading Strategy Dashboard")

# Sidebar Inputs
st.sidebar.header("🔧 Strategy Configuration")
ticker = st.sidebar.text_input("Stock Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())
strategy_option = st.sidebar.selectbox("Strategy", ["SMA Crossover", "RSI", "MACD"])

# Strategy Parameters
if strategy_option == "SMA Crossover":
    fast = st.sidebar.slider("Fast MA Period", 5, 30, 10)
    slow = st.sidebar.slider("Slow MA Period", 20, 100, 30)
elif strategy_option == "RSI":
    rsi_period = st.sidebar.slider("RSI Period", 7, 21, 14)
    rsi_buy = st.sidebar.slider("RSI Buy Threshold", 10, 50, 30)
    rsi_sell = st.sidebar.slider("RSI Sell Threshold", 50, 90, 70)
elif strategy_option == "MACD":
    macd_fast = st.sidebar.slider("MACD Fast", 5, 15, 12)
    macd_slow = st.sidebar.slider("MACD Slow", 20, 40, 26)
    macd_signal = st.sidebar.slider("MACD Signal", 5, 15, 9)

# -----------------------------
# Download Market Data
# -----------------------------
symbol = 'AAPL'
data = yf.download(symbol, start='2020-01-01', end='2025-12-31', auto_adjust=False)
data.columns = [col if isinstance(col, str) else col[0] for col in data.columns]
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data.to_csv('data.csv')
data_load_state = st.text("Downloading data...")
data = yf.download(symbol, start='2020-01-01', end='2025-12-31', auto_adjust=False)
data.columns = [col if isinstance(col, str) else col[0] for col in data.columns]
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data.to_csv('data.csv')

min_period_required = max(fast, slow) if strategy_option == "SMA Crossover" else 30
if len(data) < min_period_required:
    st.error(f"Not enough data to calculate indicators. Please select a wider date range.")
    st.stop()

# -----------------------------
# Strategy Execution (No trades plotted for now)
# -----------------------------
class PandasData(bt.feeds.PandasData):
    params = dict(datetime=None, open=-1, high=-1, low=-1, close=-1, volume=-1, openinterest=-1)

class SmaCross(bt.Strategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=fast)
        sma2 = bt.ind.SMA(period=slow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()

class RsiStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.ind.RSI(period=rsi_period)

    def next(self):
        if not self.position:
            if self.rsi < rsi_buy:
                self.buy()
        elif self.rsi > rsi_sell:
            self.sell()

class MacdStrategy(bt.Strategy):
    def __init__(self):
        macd = bt.ind.MACD(period_me1=macd_fast, period_me2=macd_slow, period_signal=macd_signal)
        self.crossover = bt.ind.CrossOver(macd.macd, macd.signal)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()


cerebro = bt.Cerebro()
cerebro.broker.set_cash(10000)
datafeed = PandasData(dataname=data)
cerebro.adddata(datafeed)

if strategy_option == "SMA Crossover":
    cerebro.addstrategy(SmaCross)
elif strategy_option == "RSI":
    cerebro.addstrategy(RsiStrategy)
elif strategy_option == "MACD":
    cerebro.addstrategy(MacdStrategy)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
results = cerebro.run()
strat = results[0]

# -----------------------------
# Show Metrics
# -----------------------------
sharpe = strat.analyzers.sharpe.get_analysis()
drawdown = strat.analyzers.drawdown.get_analysis()
trades = strat.analyzers.trades.get_analysis()

metrics = {
    "Final Portfolio Value": [round(cerebro.broker.getvalue(), 2)],
    "Sharpe Ratio": [sharpe.get('sharperatio', 'N/A')],
    "Max Drawdown (%)": [drawdown.get('max', {}).get('drawdown', 'N/A')],
    "Total Trades": [trades.get('total', {}).get('total', 'N/A')],
    "Win Rate (%)": [round((trades.get('won', {}).get('total', 0) / max(trades.get('total', {}).get('total', 1), 1)) * 100, 2)]
}

st.subheader("📊 Strategy Performance Metrics")
st.dataframe(pd.DataFrame(metrics))

# -----------------------------
# Interactive Candlestick Chart
# -----------------------------
st.subheader("📉 Price Chart (Plotly)")
data_reset = data.reset_index()
fig = go.Figure(data=[go.Candlestick(x=data_reset['Date'],
                                     open=data_reset['Open'],
                                     high=data_reset['High'],
                                     low=data_reset['Low'],
                                     close=data_reset['Close'])])
fig.update_layout(title=f"{ticker} Price Chart",
                  xaxis_title="Date",
                  yaxis_title="Price",
                  template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.success("✅ Strategy run complete!")
