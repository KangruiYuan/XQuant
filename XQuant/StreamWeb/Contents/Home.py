import streamlit as st
from pathlib import Path
from PIL import Image
from streamlit_card import card
from streamlit_extras.badges import badge


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

    # logo_path = pic_folder / "ws_logo.png"
    # image = Image.open(logo_path)
    # st.image(image, width=340)

    card(
        title="WESTERN SECURITIES",
        text="西部证券",
        image="https://www.west95582.com/jdw/images/logo3.png",
        url="https://www.west95582.com/jdw/index.html",
        styles={
            "card": {
                "width": "560px",
                "height": "84px",
                "border-radius": "20px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
            }
        },
    )

    st.title("📈 :blue[XQuant] :red[Visual]")

    badge(
        type="github",
        name="KangruiYuan/XQuant",
        url="https://github.com/KangruiYuan/XQuant",
    )

    st.markdown(
        f"""
        该项目由西部证券开发。
        - 项目主页:  [Github pages](https://github.com/KangruiYuan/XQuant)
        - 报告错误: [Issue]("https://github.com/KangruiYuan/XQuant/issues")
        """
    )


Home()
