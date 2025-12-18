# 本段代码直接从官方文档复制后只修改了key部分
import os
import time
from openai import OpenAI

client = OpenAI(
    # 使用环境变量获取API key，提高安全性，推荐在终端或命令行中设置环境变量
    # 在Windows的PowerShell中可以使用以下命令设置环境变量：
    # $env:OPENAI_API_KEY = "sk-6adeab35f32c472187a908325d949ebc"
    # 你也可以直接在这里写死API key，但不推荐这样做
    # 请设置环境变量 OPENAI_API_KEY 为你的 DeepSeek API key
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.deepseek.com")

# 初始化消息列表，包含系统角色
messages = [
    {"role": "system", "content": "你是一个专业python开发人员，请用专业的严谨的话语回答用户的问题。"}
]

print("开始对话！输入 'quit' 或 '退出' 结束对话。")

while True:
    # 获取用户输入
    user_input = input("你: ")
    if user_input.lower() in ['quit', '退出']:
        print("对话结束。")
        break

    # 添加用户消息到对话历史
    messages.append({"role": "user", "content": user_input})

    # 发送请求
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
    )

    # 获取助手回复
    reply = response.choices[0].message.content

    # 输出助手的回复内容，逐字输出，间隔0.1秒
    print("助手: ", end='', flush=True)
    for char in reply:
        print(char, end='', flush=True)
        time.sleep(0.1)
    print()  # 换行

    # 添加助手回复到对话历史
    messages.append({"role": "assistant", "content": reply})

