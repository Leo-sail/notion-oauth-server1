#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试服务器
用于在本地开发和测试OAuth授权流程
"""

from flask import Flask, request, redirect, jsonify, session
import requests
import base64
import secrets
import os
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 配置信息（在实际使用时应该从环境变量获取）
NOTION_CLIENT_ID = os.environ.get('NOTION_CLIENT_ID', 'your_client_id_here')
NOTION_CLIENT_SECRET = os.environ.get('NOTION_CLIENT_SECRET', 'your_client_secret_here')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:5001/oauth/callback')

@app.route('/')
def index():
    """
    首页，显示授权链接
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Notion OAuth 测试服务器</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .btn {{ 
                background: #0070f3; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block;
                margin: 10px 0;
            }}
            .config {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Notion OAuth 测试服务器</h1>
            <p>这是一个本地测试服务器，用于测试Notion OAuth授权流程。</p>
            
            <div class="config">
                <h3>当前配置：</h3>
                <p><strong>Client ID:</strong> {NOTION_CLIENT_ID}</p>
                <p><strong>Redirect URI:</strong> {REDIRECT_URI}</p>
                <p><strong>状态:</strong> {'✅ 已配置' if NOTION_CLIENT_ID != 'your_client_id_here' else '❌ 需要配置'}</p>
            </div>
            
            <a href="/auth/notion" class="btn">🚀 开始Notion授权</a>
            
            <h3>使用说明：</h3>
            <ol>
                <li>确保已在Notion中创建集成并获取Client ID和Secret</li>
                <li>设置环境变量或修改代码中的配置</li>
                <li>点击上方按钮开始授权流程</li>
                <li>完成授权后获取访问令牌</li>
            </ol>
        </div>
    </body>
    </html>
    '''

@app.route('/auth/notion')
def start_notion_auth():
    """
    启动Notion OAuth授权流程
    """
    if NOTION_CLIENT_ID == 'your_client_id_here':
        return jsonify({
            'error': '请先配置NOTION_CLIENT_ID环境变量',
            'help': '设置环境变量: export NOTION_CLIENT_ID=your_actual_client_id'
        }), 400
    
    # 生成state参数用于安全验证
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # 构建授权URL
    auth_params = {
        'client_id': NOTION_CLIENT_ID,
        'response_type': 'code',
        'owner': 'user',
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    
    auth_url = f"https://api.notion.com/v1/oauth/authorize?{urlencode(auth_params)}"
    
    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    """
    处理Notion OAuth回调
    """
    # 验证state参数
    if request.args.get('state') != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    # 获取授权码
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>授权失败</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ 授权失败</h1>
                <p>错误信息: {error}</p>
                <p><a href="/">返回首页</a></p>
            </div>
        </body>
        </html>
        '''
    
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400
    
    # 交换访问令牌
    token_data = exchange_code_for_token(code)
    
    if 'error' in token_data:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>令牌交换失败</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ 令牌交换失败</h1>
                <p>错误信息: {token_data['error']}</p>
                <p>详细信息: {token_data.get('details', 'N/A')}</p>
                <p><a href="/">返回首页</a></p>
            </div>
        </body>
        </html>
        '''
    
    # 返回成功页面
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>授权成功</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .success {{ color: green; }}
            .token {{ 
                background: #f5f5f5; 
                padding: 15px; 
                border-radius: 5px; 
                word-break: break-all;
                margin: 15px 0;
                border: 1px solid #ddd;
            }}
            .copy-btn {{
                background: #0070f3;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                margin-left: 10px;
            }}
        </style>
        <script>
            function copyToken() {{
                const tokenText = document.getElementById('token-text').textContent;
                navigator.clipboard.writeText(tokenText).then(function() {{
                    alert('令牌已复制到剪贴板！');
                }});
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ Notion授权成功！</h1>
            <p><strong>工作区:</strong> {token_data.get('workspace_name', 'Unknown')}</p>
            <p><strong>所有者:</strong> {token_data.get('owner', {}).get('user', {}).get('name', 'Unknown')}</p>
            
            <h3>访问令牌：</h3>
            <div class="token">
                <span id="token-text">{token_data.get('access_token', '')}</span>
                <button class="copy-btn" onclick="copyToken()">复制</button>
            </div>
            
            <h3>使用说明：</h3>
            <ol>
                <li>复制上方的访问令牌</li>
                <li>在Coze插件的notion_token参数中使用该令牌</li>
                <li>现在可以使用Notion API进行数据操作了</li>
            </ol>
            
            <p><small>⚠️ 注意：请妥善保管此令牌，不要泄露给他人。</small></p>
            <p><a href="/">返回首页</a></p>
        </div>
    </body>
    </html>
    '''

def exchange_code_for_token(code):
    """
    使用授权码换取访问令牌
    """
    if NOTION_CLIENT_SECRET == 'your_client_secret_here':
        return {'error': '请先配置NOTION_CLIENT_SECRET环境变量'}
    
    # 准备请求数据
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    # 准备Basic认证头
    auth_string = f"{NOTION_CLIENT_ID}:{NOTION_CLIENT_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    # 发送令牌交换请求
    try:
        response = requests.post(
            'https://api.notion.com/v1/oauth/token',
            json=token_data,
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': f'令牌交换失败 (HTTP {response.status_code})',
                'details': response.text
            }
    except Exception as e:
        return {
            'error': f'请求异常: {str(e)}'
        }

if __name__ == '__main__':
    print("🚀 启动Notion OAuth测试服务器...")
    print(f"📍 服务器地址: http://localhost:5001")
    print(f"🔧 Client ID: {NOTION_CLIENT_ID}")
    print(f"🔄 Redirect URI: {REDIRECT_URI}")
    print("\n💡 使用说明:")
    print("1. 确保已设置环境变量 NOTION_CLIENT_ID 和 NOTION_CLIENT_SECRET")
    print("2. 在浏览器中访问 http://localhost:5001")
    print("3. 点击授权按钮开始测试")
    print("\n📝 注意: 如果端口5001也被占用，可以修改代码中的端口号")
    print("🔧 或者设置环境变量: export REDIRECT_URI=http://localhost:PORT/oauth/callback")
    print("\n⚠️  如需停止服务器，请按 Ctrl+C")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)