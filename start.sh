#!/bin/bash

# BeeAiRating 启动脚本
echo "🚀 启动 BeeAiRating AI评分系统..."

# 进入后端目录
cd "$(dirname "$0")/back end"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3"
    exit 1
fi

# 检查依赖是否安装
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 未找到 requirements.txt"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到 .env 文件，正在从模板创建..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ 已创建 .env 文件，请编辑配置您的 API 密钥"
    fi
fi

# 启动应用
echo "📁 当前目录: $(pwd)"
echo "🐍 使用 Python: $(which python3)"
echo "🌐 启动 Flask 应用..."

# 启动应用
python3 app.py 