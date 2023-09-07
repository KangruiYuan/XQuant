from time import sleep

from streamlit_ace import st_ace, KEYBINDINGS, THEMES
import re
import sys
import streamlit as st
from pathlib import Path
import pandas as pd
from XQuant import Formatter, BARRA, Analyzer, Strategy, BackTestRunner, BackTestOptions, RtnResult
import plotly.express as px

def code_editor(**kwargs):
    code_col, para_col = st.columns([3, 1])
    para_col.subheader("Parameters")

    with code_col:
        # function_code = ["def function(x, y):", "    return x * y"]
        # function_code = "\n".join(function_code)
        function_code_file = Path(__file__).parent / "demo_web_function.txt"
        function_code = open(function_code_file, "r", encoding='utf-8').read()
        st.subheader("自定义代码输入区")
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
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : Backtest Platform")

    st.session_state.functions_path = Path(__file__).parents[2] / "Temp" / "web_functions"
    if not st.session_state.functions_path.exists():
        st.session_state.functions_path.mkdir(exist_ok=True, parents=True)
    sys.path.append(str(st.session_state.functions_path))

    factor_backtest_uploaded = st.file_uploader(
        "## 上传因子数据（宽表格式）", type=["csv"], key="backtest_factor_uploaded"
    )

    if factor_backtest_uploaded is not None:
        # Can be used wherever a "file-like" object is accepted:
        with st.spinner(f"正在读取：{factor_backtest_uploaded.name}"):
            if factor_backtest_uploaded.name.endswith("csv"):
                factor_data = pd.read_csv(factor_backtest_uploaded)
            else:
                st.error(f"File type is not supported!")

            col_names = factor_data.columns
            for col in col_names:
                sample = factor_data[col].dropna().values[0]
                if Formatter.is_date(sample):
                    date_column = col
                    break

            factor_data = factor_data.set_index(date_column)
            factor_data = Formatter.dataframe(factor_data)
            st.dataframe(factor_data.head())
            st.session_state.date_max = factor_data.index.max()
            st.session_state.date_min = factor_data.index.min()
            st.session_state.factor_data = factor_data

    st.subheader("选择模式进行回测")
    back_col, bench_col, func_name_col = st.columns(3)
    backtest_method = back_col.selectbox("回测方法", [s.value for s in Strategy])
    bench_code = bench_col.selectbox("研究标的", ("000852", "000905", "000300"), index=0)
    st.session_state.function_name = func_name_col.text_input("多个函数请指定主函数", "signal_to_weight")

    col1, col2 = st.columns(2)
    opts = BackTestOptions()
    bt = BackTestRunner(
        signals=pd.DataFrame(),
        options=opts
    )
    st.session_state.content = code_editor()

    if col1.button("因子回测", key="cal_backtest_button_in_backtest", use_container_width=True):
        if backtest_method != Strategy.SELF_DEFINED:
            opts = BackTestOptions(
                begin=st.session_state.date_min,
                end=st.session_state.date_max,
                bench_code=bench_code,
                verbose=False,
                method=backtest_method,
                surname=backtest_method
            )
        elif backtest_method == Strategy.SELF_DEFINED and st.session_state.content:
            pattern = r"def\s+(\w+)\s*\("
            matches = re.findall(pattern, st.session_state.content)
            if matches and len(matches) == 1:
                st.session_state.function_name = matches[0]
                st.write(f"自动检测到的主函数为: {st.session_state.function_name}")
            else:
                st.write(f"采用主动输入的主函数: {st.session_state.function_name}")
            with st.spinner("执行中"):
                script_path = st.session_state.functions_path / st.session_state.function_name
                script_path = script_path.with_suffix(".py")
                with open(script_path, "w") as script:
                    script.write(st.session_state.content)
                exec_code = compile(st.session_state.content, 'temp', "exec")
                scope = {}
                exec(exec_code, scope)
                user_defined_function = scope.get(st.session_state.function_name)
                # exec(f"from {st.session_state.function_name} import {st.session_state.function_name}")
                # user_defined_function = eval(st.session_state.function_name)
                opts = BackTestOptions(
                    begin=st.session_state.date_min,
                    end=st.session_state.date_max,
                    bench_code=bench_code,
                    verbose=False,
                    method=backtest_method,
                    surname=backtest_method,
                    function=user_defined_function
                )
        with st.spinner("请等待，计算中..."):
            bt.signals = st.session_state.factor_data
            bt.options = opts
            bt.prepare()
            bt.run()
            st.success(f"结果保存在: {bt.work_folder}")
            fig = bt.plot()
            st.plotly_chart(fig, use_container_width=True)
            if bt.options.method == Strategy.GROUP:
                bench_res = bt.cache[bt.date_range_str]["bench_result"]
                for group in range(bt.options.group_nums):
                    st.divider()
                    res: RtnResult = bt.cache[bt.date_range_str][bt.options.method.value][group]["result"]
                    fields = res._fields
                    st.write(f"### Group {group}")
                    cols = st.columns(len(fields))
                    for i in range(len(fields)):
                        cols[i].metric(
                            label=fields[i],
                            value=round(res[i], 2),
                            delta=round(res[i] - bench_res[i], 2),
                        )
            else:
                res: RtnResult = bt.cache[bt.date_range_str][bt.options.method.value]["result"]
                bench_res = bt.cache[bt.date_range_str]["bench_result"]
                fields = res._fields
                cols = st.columns(len(fields))
                for i in range(len(fields)):
                    cols[i].metric(
                        label=fields[i],
                        value=round(res[i], 2),
                        delta=round(res[i] - bench_res[i], 2),
                    )

    if col2.button("ICIR", key="cal_ICIR_button_in_backtest", use_container_width=True):
        with st.spinner("请等待"):
            if "factor_data" in st.session_state.keys() and len(st.session_state.factor_data > 0):
                returns = BARRA(begin=st.session_state.date_min, end=st.session_state.date_max).returns
                IC, IR = Analyzer.ICIR(st.session_state.factor_data, returns)
                IC = IC.reset_index()
                fig = px.bar(
                    IC,
                    x="index",
                    y="IC",
                    color="IC",
                    orientation='v',
                    labels={"index": "Date"},
                    title=f"IR={float(IR):.2f}",
                    color_continuous_scale="spectral"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"请准备您的因子数据")


FactorBackTest()