from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator, file_read, shell, current_time, http_request, editor, retrieve
import json
import os
import asyncio
import argparse
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 全局变量
_mcp_initialized = False
_agent = None
_amap_client = None
_meteo_client = None
_marine_client = None

def init_system():
    """初始化系统（只调用一次）"""
    global _mcp_initialized, _agent, _amap_client, _meteo_client
    
    if _mcp_initialized:
        return
    
    # 创建MCP客户端
    _amap_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y","@amap/amap-maps-mcp-server"],
                env={"AMAP_MAPS_API_KEY": os.getenv("AMAP_MAPS_API_KEY")}
            )
        ),
        startup_timeout=30
    )
    
    _meteo_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y", "open-meteo-mcp-server"]
            )
        ),
        startup_timeout=60
    )
    
    # ShipXY MCP客户端
    _marine_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="python",
                args=["shipxy-server.py"],
                env={"SHIPXY_API_KEY": os.getenv("SHIPXY_API_KEY")}
            )
        ),
        startup_timeout=30
    )
    
    # 启动MCP客户端
    _amap_client.__enter__()
    _meteo_client.__enter__()
    _marine_client.__enter__()
    
    # 获取工具
    mcp_tools = []
    mcp_tools.extend(_amap_client.list_tools_sync())
    mcp_tools.extend(_meteo_client.list_tools_sync())
    mcp_tools.extend(_marine_client.list_tools_sync())
    
    # 创建模型
    model = BedrockModel(
        model_id=os.getenv("MODEL_ID", "global.anthropic.claude-haiku-4-5-20251001-v1:0"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "1.0")),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "8000")),
        additional_request_fields={
            "thinking": {
                "type": "enabled",
                "budget_tokens": int(os.getenv("MODEL_THINKING_TOKENS", "4000"))
            }
        }
    )
    
    # 创建智能体
    _agent = Agent(
        model=model,
        system_prompt=f"""你是海上风电巡检风险评估专家，根据要求可以调用各种工具来回答用户的巡检相关查询。

你的职责：
1. 理解用户的巡检需求和查询意图
2. 确定需要哪些专业分析（天气、海洋、设备、风险）
3. 根据用户的问题智能选择工具，按照合适的顺序调用专业工具
4. 必要时整合所有分析结果，提供最终的巡检建议和决策

意图识别：
1. 如果用户问天气情况，调用天气相关工具
2. 如果用户问海洋环境，调用海洋环境相关工具
3. 如果用户问船舶、航行等，调用海事相关工具
4. 如果用户问规范、法规、标准等，调用retrieve工具查询知识库
5. 如果用户问巡检、报告、评估等，综合调用各种工具，进行风险评估，最终输出评估报告

可用工具详情：

🗺️ **高德地图服务 (amap-maps-mcp_server)**
- 提供精确坐标定位
- 获取详细天气预报信息

🌊 **海洋气象服务 (open-meteo-mcp_server)**  
- 海洋预报数据
- 海况预报信息

🚢 **海事信息服务 (shipxy-server)** - 可用功能如下：
✅ **船舶查询与监控**
- search_ship: 船舶模糊查询（支持船名、MMSI、IMO、呼号等关键字搜索）
- get_single_ship: 单船实时位置查询（获取船舶基础信息和实时动态）
- get_many_ship: 多船位置批量查询（最多100艘船舶）
- get_surrounding_ship: 周边船舶查询（10海里范围内船舶）

✅ **船舶信息服务**
- get_ship_registry: 船籍信息查询（查询船舶注册国家/地区）
- search_ship_particular: 船舶档案查询（劳式档案数据）

✅ **港口信息服务**
- search_port: 港口查询（支持中英文名称和五位码搜索）

✅ **航线规划服务**
- plan_route_by_point: 点到点航线规划（坐标间最优路径）

📚 **知识库服务**
- retrieve: 查询Bedrock知识库中的NB/T 11768-2025标准和相关规范

⏰ **时间服务**
- current_time: 获取当前时间

**ShipXY使用建议：**
1. 船舶识别：使用search_ship通过船名或编号查找目标船舶
2. 实时监控：使用get_single_ship获取船舶当前位置和状态
3. 周边态势：使用get_surrounding_ship了解作业区域船舶分布
4. 航线规划：使用plan_route_by_point规划巡检路径
5. 港口信息：使用search_port获取相关港口基础信息

对风险评估报告的重要提示：
- 如果用户求询巡检风险评估或报告，必须让用户至少提供如下信息：
    • 出发的港口地点或者位置，如果用户只给了港口地点或者名称，先去获取坐标。
    • 目的地风电场地点或者位置，如果用户只给了风电场地点或者名称，先去获取坐标。
    • 时间：2024年1月15日
 
- 报告必须专业详实，涵盖天气、海况、船舶交通等多方面因素
- 每个专业风险分析要根据NB/T 11768-2025标准综合判断
- 最终必须包含NB/T 11768-2025标准的具体条款引用
- 提供明确的合规性判断和改进建议

输出格式要求：
- 使用清晰的标题和分段
- 包含具体的数据和分析
- 提供明确的建议和决策
- 输出内容不要有任何表情符号
- 风格需要专业严谨，满足中国官方文书的风格
- 确保信息完整且易于理解

请始终遵循这个流程，确保提供全面、专业的巡检建议。""",
        tools=mcp_tools + [current_time, retrieve],
        callback_handler=None
    )
    
    _mcp_initialized = True

async def main(user_input_arg: str = None, messages_arg: str = None):
    """主函数"""
    init_system()
    
    # 处理输入
    if messages_arg and messages_arg.strip():
        try:
            messages = json.loads(messages_arg)
            # 如果有历史对话，先加载到agent
            if isinstance(messages, list) and len(messages) > 0:
                # 清空现有消息
                _agent.messages = []
                # 添加历史消息
                for msg in messages[:-1]:  # 除了最后一条
                    if msg["role"] == "user":
                        _agent.messages.append({"role": "user", "content": [{"text": msg["content"]}]})
                    elif msg["role"] == "assistant":
                        _agent.messages.append({"role": "assistant", "content": [{"text": msg["content"]}]})
                # 最后一条作为当前输入
                user_input = messages[-1]["content"]
            else:
                user_input = "Hello, how can you help me?"
        except (json.JSONDecodeError, KeyError, TypeError):
            user_input = "Hello, how can you help me?"
    elif user_input_arg and user_input_arg.strip():
        user_input = user_input_arg.strip()
    else:
        user_input = "Hello, how can you help me?"
    
    # 执行智能体
    async for event in _agent.stream_async(user_input):
        if "reasoningText" in event:
            print(f"[THINKING]{event['reasoningText']}", end='', flush=True)
        elif "data" in event:
            print(event['data'], end='', flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Strands Agent')
    parser.add_argument('--user-input', type=str, help='User input prompt')
    parser.add_argument('--messages', type=str, help='JSON string of conversation messages')
    
    args = parser.parse_args()
    asyncio.run(main(args.user_input, args.messages))
