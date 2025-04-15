# StudySync - 智能学习助手

StudySync 是一个基于人工智能的智能学习助手系统，旨在帮助学生更高效地学习和复习。系统通过分析用户的学习数据，提供个性化的学习建议和练习题目。

## 功能特性

- **智能学习计划**：根据用户的学习目标和时间安排，自动生成个性化的学习计划
- **每日练习**：每天推送适合用户当前学习进度的练习题
- **错题本**：自动收集和整理用户的错题，方便针对性复习
- **知识图谱**：可视化展示用户的知识掌握情况，帮助发现薄弱环节
- **学习统计**：提供详细的学习数据统计和分析
- **用户认证**：安全的用户注册和登录系统

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- JWT 认证
- OpenAI API

### 前端
- React 18
- TypeScript
- Ant Design 5
- React Router 6
- Axios
- Chart.js

## 项目结构

```
StudySync/
├── backend/                 # 后端服务
│   ├── app/                # 应用主目录
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   ├── crud/          # 数据库操作
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic 模型
│   │   └── services/      # 业务逻辑
│   ├── tests/             # 测试文件
│   └── requirements.txt   # Python 依赖
│
├── frontend/               # 前端应用
│   ├── public/            # 静态资源
│   └── src/               # 源代码
│       ├── components/    # 可复用组件
│       ├── hooks/         # 自定义 Hooks
│       ├── pages/         # 页面组件
│       ├── services/      # API 服务
│       └── utils/         # 工具函数
│
└── README.md              # 项目文档
```

## 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

## 安装和运行

### 后端

1. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

4. 初始化数据库：
```bash
python -m app.db.init_db
```

5. 运行开发服务器：
```bash
uvicorn app.main:app --reload
```

### 前端

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置 API 地址等
```

3. 运行开发服务器：
```bash
npm start
```

## API 文档

启动后端服务后，访问 `http://localhost:8000/docs` 查看完整的 API 文档。

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 