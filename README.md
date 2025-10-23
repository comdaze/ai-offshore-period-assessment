# 🌊 海上风电巡检风险评估系统

基于 NB/T 11768-2025 标准的专业巡检风险评估助手，集成天气、海洋、船舶等多维度数据分析。

## 功能特性

### 🚢 船舶信息查询
- 按船名搜索船舶信息
- 按 MMSI 查询船舶详细位置和状态  
- 多船舶位置信息查询
- 船舶周边范围内的其他船舶分布查询
- 船籍信息和档案资料查询

### 🌊 海洋环境监测
- 实时天气数据获取
- 海洋气象条件分析
- 港口信息查询

### 🤖 智能风险评估
- 基于 NB/T 11768-2025 标准
- 多维度数据融合分析
- AI 驱动的风险评估

## 技术架构

- **前端**: Streamlit Web 应用
- **AI 引擎**: Strands AI Agent 框架
- **数据源**: 
  - 船舶 AIS 数据
  - Open-Meteo 气象数据
  - 高德地图 API
- **后端**: Python + FastAPI

## 快速开始

### 环境要求
- Python 3.8+
- Node.js (用于 MCP 服务器)

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
复制 `.env.example` 为 `.env` 并配置相关 API 密钥：
```bash
cp .env.example .env
```

### 运行应用
```bash
# 启动 Streamlit 应用
python run_streamlit.py

# 或直接运行
streamlit run streamlit_app.py
```

## 项目结构

```
offshore-risk/
├── streamlit_app.py      # Streamlit 主应用
├── agent.py             # AI Agent 核心逻辑
├── ship_service.py      # 船舶数据服务
├── main.py             # 主程序入口
├── requirements.txt     # Python 依赖
├── .env.example        # 环境变量模板
└── docs/               # 文档目录
```

## 使用示例

### 船舶查询
```python
# 搜索船名包含'FENG DIAN'的船舶信息
# 查询MMSI为220150003的船舶详细位置和状态
# 查询多艘船舶的位置信息
```

### 风险评估
```python
# 查看MMSI为440200920周边10海里范围内的船舶分布
# 基于当前海况进行风险评估
```

## 标准合规

本系统严格遵循 **NB/T 11768-2025** 海上风电巡检相关标准，确保评估结果的专业性和准确性。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。
