import pandas as pd
import streamlit as st
from XQuant import IMPLEMENTED, BARRA, Formatter

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def BarraFactor():
    st.title("📈 :blue[XQuant] :red[Visual] : Barra")

    with st.expander("原生数据及Barra因子说明"):
        st.json(IMPLEMENTED.raw)
        st.json(IMPLEMENTED.factor)

    date_col, name_col = st.columns(2)
    with name_col:
        raw_name = st.selectbox("原生数据", IMPLEMENTED.raw.keys())
        factor_name = st.selectbox("BARRA因子", IMPLEMENTED.factor.keys())
        bench_code = st.selectbox("研究标的", ("000852", "000905", "000300"), index=0)
    with date_col:
        begin = st.date_input("起始日期", value=Formatter.date("20200101"))
        end = st.date_input("截止日期", value=Formatter.date("20210101"))

    st.divider()

    barra = BARRA(begin=begin, end=end)

    factor_col, raw_col = st.columns(2)

    with factor_col:
        df = pd.DataFrame()
        if st.button("获取Barra因子数据", key="get_barra_button"):
            with st.spinner("请等待"):
                df = getattr(barra, IMPLEMENTED.factor[factor_name])
        if len(df) > 0:
            st.dataframe(df.head())
        csv = convert_df(df)
        st.download_button(
            label="以CSV方式下载表格",
            data=csv,
            file_name=f'{IMPLEMENTED.factor[factor_name]}.csv',
            mime='text/csv',
        )

    with raw_col:
        df = pd.DataFrame()
        if st.button("获取原生数据", key="get_raw_button"):
            with st.spinner("请等待"):
                barra.bench_code = bench_code
                df = getattr(barra, IMPLEMENTED.raw[raw_name])
        if len(df) > 0:
            st.dataframe(df.head())
        csv = convert_df(df)
        st.download_button(
            label="以CSV方式下载表格",
            data=csv,
            file_name=f'{IMPLEMENTED.raw[raw_name]}.csv',
            mime='text/csv',
        )

BarraFactor()