import streamlit as st
from streamlit.components.v1 import html
from pathlib import Path


def HelperPage():
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : 帮助文档")

    docs_folder = Path(__file__).parents[3] / "Docs" / "DemoHtml"
    html_help_docs = list(docs_folder.glob("*.html"))

    docs_mapper = {k.stem: k for k in html_help_docs}

    docs_name = st.selectbox("帮助文档", docs_mapper.keys(), index=1)

    st.divider()
    cont = open(docs_mapper[docs_name], "r", encoding="utf-8").read()
    html(cont, scrolling=True, height=400)
    st.divider()


HelperPage()
