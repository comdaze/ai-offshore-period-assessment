#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import main as agent_main, init_system

async def interactive_chat():
    print("🌊 海上风电巡检风险评估系统")
    print("正在初始化...")
    
    # 启动时初始化系统
    init_system()
    
    print("系统就绪！输入 'quit' 退出")
    print("-" * 60)
    
    # 显示常用问题示例
    print("💡 常用问题示例：")
    print()
    print("🚢 船舶查询与监控：")
    print("  • 搜索船名包含'海洋'的船舶信息")
    print("  • 查询MMSI为440200920的船舶详细位置和状态")
    print("  • 查询多艘船舶的位置信息（如MMSI: 440200920, 413859483）")
    print("  • 查看MMSI为440200920周边10海里范围内的船舶分布")
    print("  • 查询船舶的船籍信息和档案资料")
    print()
    print("⚓ 港口信息查询：")
    print("  • 搜索上海港的详细信息和五位码")
    print("  • 查询宁波港的基本信息")
    print("  • 搜索'青岛'相关的港口信息")
    print()
    print("🛣️ 航线规划：")
    print("  • 规划从坐标(121.5,31.2)到(120.2,30.3)的最优航线")
    print("  • 计算两个GPS坐标点之间的航行距离和路径")
    print()
    print("🌊 海洋环境评估：")
    print("  • 获取北纬31.2度，东经121.5度的海洋天气情况")
    print("  • 查询长江口海域的海况预报")
    print("  • 分析明天的海况是否适合海上作业")
    print()
    print("🌤️ 天气预报分析：")
    print("  • 查询上海地区未来3天的天气预报")
    print("  • 获取长江口海域的风速风向信息")
    print("  • 分析当前天气条件对巡检作业的影响")
    print()
    print("📖 规范标准查询：")
    print("  • 根据NB/T 11768-2025标准，海上风电巡检的安全要求是什么？")
    print("  • 查询海上风电巡检作业的天气条件限制标准")
    print("  • NB/T 11768-2025标准中关于船舶交通安全距离的规定")
    print("  • 海上风电场巡检作业的人员安全防护要求")
    print()
    print("📋 综合风险评估：")
    print("  • 我需要对位于北纬32.5度，东经120.8度的海上风电场进行巡检风险评估")
    print("  • 分析明天上午10点在长江口进行海上风电巡检的安全性")
    print("  • 根据NB/T 11768-2025标准评估当前海况是否适合巡检作业")
    print("  • 综合分析当前天气、海况、船舶交通对巡检作业的影响")
    print()
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n请输入问题: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
                
            if not user_input:
                continue
                
            await agent_main(user_input, None)
            
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    asyncio.run(interactive_chat())
