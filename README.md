# BeeAiRating

一个基于AI的智能网站评分系统，使用先进的机器学习技术为网站提供多维度专业评估。

## 功能特性

- 🤖 **AI驱动的评分算法** - 基于机器学习的智能评分系统
- 📊 **多维度分析** - 内容质量、技术性能、用户体验、SEO优化、安全性
- 📈 **数据可视化** - 雷达图和柱状图展示评分结果
- 🌐 **Web界面** - 现代化响应式用户界面
- ⚡ **实时分析** - 快速准确的网站评估
- 📦 **批量评测** - 支持同时评测多个网站
- 🎯 **特征重要性分析** - 了解影响评分的因素
- 💡 **智能建议** - 基于评分结果提供改进建议
- 🔒 **安全评估** - SSL证书、安全策略检查
- 📱 **移动友好性检测** - 响应式设计评估

## 安装

1. 克隆项目：
```bash
git clone <repository-url>
cd BeeAiRating
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 安装依赖：
```bash
cd "back end"
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp env.example .env
# 编辑 .env 文件，添加您的 Google Gemini API 密钥
```

3. 启动应用：
```bash
python run.py
```

4. 在浏览器中访问：
- 基础评测界面：`http://localhost:5000/website-rating`
- 增强评测界面：`http://localhost:5000/enhanced-rating`

## 项目结构

```
BeeAiRating/
├── back end/                    # 后端代码
│   ├── app.py                  # 主应用文件
│   ├── enhanced_rating_model.py # 增强AI评分模型
│   ├── website_analyzer.py     # 网站分析器
│   ├── gemini_client.py        # Gemini AI客户端
│   ├── requirements.txt        # Python依赖
│   ├── run.py                  # 应用启动脚本
│   └── test_enhanced_features.py # 增强功能测试
├── website_rating.html         # 基础评测界面
├── enhanced_rating.html        # 增强评测界面
├── index.html                  # 主页
├── README.md                   # 项目说明
└── .cursorrule                 # Cursor规则
```

## API接口

### 单个网站评测
- **POST** `/api/rate-website`
- 请求体：`{"url": "https://example.com"}`
- 返回：网站评分和详细分析

### 批量网站评测
- **POST** `/api/rate-batch`
- 请求体：`{"urls": ["url1", "url2", "url3"]}`
- 返回：批量评测结果和统计信息

### 健康检查
- **GET** `/api/health`
- 返回：服务状态信息

## 开发

### 运行测试
```bash
# 运行基础测试
python test_app.py

# 运行网站评测测试
python test_website_rating.py

# 运行增强功能测试
python test_enhanced_features.py
```

### 代码质量
- 使用 `black` 格式化代码
- 使用 `flake8` 检查代码质量
- 使用 `pytest` 运行测试套件

### 模型训练
系统支持使用自定义数据训练评分模型：
```python
from enhanced_rating_model import EnhancedRatingModel

model = EnhancedRatingModel()
training_data = [
    (website_data1, rating1),
    (website_data2, rating2),
    # ...
]
model.train_model(training_data)
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License 