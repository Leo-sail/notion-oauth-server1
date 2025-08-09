# api/callback.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
import base64
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        处理Notion OAuth回调
        """
        # 解析URL参数
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # 获取授权码
        code = query_params.get('code', [None])[0]
        state = query_params.get('state', [None])[0]
        error = query_params.get('error', [None])[0]
        
        if error:
            self.send_error_response(f"授权失败: {error}")
            return
        
        if not code:
            self.send_error_response("未收到授权码")
            return
        
        # 交换访问令牌
        token_result = self.exchange_token(code)
        
        if 'error' in token_result:
            self.send_error_response(token_result['error'])
            return
        
        # 返回成功页面
        self.send_success_response(token_result)
    
    def exchange_token(self, code):
        """
        使用授权码交换访问令牌
        """
        client_id = os.environ.get('NOTION_CLIENT_ID')
        client_secret = os.environ.get('NOTION_CLIENT_SECRET')
        redirect_uri = os.environ.get('REDIRECT_URI', 'https://your-app.vercel.app/api/callback')
        
        if not client_id or not client_secret:
            return {'error': '缺少必要的环境变量'}
        
        # 准备请求数据
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        # 准备Basic认证
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
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
                    'error': f'令牌交换失败: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {'error': f'请求异常: {str(e)}'}
    
    def send_success_response(self, token_data):
        """
        发送成功响应
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>授权成功</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .success {{ color: green; }}
                .token {{ background: #f5f5f5; padding: 10px; border-radius: 5px; word-break: break-all; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">✅ Notion授权成功！</h1>
                <p>工作区: {token_data.get('workspace_name', 'Unknown')}</p>
                <p>请复制以下访问令牌到Coze插件中使用：</p>
                <div class="token">
                    <strong>Access Token:</strong><br>
                    {token_data.get('access_token', '')}
                </div>
                <p><small>注意：请妥善保管此令牌，不要泄露给他人。</small></p>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def send_error_response(self, error_message):
        """
        发送错误响应
        """
        html_content = f"""
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
                <p>错误信息: {error_message}</p>
                <p><a href="/api/auth">重新授权</a></p>
            </div>
        </body>
        </html>
        """
        
        self.send_response(400)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))