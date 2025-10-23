#!/usr/bin/env python3.13
"""
Streamlit 应用启动脚本
"""
import subprocess
import sys
import os

def main():
    # 设置环境
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 启动 Streamlit
    cmd = [
        "python", "-m", "streamlit", "run", 
        "streamlit_app.py",
        "--server.port", "80",
        "--server.address", "0.0.0.0",
        "--server.headless", "false"
    ]
    
    print("🌊 启动海上风电巡检风险评估系统...")
    print(f"📍 访问地址: http://localhost:8501")
    print("🔧 使用 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")

if __name__ == "__main__":
    main()
