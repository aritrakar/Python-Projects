import pytz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import vectorbt as vbt

# Set variables for the analysis

symbols = [
    "META",
    "AMZN",
    "AAPL",
    "NFLX",
    "GOOG",
]

start_date = datetime(2018, 1, 1, tzinfo=pytz.utc)
end_date = datetime(2021, 1, 1, tzinfo=pytz.utc)

traded_count = 3
window_len = timedelta(days=12 * 21)

seed = 42
window_count = 400
exit_types = ["SL", "TS", "TP"]
stops = np.arange(0.01, 1 + 0.01, 0.01)


# Download historical data and concatenate into a single DataFrame

print("Downloading data...")

yfdata = vbt.YFData.download(symbols, start=start_date, end=end_date)
ohlcv = yfdata.concat()

# print("Downloaded data:" + str(ohlcv))

split_ohlcv = {}

for k, v in ohlcv.items():
    split_df, split_indexes = v.vbt.range_split(
        range_len=window_len.days, n=window_count
    )
    split_ohlcv[k] = split_df
ohlcv = split_ohlcv


# Build the momentum strategy
'''
Calculate the momentum of each stock symbol based on the
percentage change of their closing prices. Then sort these
values within each split and select the top 3 stocks with
the highest momentum. Finally, extract the prices of the
selected stocks using their indices and store them in
selected_open, selected_high, selected_low, and selected_close, respectively.
'''

momentum = ohlcv["Close"].pct_change().mean()

sorted_momentum = (
    momentum
    .groupby(
        "split_idx",
        group_keys=False,
        sort=False
    )
    .apply(
        pd.Series.sort_values
    )
    .groupby("split_idx")
    .head(traded_count)
)

selected_open = ohlcv["Open"][sorted_momentum.index]
selected_high = ohlcv["High"][sorted_momentum.index]
selected_low = ohlcv["Low"][sorted_momentum.index]
selected_close = ohlcv["Close"][sorted_momentum.index]

# Test the order types

entries = pd.DataFrame.vbt.signals.empty_like(selected_open)
entries.iloc[0, :] = True

sl_exits = vbt.OHLCSTX.run(
    entries,
    selected_open,
    selected_high,
    selected_low,
    selected_close,
    sl_stop=list(stops),
    stop_type=None,
    stop_price=None,
).exits

ts_exits = vbt.OHLCSTX.run(
    entries,
    selected_open,
    selected_high,
    selected_low,
    selected_close,
    sl_stop=list(stops),
    sl_trail=True,
    stop_type=None,
    stop_price=None,
).exits

tp_exits = vbt.OHLCSTX.run(
    entries,
    selected_open,
    selected_high,
    selected_low,
    selected_close,
    tp_stop=list(stops),
    stop_type=None,
    stop_price=None,
).exits

sl_exits.vbt.rename_levels({"ohlcstx_sl_stop": "stop_value"}, inplace=True)
ts_exits.vbt.rename_levels({"ohlcstx_sl_stop": "stop_value"}, inplace=True)
tp_exits.vbt.rename_levels({"ohlcstx_tp_stop": "stop_value"}, inplace=True)
ts_exits.vbt.drop_levels("ohlcstx_sl_trail", inplace=True)

sl_exits.iloc[-1, :] = True
ts_exits.iloc[-1, :] = True
tp_exits.iloc[-1, :] = True

sl_exits = sl_exits.vbt.signals.first(reset_by=entries, allow_gaps=True)
ts_exits = ts_exits.vbt.signals.first(reset_by=entries, allow_gaps=True)
tp_exits = tp_exits.vbt.signals.first(reset_by=entries, allow_gaps=True)

exits = pd.DataFrame.vbt.concat(
    sl_exits,
    ts_exits,
    tp_exits,
    keys=pd.Index(exit_types, name="exit_type"),
)


# Run and analyze the backtest

print("Running backtest...")

portfolio = vbt.Portfolio.from_signals(selected_close, entries, exits)

total_return = portfolio.total_return()

total_return_by_type = total_return.unstack(level="exit_type")[exit_types]

total_return_by_type[exit_types].vbt.histplot(
    xaxis_title="Total return",
    xaxis_tickformat="%",
    yaxis_title="Count",
).show()

print("Total return by exit type:" + str(total_return_by_type))

# total_return_by_type.vbt.boxplot(
#     yaxis_title='Total return',
#     yaxis_tickformat='%'
# )

# total_return_by_type.describe(percentiles=[])
