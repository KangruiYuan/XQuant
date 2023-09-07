import streamlit as st
from XQuant import IMPLEMENTED

def JointQuantFactor():
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : JointQuant")

    with st.expander("聚宽因子说明"):
        st.markdown("因子数据（宽表）")
        st.json(IMPLEMENTED.joint_quant)
        st.markdown("原生数据（宽表）")
        st.json(IMPLEMENTED.raw)

JointQuantFactor()