from pathlib import Path
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="运行网页端量化的附属指令")
    parser.add_argument("-a", "--app", type=str, default="Home.py", help="模型路径")
    parser.add_argument("-p", "--port", type=int, default=9999)
    args = parser.parse_args()
    app_path = Path(__file__).parent / "Contents" / args.app
    os.system(f"python -m streamlit run {app_path} --server.port {args.port}")