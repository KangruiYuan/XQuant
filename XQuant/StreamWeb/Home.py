import streamlit as st
from pathlib import Path
from PIL import Image


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

def Home():
    pic_folder = Path(__file__).parent / "pics"
    logo_path = pic_folder / "ws_logo.png"

    image = Image.open(logo_path)
    st.image(image, width=340)

    st.title("📈 :blue[XQuant] :red[Visual]")

    st.markdown(
        f"""
        该项目由西部证券开发。
        - 项目主页:  [Github pages](https://github.com/KangruiYuan/XQuant)
        - 报告错误: [Issue]("https://github.com/KangruiYuan/XQuant/issues")
        """
    )

Home()