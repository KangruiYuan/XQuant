import pandas as pd
import streamlit as st
from XQuant import IMPLEMENTED, BARRA, Formatter, Analyzer
from collections import ChainMap
import plotly.express as px

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def BarraFactor():
    st.title("📈 :blue[XQuant] :red[Visual] : Barra")

    with st.expander("Barra因子说明"):
        st.markdown("原生数据（宽表）")
        st.json(IMPLEMENTED.raw)
        st.markdown("因子数据（宽表）")
        st.json(IMPLEMENTED.factor)

    all_data = ChainMap(IMPLEMENTED.raw, IMPLEMENTED.factor)

    date_col, name_col = st.columns(2)
    with name_col:
        data_name = st.selectbox("数据名", all_data.keys())
        bench_code = st.selectbox("研究标的", ("000852", "000905", "000300"), index=0)
    with date_col:
        begin = st.date_input("起始日期", value=Formatter.date("20200101"))
        end = st.date_input("截止日期", value=Formatter.date("20210101"))

    st.divider()

    barra = BARRA(begin=begin, end=end, bench_code=bench_code)

    col1, col2, col3, col4 = st.columns(4)

    st.session_state.barra_factor_df = pd.DataFrame()

    if col1.button("获取/显示数据", key="get_barra_button", use_container_width=True):
        with st.spinner("请等待"):
            st.session_state.barra_factor_df = getattr(barra, all_data[data_name])
        if len(st.session_state.barra_factor_df) > 0:
            st.dataframe(st.session_state.barra_factor_df.head())

    with col2:
        csv = convert_df(st.session_state.barra_factor_df)
        st.download_button(
            label="以CSV格式下载数据",
            data=csv,
            file_name=f"{all_data[data_name]}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if col3.button("ICIR", key="cal_ICIR_button", use_container_width=True):
        with st.spinner("请等待"):
            if len(st.session_state.barra_factor_df) == 0:
                st.session_state.barra_factor_df = getattr(barra, all_data[data_name])
            if len(st.session_state.barra_factor_df > 0) and data_name != "bench":
                returns = barra.returns
                IC, IR = Analyzer.ICIR(st.session_state.barra_factor_df, returns)
                IC = IC.reset_index()
                fig = px.bar(
                    IC,
                    x="index",
                    y="IC",
                    color="IC",
                    orientation='v',
                    labels={"index": "Date"},
                    title=f"IR={float(IR):.2f}"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"因子数据长度为{len(st.session_state.barra_factor_df)}或者您选择的数据为指数基准数据")

    if col4.button("因子回测", key="cal_backtest_button", use_container_width=True):
        pass

BarraFactor()
