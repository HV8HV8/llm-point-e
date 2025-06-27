import json
import pandas as pd
import os
from llm_module import LLMAgent

# 设置 API 密钥
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("请设置 API_KEY 环境变量")

# 初始化 LLMAgent
llm_agent = LLMAgent(api_key)

# 用户输入的描述
user_input = "绿色的椅子"

# 要测试的不同 temperature 值
temperatures = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]

# 存储不同 temperature 下的生成结果
results = {}

for temperature in temperatures:
    structured_params = llm_agent.generate_3d_prompt(user_input, temperature)
    results[temperature] = structured_params

# 将结果转换为 DataFrame
data = []
for temperature, params in results.items():
    row = {
        "Temperature": temperature,
        "object": params.get("object", ""),
        "dimensions": params.get("dimensions", ""),
        "material": params.get("material", ""),
        "color": params.get("color", ""),
        "style": params.get("style", ""),
        "modifications": params.get("modifications", [])
    }
    data.append(row)

df = pd.DataFrame(data)

# 打印表格
print(df)

# 将表格保存为 CSV 文件
df.to_csv('temperature_results.csv', index=False)
