from streamlit_ace import st_ace, KEYBINDINGS, THEMES
import re
import sys
import streamlit as st
from pathlib import Path

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


def FactorBackTest():
    st.title("📈 :blue[XQuant] :red[Visual] : Backtest Platform")

    functions_path = Path(__file__).parents[2] / "Temp" / "web_functions"
    if not functions_path.exists():
        functions_path.mkdir(exist_ok=True, parents=True)
    sys.path.append(str(functions_path))

    st.subheader("选择模式进行回测")

    # if st.button("输入自定义因子转换代码", key="input_code_button"):
    st.subheader("自定义代码输入区")
    content = code_editor()

    if st.button("执行自定义回测", key="exec_code_button") and content:
        pattern = r"def\s+(\w+)\s*\("
        matches = re.findall(pattern, content)
        if matches:
            function_name = matches[0]
            with st.spinner("执行中"):
                script_path = functions_path / function_name
                script_path = script_path.with_suffix(".py")
                with open(script_path, "w") as script:
                    script.write(content)
                exec(f"from {function_name} import {function_name}")
                user_defined_function = globals()[function_name]
                st.success("自定义代码执行成功")

FactorBackTest()