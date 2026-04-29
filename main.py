import os
from crewai import Agent, Task, Crew, Process

# ==========================================
# 0. Google Gemini API 配置
# ==========================================
# 填入你在 Google AI Studio 申请的 API Key (通常是 AIza 开头)
os.environ["GEMINI_API_KEY"] = "AIzaSy_在这里填入你的真实_Gemini_Key"

# 告诉底层框架使用 Gemini 模型 (带有 gemini/ 前缀)
# 这里使用的是 1.5 Flash，速度极快且聪明；如果你想用更强的，可以改成 gemini/gemini-1.5-pro
GEMINI_MODEL = "gemini/gemini-pro"

print("🚀 正在通过 Google Gemini 引擎初始化投研系统...")

# ==========================================
# 第一步：定义 Agent 团队
# ==========================================

data_gatherer = Agent(
    role='高级宏观数据感知专家',
    goal='从资讯中提取关键财务数据、宏观指标和产业链异动信息。',
    backstory='你拥有强大的数据敏感度，擅长在海量新闻中快速锁定核心量化指标。',
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

logical_reasoner = Agent(
    role='资深产业链推演分析师',
    goal='进行多步骤的上下游产业链推演，预测宏观事件对特定行业的长期影响。',
    backstory='你擅长“蝴蝶效应”分析，能根据基础原材料的变动推导出三层之外的行业影响。',
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

risk_manager = Agent(
    role='严格的合规与风控总监',
    goal='审查推演结论，识别潜在的黑天鹅风险，确保预测逻辑严谨合规。',
    backstory='你性格保守严谨，负责拦截过于激进的预测，并补充政策风险提示。',
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

report_writer = Agent(
    role='首席金融报告撰稿人',
    goal='将推演逻辑转化为结构清晰、专业严谨的深度投研简报。',
    backstory='你擅长金融术语，能将复杂的推理过程包装成具有极高可读性的专业研报。',
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

# ==========================================
# 第二步：定义任务流
# ==========================================

input_market_event = """
突发：中东核心产油区港口封锁，国际原油价格单日跳涨 8%。
同时，某头部新能源车企宣布在欧洲市场降价 15%。
"""

task1_gather = Task(
    description=f'分析以下事件并提取核心变量：\n{input_market_event}',
    expected_output='一份结构化的核心数据列表。',
    agent=data_gatherer
)

task2_reasoning = Task(
    description='推演原油涨价与新能源车降价对国内锂电供应链及燃油车市场的复合传导效应。',
    expected_output='一份包含逻辑链路的深度推演报告。',
    agent=logical_reasoner
)

task3_risk_check = Task(
    description='对推演报告进行压力测试，指出其中可能的盲点和政策干预风险。',
    expected_output='一份带有风控修正建议的草案。',
    agent=risk_manager
)

task4_write_report = Task(
    description='整合所有逻辑，撰写一份《全球能源波动下的汽车产业链影响分析》研报。',
    expected_output='一篇 Markdown 格式的专业投研研报。',
    agent=report_writer
)

# ==========================================
# 第三步：实例化 Crew 并执行
# ==========================================

research_crew = Crew(
    agents=[data_gatherer, logical_reasoner, risk_manager, report_writer],
    tasks=[task1_gather, task2_reasoning, task3_risk_check, task4_write_report],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("==============================================")
    print("Agent 开始协作（基于 Google Gemini 引擎）...")
    print("==============================================")

    result = research_crew.kickoff()

    print("\n\n==============================================")
    print("🎉 投研报告生成完毕：")
    print("==============================================")
    print(result)