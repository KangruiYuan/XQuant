from XQuant import BufferManager, capture_prints
import streamlit as st


def Cache():
    st.set_page_config(layout="wide")
    st.title("📈 :blue[XQuant] :red[Visual] : Cache")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("显示回测缓存", key="print_cache_button", use_container_width=True):
            # @capture_prints
            # def cache_info():
            #     return BufferManager.display_file_tree()
            # res, output = cache_info()
            st.write(f"#### 缓存路径为: {BufferManager.root_folder / 'BackTestCache'}")
            st.write(
                BufferManager._build_file_tree(
                    BufferManager.root_folder / "BackTestCache"
                )
            )

    with col2:
        if st.button(
            "自定义回测函数缓存", key="print_cache_func_button", use_container_width=True
        ):
            st.write(f"#### 缓存路径为: {BufferManager.root_folder / 'web_functions'}")
            st.write(
                BufferManager._build_file_tree(
                    BufferManager.root_folder / "web_functions"
                )
            )


Cache()
