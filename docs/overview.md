# 海上风电巡检风险评估系统 - 项目概览

## 项目简介

海上风电巡检风险评估系统是一个基于AI Agent的智能评估平台，集成了船舶监控、海洋气象、航线规划等多维度数据，为海上风电场巡检作业提供专业的风险评估服务。系统遵循NB/T 11768-2025《海上风电场工程水域安全管理技术导则》标准。

## 技术栈

### 核心框架
- **AI Agent框架**: Strands Agents SDK (>=1.12.0)
- **大语言模型**: Amazon Bedrock (Claude Sonnet 4)
- **前端框架**: Streamlit (>=1.28.0)
- **后端框架**: FastAPI + FastMCP
- **协议支持**: Model Context Protocol (MCP)

### 开发语言
- **Python**: 主要开发语言 (3.11+)
- **TypeScript**: CDK基础设施即代码

### 云服务
- **AWS Bedrock**: LLM推理服务
- **AWS ECS Fargate**: 容器化部署
- **AWS ALB**: 应用负载均衡
- **AWS CloudWatch**: 日志和监控

### 外部API集成
- **ShipXY API**: 船舶位置、港口、航线等数据
- **高德地图API**: 地理位置和路径规划
- **Open-Meteo API**: 气象和海洋数据

## 项目结构

```
offshort-risk/
├── agent.py                    # AI Agent核心逻辑
├── ship_service.py             # ShipXY API服务封装
├── shipxy-server.py            # ShipXY MCP服务器
├── streamlit_app.py            # Streamlit前端应用
├── main.py                     # 命令行交互入口
├── run_streamlit.py            # Streamlit启动脚本
├── requirements.txt            # Python依赖
├── .env                        # 环境变量配置
├── .env.example                # 环境变量示例
├── deploy.sh                   # 部署脚本
│
├── docs/                       # 文档目录
│   ├── overview.md             # 项目概览（本文档）
│   ├── NBT+10579-2021+海上风电场运行安全规程.md
│   └── NB_T 11768-2025 海上风电场工程水域安全管理技术导则.md
│
├── docker/                     # Docker配置（旧版）
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── app.py
│
├── docker-backend/             # 后端Docker配置
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── shipxy-server.py
│   ├── .env
│   └── app/
│       └── app.py
│
├── docker-frontend/            # 前端Docker配置
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── streamlit_app.py
│
├── cdk-deployment/             # AWS CDK部署配置
│   ├── bin/
│   │   └── cdk-app.ts          # CDK应用入口
│   ├── lib/
│   │   └── offshore-wind-inspection-stack.ts  # 基础设施定义
│   ├── package.json            # Node.js依赖
│   ├── tsconfig.json           # TypeScript配置
│   ├── cdk.json                # CDK配置
│   └── cdk.out/                # CDK输出文件
│
├── .amazonq/                   # Amazon Q配置
│   └── rules/
│       └── lang.md             # 语言偏好规则
│
└── __pycache__/                # Python缓存文件
```

## 核心模块说明

### 1. agent.py - AI Agent核心
- **功能**: 实现基于Strands Agents的智能对话系统
- **集成**: 
  - ShipXY MCP服务器（船舶数据）
  - 高德地图MCP服务器（地理数据）
  - Open-Meteo MCP服务器（气象数据）
- **工具**: calculator, file_read, shell, current_time, http_request, editor, retrieve
- **模型**: Amazon Bedrock Claude Sonnet 4

### 2. ship_service.py - 船舶服务API
- **功能**: ShipXY API的Python封装
- **主要接口**:
  - 船舶搜索与查询
  - 船舶位置追踪
  - 周边船舶监控
  - 港口信息查询
  - 航线规划
  - 海洋气象数据
  - 台风信息
  - 潮汐数据

### 3. shipxy-server.py - MCP服务器
- **功能**: 将ShipXY API封装为MCP服务器
- **协议**: Model Context Protocol (SSE传输)
- **端口**: 8000
- **工具数量**: 30+个MCP工具

### 4. streamlit_app.py - Web前端
- **功能**: 提供Web界面的交互式对话系统
- **特性**:
  - 实时对话显示
  - 思考过程可视化
  - 常用问题快捷按钮
  - 会话历史管理

### 5. main.py - 命令行入口
- **功能**: 提供命令行交互界面
- **特性**:
  - 交互式问答
  - 示例问题展示
  - 系统初始化管理

### 6. cdk-deployment/ - 基础设施即代码
- **功能**: AWS云资源自动化部署
- **资源**:
  - VPC网络（2个可用区）
  - ECS Fargate集群
  - Application Load Balancer
  - CloudWatch日志组
  - IAM角色和策略
- **服务**:
  - 后端服务（FastAPI + MCP）
  - 前端服务（Streamlit）

## 主要依赖

### Python依赖 (requirements.txt)
```
strands-agents>=1.12.0          # AI Agent框架
strands-agents-tools>=0.2.11    # Agent工具集
streamlit>=1.28.0               # Web前端框架
python-dotenv                   # 环境变量管理
mcp                             # MCP协议核心
mcp[cli]                        # MCP命令行工具
httpx                           # 异步HTTP客户端
requests                        # HTTP客户端
pandas                          # 数据处理
numpy                           # 数值计算
pydantic                        # 数据验证
```

### Node.js依赖 (cdk-deployment/package.json)
```
aws-cdk-lib: 2.161.1            # AWS CDK库
constructs: ^10.0.0             # CDK构造库
typescript: ~4.9.5              # TypeScript编译器
ts-node: ^10.9.1                # TypeScript运行时
jest: ^29.5.0                   # 测试框架
```

## 环境变量配置

系统需要以下环境变量（参考.env.example）：

```bash
# ShipXY API配置
SHIPXY_API_KEY=your_shipxy_api_key

# 高德地图API配置
AMAP_MAPS_API_KEY=your_amap_api_key

# AWS Bedrock配置
AWS_DEFAULT_REGION=us-east-1
MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
MODEL_TEMPERATURE=1.0
MODEL_MAX_TOKENS=8000
MODEL_THINKING_TOKENS=4000

# MCP服务器配置
SHIPXY_MCP_SERVER_URL=http://localhost:8000/sse
```

## 部署架构

### 本地开发
1. **命令行模式**: `python main.py`
2. **Web模式**: `streamlit run streamlit_app.py`
3. **MCP服务器**: `python shipxy-server.py`

### Docker部署
- **后端容器**: FastAPI + ShipXY MCP服务器
- **前端容器**: Streamlit应用

### AWS云部署
- **计算**: ECS Fargate（无服务器容器）
- **网络**: VPC + ALB
- **存储**: CloudWatch Logs
- **AI**: Amazon Bedrock
- **部署工具**: AWS CDK

## 功能特性

### 1. 船舶监控
- 船舶搜索（按名称、MMSI、IMO）
- 实时位置追踪
- 周边船舶分析
- 船舶档案查询
- 船舶轨迹回放

### 2. 港口服务
- 港口信息查询
- 泊位船舶监控
- 锚地船舶统计
- 预计到港船舶
- 港口历史记录

### 3. 航线规划
- 点对点航线规划
- 港口间航线规划
- 距离计算
- ETA预测

### 4. 海洋气象
- 实时天气数据
- 海况预报
- 台风追踪
- 潮汐信息
- 风浪分析

### 5. 风险评估
- 基于NB/T 11768-2025标准
- 多维度数据综合分析
- 安全建议生成
- 风险等级评定

## 标准规范

系统内置以下行业标准文档：
- **NB/T 10579-2021**: 海上风电场运行安全规程
- **NB/T 11768-2025**: 海上风电场工程水域安全管理技术导则

## 开发团队

- **开发语言**: 中文
- **代码注释**: 中文
- **文档语言**: 中文
- **变量命名**: 英文

## 版本信息

- **项目版本**: 1.0.0
- **Python版本**: 3.11+
- **Node.js版本**: 18.14.6
- **AWS CDK版本**: 2.161.1

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入API密钥
```

### 3. 启动MCP服务器
```bash
python shipxy-server.py
```

### 4. 启动应用
```bash
# 命令行模式
python main.py

# Web模式
streamlit run streamlit_app.py
```

### 5. 云端部署
```bash
cd cdk-deployment
npm install
cdk deploy
```

## 许可证

本项目为内部使用项目，未公开许可证信息。
