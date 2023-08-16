
from FactorAnalysisPage import FactorBackTest
from Mold import intro
import streamlit as st

st.set_page_config(
        page_title="XQuant Visual",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "About": "https://github.com/KangruiYuan/XQuant",
            "Report a bug": "https://github.com/KangruiYuan/XQuant/issues",
        },
    )

page_names_to_funcs = {
    "主页": intro,
    "回测": FactorBackTest,
}

page_name = st.sidebar.selectbox("选择页面", page_names_to_funcs.keys(), index=0)
page_names_to_funcs[page_name]()