from itertools import chain

import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

from XQuant import Config, DataAPI, shift_trade_date, format_date
import talib
import numpy as np
import mplfinance as mpf
from cycler import cycler


def Candle():
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : Candle Plot")

    code_full = Config.stock_table["symbol"].values

    col1, col2 = st.columns(2)

    st.session_state.symbol = col1.selectbox("选择股票代码", options=code_full, index=0)
    st.session_state.begin = col1.date_input("起始日期", value=format_date("20200101"))

    st.session_state.freq = col2.selectbox("选择数据频率", options=("日线",))
    st.session_state.end = col2.date_input("截止日期", value=format_date("20210101"))

    if st.session_state.freq == "日线":
        st.session_state.table_name = "gmData_history_adj"
    elif st.session_state.freq == "分钟线":
        st.session_state.table_name = "gmData_history_1m"

    ma_period = st.text_input(
        "均线周期(英文逗号隔开)",
        value="10,20,30",
        key="ma_period_input",
    )
    st.session_state.ma_period = list(map(int, ma_period.split(",")))
    st.session_state.shift = max(chain(st.session_state.ma_period, [26]))

    st.divider()

    if st.button("绘制蜡烛图", key="candle_plot_button"):
        date_column = Config.datatables[st.session_state.table_name]["date_column"]
        df = DataAPI.get_data(
            name=st.session_state.table_name,
            begin=shift_trade_date(st.session_state.begin, -st.session_state.shift),
            end=st.session_state.end,
            ticker=st.session_state.symbol,
        )
        df.index = pd.to_datetime(df[date_column])
        df = df.sort_index()
        ma_name = []
        for i in st.session_state.ma_period:
            tmp = "sma" + str(i)
            ma_name.append(tmp)
            df[tmp] = talib.SMA(df["close"], timeperiod=i)
        df["dif"], df["dea"], df["bar"] = talib.MACD(
            df["close"].values, fastperiod=12, slowperiod=26, signalperiod=9
        )
        df["k"], df["d"] = talib.STOCH(
            df["high"].values,
            df["low"].values,
            df["close"].values,
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )
        df["j"] = 3 * df["k"] - 2 * df["d"]

        df = df.loc[st.session_state.begin :, :]

        my_color = mpf.make_marketcolors(
            up="red", down="green", edge="i", wick="i", volume="in", inherit=True
        )

        my_style = mpf.make_mpf_style(
            gridaxis="both", gridstyle="-.", y_on_right=False, marketcolors=my_color
        )

        custom_cycler = cycler(
            color=["dodgerblue", "deeppink", "navy", "red", "green", "purple", "black"]
        )

        fig = mpf.figure(style=my_style, figsize=(12, 8))
        left, width = 0.05, 0.9
        ax1 = fig.add_axes([left, 0.6, width, 0.35])  # left, bottom, width, height
        ax2 = fig.add_axes([left, 0.4, width, 0.2], sharex=ax1)
        ax3 = fig.add_axes([left, 0.2, width, 0.2], sharex=ax1)
        ax4 = fig.add_axes([left, 0.05, width, 0.15], sharex=ax1)

        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)
        ax1.set_prop_cycle(custom_cycler)
        ax3.set_prop_cycle(custom_cycler)
        ax4.set_prop_cycle(custom_cycler)

        ap = []
        bar_r = np.where(df["bar"] > 0, df["bar"], 0)
        bar_g = np.where(df["bar"] <= 0, df["bar"], 0)
        ap.append(mpf.make_addplot(bar_r, type="bar", color="red", ax=ax3, width=0.6))
        ap.append(mpf.make_addplot(bar_g, type="bar", color="green", ax=ax3, width=0.6))

        for i in ma_name:
            ax1.plot(df[i], label=i.upper())
        ax1.legend(loc="upper left")

        signal = df["dea"]
        macd = df["dif"]
        for i in ["dif", "dea"]:
            ax3.plot(df[i], label=i.upper() if i == "dif" else i.upper() + "(Signal)")
        ax3.fill_between(
            x=signal.index,
            y1=macd,
            y2=signal,
            where=signal < macd,
            color="#93c47d",
            interpolate=True,
        )
        ax3.fill_between(
            x=signal.index,
            y1=macd,
            y2=signal,
            where=signal > macd,
            color="#e06666",
            interpolate=True,
        )
        ax3.legend()

        for i in ["k", "d", "j"]:
            ax4.plot(df[i], label=i.upper())
        ax4.legend()

        mpf.plot(
            df,
            type="candle",
            style=my_style,
            ax=ax1,
            volume=ax2,
            show_nontrading=True,
            addplot=ap,
            ylabel="Price(RMB\u00A5)",
            update_width_config=dict(
                line_width=1.2, candle_width=0.6, candle_linewidth=1.5, volume_width=0.6
            ),
            tight_layout=True,
        )
        ax1.set_title(st.session_state.symbol, fontdict={"size": 20})
        ax2.set_ylabel(r"Volume $1\times 10^6$", fontdict={"size": 10}, labelpad=0)
        ax3.set_ylabel("MACD", fontdict={"size": 10})
        ax4.set_ylabel("KDJ", fontdict={"size": 10})
        ax4.set_xlabel("Date", fontdict={"size": 15})

        st.pyplot(fig=fig)


Candle()
