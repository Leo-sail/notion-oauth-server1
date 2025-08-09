#!/bin/bash

# Notion OAuth 服务器启动脚本

echo "🚀 Notion OAuth 服务器启动脚本"
echo "================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip3，请先安装 pip"
    exit 1
fi

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到 .env 文件"
    echo "📝 请复制 .env.example 为 .env 并配置相关参数"
    echo "💡 或者直接设置环境变量:"
    echo "   export NOTION_CLIENT_ID=your_client_id"
    echo "   export NOTION_CLIENT_SECRET=your_client_secret"
    echo ""
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖..."
pip install flask requests

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接或Python环境"
    exit 1
fi

# 加载环境变量（如果.env文件存在）
if [ -f ".env" ]; then
    echo "🔧 加载环境变量..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# 检查必要的环境变量
if [ -z "$NOTION_CLIENT_ID" ] || [ "$NOTION_CLIENT_ID" = "your_notion_client_id_here" ]; then
    echo "⚠️  警告: NOTION_CLIENT_ID 未设置或使用默认值"
fi

if [ -z "$NOTION_CLIENT_SECRET" ] || [ "$NOTION_CLIENT_SECRET" = "your_notion_client_secret_here" ]; then
    echo "⚠️  警告: NOTION_CLIENT_SECRET 未设置或使用默认值"
fi

echo ""
echo "🌟 启动服务器..."
echo "📍 访问地址: http://localhost:5000"
echo "🛑 停止服务器: 按 Ctrl+C"
echo "================================"
echo ""

# 启动Flask服务器（在虚拟环境中）
source venv/bin/activate && python local_server.py