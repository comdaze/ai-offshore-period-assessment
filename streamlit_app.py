import streamlit as st
import subprocess
import json
import asyncio
import sys
import os

# 页面配置
st.set_page_config(
    page_title="海上风电巡检风险评估系统",
    page_icon="🌊",
    layout="wide"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "thinking_history" not in st.session_state:
    st.session_state.thinking_history = []

st.title("🌊 海上风电巡检风险评估系统")
st.write("基于NB/T 11768-2025标准的专业巡检风险评估助手，集成天气、海洋、船舶等多维度数据分析。")

# 示例问题
st.markdown("### 💡 常用问题示例")
questions = [
    "搜索船名包含'FENG DIAN'的船舶信息", "查询MMSI为220150003的船舶详细位置和状态", "查询多艘船舶的位置信息（如MMSI: 413248640, 413397110）",
    "查看MMSI为440200920周边10海里范围内的船舶分布", "查询船舶的船籍信息和档案资料", "搜索上海港的详细信息和五位码",
    "查询宁波港的基本信息", "搜索'青岛'相关的港口信息", "规划从坐标(121.5,31.2)到(120.2,30.3)的最优航线",
    "计算两个GPS坐标点之间的航行距离和路径", "获取北纬31.2度，东经121.5度的海洋天气情况", "查询长江口海域的海况预报",
    "分析明天的海况是否适合海上作业", "查询上海地区未来3天的天气预报", "获取长江口海域的风速风向信息",
    "分析当前浙江舟山海域天气条件对巡检作业的影响", "根据NB/T 11768-2025标准，海上风电巡检的安全要求是什么？", "查询海上风电巡检作业的天气条件限制标准",
    "NB/T 11768-2025标准中关于船舶交通安全距离的规定", "海上风电场巡检作业的人员安全防护要求", "我需要对后天从上海港长江口南岸港区出发去申能集团临港海上风电场进行巡检风险评估",
    "分析明天上午10点在南汇风电场进行海上风电巡检的安全性", "根据NB/T 11768-2025标准评估当前海况是否适合巡检作业", "综合分析当前洋山港出发到金山风电场一期的天气、海况、船舶交通对巡检作业的影响"
]

cols = st.columns(3)
for i, question in enumerate(questions):
    with cols[i % 3]:
        if st.button(question, key=f"q_{i}"):
            st.session_state.example_prompt = question

# 显示历史消息
assistant_count = 0
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if assistant_count < len(st.session_state.thinking_history):
                thinking = st.session_state.thinking_history[assistant_count]
                if thinking:
                    with st.expander("🧠 Thinking", expanded=False):
                        st.text(thinking)
            assistant_count += 1
        st.markdown(message["content"])

# 处理示例问题
prompt = None
if "example_prompt" in st.session_state:
    prompt = st.session_state.example_prompt
    del st.session_state.example_prompt

# 聊天输入
if not prompt:
    prompt = st.chat_input("请输入您的巡检查询...")

if prompt:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    
    # 显示助手响应
    with st.chat_message("assistant"):
        thinking_expander = st.expander("🧠 Thinking", expanded=False)
        thinking_placeholder = thinking_expander.empty()
        response_placeholder = st.empty()
        
        try:
            # 构建包含历史对话的消息
            messages_json = json.dumps(st.session_state.conversation_history)
            
            # 调用agent.py，传递对话历史
            process = subprocess.Popen(
                ["python", "agent.py", "--messages", messages_json],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                cwd="./"
            )
            
            # 实时显示输出，区分 thinking 和回答
            thinking_text = ""
            output_text = ""
            
            for line in iter(process.stdout.readline, ''):
                if "[THINKING]" in line:
                    thinking_text += line.replace("[THINKING]", "")
                    thinking_placeholder.text(thinking_text)
                else:
                    output_text += line
                    response_placeholder.markdown(output_text)
            
            process.wait()
            
            # 添加响应到历史
            if output_text.strip():
                st.session_state.messages.append({"role": "assistant", "content": output_text.strip()})
                st.session_state.conversation_history.append({"role": "assistant", "content": output_text.strip()})
                st.session_state.thinking_history.append(thinking_text.strip())
                st.rerun()
                
        except Exception as e:
            st.error(f"调用agent.py时出错: {str(e)}")

# 侧边栏
with st.sidebar:
    st.header("📋 系统信息")
    st.info("海上风电巡检风险评估演示系统")
    
    st.header("🛠️ 可用功能")
    st.markdown("""
    - 🌤️ 天气预报查询
    - 🌊 海洋环境分析  
    - 🚢 船舶信息查询
    - 📚 标准规范检索
    - 📊 风险评估报告
    """)
    
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.session_state.thinking_history = []
        st.rerun()
    
    st.markdown("---")
    st.caption(f"💬 当前对话轮次: {len(st.session_state.conversation_history) // 2}")
