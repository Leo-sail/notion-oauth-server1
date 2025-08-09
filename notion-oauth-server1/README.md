# Notion OAuth Server

这是一个用于Coze平台Notion插件的OAuth授权服务器，部署在Vercel上。

## 功能特性

- 🔐 完整的Notion OAuth 2.0授权流程
- 🚀 部署在Vercel的无服务器架构
- 🎨 用户友好的授权界面
- 🔒 安全的令牌交换机制

## 项目结构

```
notion-oauth-server/
├── api/
│   ├── auth.py          # 授权端点
│   └── callback.py      # 回调处理
├── requirements.txt     # Python依赖
├── vercel.json         # Vercel配置
└── README.md           # 项目说明
```

## 部署步骤

### 1. 准备Notion集成

1. 访问 [Notion集成页面](https://www.notion.so/my-integrations)
2. 创建新的公开集成
3. 记录Client ID和Client Secret
4. 配置Redirect URI: `https://your-app.vercel.app/api/callback`

### 2. 部署到Vercel

1. 将代码上传到GitHub仓库
2. 在Vercel中导入GitHub项目
3. 配置环境变量：
   - `NOTION_CLIENT_ID`: 你的Notion Client ID
   - `NOTION_CLIENT_SECRET`: 你的Notion Client Secret
   - `REDIRECT_URI`: `https://your-app.vercel.app/api/callback`
4. 部署项目

### 3. 测试授权流程

1. 访问 `https://your-app.vercel.app/api/auth`
2. 完成Notion授权
3. 获取访问令牌

## 使用方法

### 在Coze插件中使用

1. 用户访问授权链接完成授权
2. 复制返回的access_token
3. 在Coze插件的notion_token参数中使用该令牌

### API端点

- `GET /api/auth` - 启动授权流程
- `GET /api/callback` - 处理授权回调

## 环境变量

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| NOTION_CLIENT_ID | Notion应用的客户端ID | `your_client_id` |
| NOTION_CLIENT_SECRET | Notion应用的客户端密钥 | `your_client_secret` |
| REDIRECT_URI | OAuth回调地址 | `https://your-app.vercel.app/api/callback` |

## 安全注意事项

- 🔒 Client Secret必须保密，只在服务器端使用
- 🛡️ 使用HTTPS确保数据传输安全
- 🔄 定期轮换访问令牌
- 📝 监控访问日志

## 故障排除

### 常见问题

1. **授权失败**
   - 检查Client ID和Secret是否正确
   - 确认Redirect URI配置一致

2. **部署失败**
   - 检查requirements.txt格式
   - 确认vercel.json配置正确

3. **令牌获取失败**
   - 验证环境变量设置
   - 检查Notion API版本兼容性

## 技术栈

- **运行时**: Python 3.9
- **部署平台**: Vercel
- **HTTP库**: requests
- **认证协议**: OAuth 2.0

## 许可证

MIT License