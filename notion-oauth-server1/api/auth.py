# api/auth.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlencode
import json
import secrets
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        处理授权请求，重定向到Notion OAuth
        """
        # 生成state参数
        state = secrets.token_urlsafe(32)
        
        # 从环境变量获取配置
        client_id = os.environ.get('NOTION_CLIENT_ID')
        redirect_uri = os.environ.get('REDIRECT_URI', 'https://your-app.vercel.app/api/callback')
        
        if not client_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': '缺少NOTION_CLIENT_ID环境变量'
            }).encode())
            return
        
        # 构建Notion授权URL
        auth_params = {
            'client_id': client_id,
            'response_type': 'code',
            'owner': 'user',
            'redirect_uri': redirect_uri,
            'state': state
        }
        
        auth_url = f"https://api.notion.com/v1/oauth/authorize?{urlencode(auth_params)}"
        
        # 重定向到Notion授权页面
        self.send_response(302)
        self.send_header('Location', auth_url)
        self.end_headers()