#!/usr/bin/env python3
"""
BeeAiRating 启动脚本
解决路径中的空格问题
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 启动 BeeAiRating AI评分系统...")
    
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    backend_dir = script_dir / "back end"
    
    print(f"📁 项目目录: {script_dir}")
    print(f"📁 后端目录: {backend_dir}")
    
    # 检查后端目录是否存在
    if not backend_dir.exists():
        print(f"❌ 错误: 找不到后端目录 {backend_dir}")
        return 1
    
    # 检查app.py是否存在
    app_file = backend_dir / "app.py"
    if not app_file.exists():
        print(f"❌ 错误: 找不到 app.py 文件 {app_file}")
        return 1
    
    # 切换到后端目录
    os.chdir(backend_dir)
    print(f"✅ 已切换到目录: {os.getcwd()}")
    
    # 检查Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"🐍 Python版本: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python检查失败: {e}")
        return 1
    
    # 启动Flask应用
    print("🌐 启动Flask应用...")
    print("=" * 50)
    
    try:
        # 使用subprocess启动，这样可以看到实时输出
        process = subprocess.Popen([sys.executable, "app.py"])
        
        print("✅ 应用已启动!")
        print("🌐 访问地址:")
        print("   • 增强评测: http://127.0.0.1:8080/enhanced-rating")
        print("   • 基础评测: http://127.0.0.1:8080/website-rating")
        print("   • 主页: http://127.0.0.1:8080/")
        print()
        print("按 Ctrl+C 停止应用")
        
        # 等待进程结束
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 正在停止应用...")
        if process:
            process.terminate()
        print("✅ 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 