from typing import Literal

import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, THEMES


def initialize(
    app_title: str = "XQuant Visual",
    page_title: str = "📈 :blue[XQuant] :red[Visual]",
    layout: Literal["centered", "wide"] = "wide",
    **kwargs
):
    st.set_page_config(
        page_title=app_title,
        page_icon=kwargs.get("page_icon", "📈"),
        layout=layout,
        initial_sidebar_state=kwargs.get("initial_sidebar_state", "auto"),
        menu_items={
            "About": "https://github.com/KangruiYuan/XQuant",
            "Report a bug": "https://github.com/KangruiYuan/XQuant/issues",
        },
    )

    st.title(page_title)
    st.divider()


def code_editor(**kwargs):
    code_col, para_col = st.columns([3, 1])
    para_col.subheader("Parameters")

    with code_col:
        function_code = ["def function(x, y):", "    return x * y"]
        function_code = "\n".join(function_code)
        content = st_ace(
            value=function_code,
            placeholder=para_col.text_input("控件提示", value="请输入处理因子的代码"),
            language=para_col.selectbox("编程语言", options=["python"], index=0),
            theme=para_col.selectbox("界面风格", options=THEMES, index=35),
            keybinding=para_col.selectbox("键入模式", options=KEYBINDINGS, index=3),
            font_size=para_col.slider("字体大小", 5, 24, 14),
            tab_size=para_col.slider("Tab大小", 1, 8, 4),
            show_gutter=para_col.checkbox("显示代码行号", value=True),
            show_print_margin=para_col.checkbox("显示打印边缘", value=False),
            wrap=para_col.checkbox("允许折叠", value=False),
            auto_update=para_col.checkbox("自动更新显示", value=True),
            readonly=para_col.checkbox("只读模式", value=False),
            min_lines=45,
            key="ace",
        )

        return content
