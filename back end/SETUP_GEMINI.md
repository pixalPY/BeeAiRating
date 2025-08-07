# Google Gemini API 设置指南

## 🔒 安全警告

**重要：** 永远不要在代码中直接硬编码 API key！

## 📋 设置步骤

### 1. 获取新的 API Key
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的 API key
3. 设置使用限制和配额

### 2. 配置环境变量
1. 复制 `env.example` 到 `.env`：
   ```bash
   cp env.example .env
   ```

2. 编辑 `.env` 文件，添加你的 API key：
   ```env
   GOOGLE_GEMINI_API_KEY=your-new-api-key-here
   GEMINI_MODEL=gemini-1.5-flash
   GEMINI_MAX_TOKENS=1000
   GEMINI_TEMPERATURE=0.7
   ```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 测试连接
```bash
python gemini_client.py
```

## 🛡️ 安全最佳实践

### ✅ 正确做法
- 使用环境变量存储 API key
- 将 `.env` 文件添加到 `.gitignore`
- 定期轮换 API key
- 设置使用限制和配额

### ❌ 错误做法
- 在代码中硬编码 API key
- 将 API key 提交到 Git
- 在日志中输出 API key
- 分享 API key 给他人

## 🔧 使用示例

```python
from gemini_client import GeminiClient

# 初始化客户端
client = GeminiClient()

# 生成文本
response = client.generate_text("你好，世界！")
print(response)

# 分析文本
analysis = client.analyze_text("这是一个很好的产品！", "sentiment")
print(analysis)
```

## 📊 监控使用情况

定期检查 Google AI Studio 的使用情况：
- 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 查看 API 使用统计
- 监控配额使用情况

## 🚨 紧急情况

如果 API key 泄露：
1. 立即在 Google AI Studio 中删除该 key
2. 创建新的 API key
3. 更新所有环境变量
4. 检查是否有异常使用 