import pandas as pd
import streamlit as st
from XQuant import IMPLEMENTED, Formatter, Config, DataAPI


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def RawDataVisual():
    st.title("📈 :blue[XQuant] :red[Visual] : Raw Data")

    with st.expander("XQuant原生数据"):
        data_df = pd.DataFrame({"表名": Config.datatables.keys()})

        st.data_editor(
            data_df,
            column_config={
                "表名": st.column_config.TextColumn(
                    "表名",
                    help="XQuant 内置数据表🎈",
                    default="st.",
                    max_chars=50,
                    validate="^st\.[a-z_]+$",
                )
            },
            hide_index=False,
        )

    date_col, name_col = st.columns(2)
    with name_col:
        data_name = st.selectbox("原生数据", Config.datatables.keys())
        show_all = st.checkbox("展示所有数据", key="show_all_check", value=False)
    with date_col:
        begin = st.date_input("起始日期", value=Formatter.date("20200101"))
        end = st.date_input("截止日期", value=Formatter.date("20210101"))

    if st.button("获取数据", key="get_raw_button"):
        with st.spinner("请等待"):
            df = DataAPI.get_data(name=data_name, begin=begin, end=end)
        if show_all:
            st.dataframe(df)
        else:
            st.dataframe(df.head())


RawDataVisual()
