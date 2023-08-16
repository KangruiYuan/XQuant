

def FactorBackTest():
    import re
    import sys
    from Mold import code_editor
    import streamlit as st
    from pathlib import Path
    global content

    st.title("📈 :blue[XQuant] :red[Visual] : Backtest Platform")

    functions_path = Path(__file__).parents[1] / "Temp" / "web_functions"
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