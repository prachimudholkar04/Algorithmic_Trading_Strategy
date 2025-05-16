# Algorithmic Trading Strategy with Backtrader (SMA Crossover)

# Cell 1: Install required packages
#!pip install backtrader yfinance matplotlib --quiet

# Cell 2: Imports
import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

# Cell 3: Download historical data
symbol = 'AAPL'
data = yf.download(symbol, start='2020-01-01', end='2025-12-31', auto_adjust=False)
data.columns = [col if isinstance(col, str) else col[0] for col in data.columns]
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data.to_csv('data.csv')

# Cell 4: Backtrader Data Feed
class PandasData(bt.feeds.PandasData):
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )

# Cell 5: Define Strategy
class SmaCross(bt.Strategy):
    params = dict(
        pfast=10,  # period for the fast MA
        pslow=30   # period for the slow MA
    )

    def __init__(self):
        self.sma1 = bt.ind.SMA(period=self.p.pfast)
        self.sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()

# Cell 6: Run Backtest
cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000)
cerebro.addstrategy(SmaCross)
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
results = cerebro.run()
strat = results[0]

# Cell 7: Print Results
print("Final Portfolio Value: $%.2f" % cerebro.broker.getvalue())
print("Sharpe Ratio:", strat.analyzers.sharpe.get_analysis())
print("Drawdown:", strat.analyzers.drawdown.get_analysis())
print("Trade Stats:", strat.analyzers.trades.get_analysis())

# Cell 8: Clean Plot
plt.figure(figsize=(20, 10))
cerebro.plot(style='candlestick', volume=False, iplot=False)[0][0].suptitle("SMA Crossover Strategy - AAPL", fontsize=16)
plt.tight_layout()
plt.show()
