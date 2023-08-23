from XQuant import BufferManager, capture_prints
import streamlit as st

def Cache():
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : Cache")

    st.write(f"#### 缓存路径为: {BufferManager.root_folder / 'BackTestCache'}")

    col1, col2, col3 = st.columns(3)

    if col1.button("显示系统缓存", key="print_cache_button", use_container_width=True):
        # @capture_prints
        # def cache_info():
        #     return BufferManager.display_file_tree()
        # res, output = cache_info()

        st.write(BufferManager._build_file_tree(BufferManager.root_folder / "BackTestCache"))

Cache()