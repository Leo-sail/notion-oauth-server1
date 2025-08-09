from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    """处理根路径访问的处理器"""
    
    def do_GET(self):
        """处理GET请求，返回欢迎页面"""
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 创建HTML响应内容
            html_content = """
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Notion OAuth 服务器</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 40px 20px;
                        background-color: #f8f9fa;
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #2d3748;
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .status {
                        background: #e6fffa;
                        border: 1px solid #38b2ac;
                        color: #234e52;
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 30px;
                        text-align: center;
                    }
                    .endpoints {
                        background: #f7fafc;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                    }
                    .endpoint {
                        margin: 10px 0;
                        padding: 10px;
                        background: white;
                        border-radius: 6px;
                        border-left: 4px solid #4299e1;
                    }
                    .endpoint-url {
                        font-family: 'Monaco', 'Menlo', monospace;
                        color: #2b6cb0;
                        font-weight: bold;
                    }
                    .description {
                        color: #4a5568;
                        font-size: 14px;
                        margin-top: 5px;
                    }
                    .footer {
                        text-align: center;
                        color: #718096;
                        font-size: 14px;
                        margin-top: 30px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔗 Notion OAuth 服务器</h1>
                    
                    <div class="status">
                        ✅ 服务器运行正常
                    </div>
                    
                    <div class="endpoints">
                        <h3>可用的API端点：</h3>
                        
                        <div class="endpoint">
                            <div class="endpoint-url">/api/auth</div>
                            <div class="description">启动Notion OAuth授权流程</div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-url">/api/callback</div>
                            <div class="description">处理Notion OAuth回调</div>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>这是一个用于Notion集成的OAuth授权服务器</p>
                        <p>部署在 Vercel 平台</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # 发送HTML内容
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            # 错误处理
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "error": "Internal Server Error",
                "message": str(e)
            }
            
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理OPTIONS请求，用于CORS预检"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()