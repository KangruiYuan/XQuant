import re
import sys
from Mold import initialize, code_editor
import streamlit as st
from pathlib import Path

functions_path = Path(__file__).parents[1] / "Temp" / "web_functions"
if not functions_path.exists():
    functions_path.mkdir(exist_ok=True, parents=True)
sys.path.append(str(functions_path))

initialize()
content = code_editor()

if st.button("执行自定义代码", key="exec_code_button") and content:
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
