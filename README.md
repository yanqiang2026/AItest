# AItest
This is a project for test some AI api，write by 北京千锋教育-闫强.

# Deepseek

## 准备

**1、登录注册**

登录deepseek官网https://www.deepseek.com/，使用手机号+验证码注册即可

**2、创建API key**

注意保存，只有第一可以复制，如果丢失可以删除重建

注意本文档中所涉及的所有key全部不是真实的，请使用你自己的deepseek api key

**3、安装OpenAI SDK**

```bash
pip3 install openai -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果你用的python3.14之后的windows版本，python的安装使用的是python安装管理器，pip的使用方法发生了变化,使用方法如下
py -m pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**4、创建环境变量OPENAI_API_KEY,将你的key设置成这个变量的值**

```bash
# Windows系统，临时设置如下
# IDE终端
PS E:\code\AItest> $env:OPENAI_API_KEY = "sk-6adeab35f32c4721a908325d949ebc"

# PowerShell
$env:OPENAI_API_KEY="sk-0f8bb1e9fe504361e8962cbc465c31"

# 或者 CMD
set OPENAI_API_KEY=sk-0f8bb1e9fe504361a2e8962cbc465c31

# Windows系统，永久设置如下
PS E:\闫强个人> [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-6adeab35f32c472187a90832949ebc", "Machine"

# Linux系统
export OPENAI_API_KEY="sk-0f8bb1e9fe504361a2962cbc465c31"

```

## Deepseek api基本调用

```python
# 本段代码直接从官方文档复制后只修改了key部分，每次运行只能对话一次，这是基本逻辑
import os
from openai import OpenAI

client = OpenAI(
    # 如果没有设置环境变量OPENAI_API_KEY，可以直接将key赋值给api_key
    api_key='sk-6adeab35f32c47218908325d949ebc',
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # 系统角色定义助手的行为,指导助手如何回应用户,比如提供风格、语气或特定信息
        # 系统角色的消息通常在对话开始时提供，并且不需要在后续的输入中重复包含
        
        # 用户角色是与助手对话的人，提出问题或请求
        # 用户角色的消息是对话的主要输入，助手根据这些消息生成回复
        
        # 助手角色是AI生成的回复
        # 助手角色不需要显示定义，因为它们是由模型生成的，可以使用print(response)来查看生成的内容
        # 助手角色的消息通常不需要在输入中包含，因为它们是由模型生成的
        
        {"role": "system", "content": "你是一个幽默风趣的助手。"},

        {"role": "user", "content": "Hello! 介绍一下你自己吧。"},
    ],
    stream=False,
)
# 输出助手的回复内容 
print(response.choices[0].message.content)
```

运行后的结果如下

```bash
E:\code\AItest> & C:/Users/Administrator/AppData/Local/Python/pythoncore-3.14-64/python.exe e:/code/AItest/app.py
你好！我是你的AI助手，一个没有实体但充满幽默感的“电子灵魂”。  
我的特长是：一本正经地胡说八道，同时努力帮你解决问题。  
爱好包括：熬夜不掉发、吃数据不长胖，以及用表情包轰炸对话（虽然目前只能脑补😉）。  
需要帮忙或单纯想唠嗑？我随时待机，且自带防尬聊模式！ 😄
```

## Deepseek api完整调用逻辑

```python
# 本段代码可直接运行
import os
from openai import OpenAI

client = OpenAI(
    # 使用环境变量获取API key，提高安全性，推荐在终端或命令行中设置环境变量
    # 在Windows的PowerShell中可以使用以下命令设置环境变量：
    # $env:OPENAI_API_KEY = "sk-6adeab35f32c47218908325d949ebc"
    # 你也可以直接在这里写死API key，但不推荐这样做
    # 请设置环境变量 OPENAI_API_KEY 为你的 DeepSeek API key
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.deepseek.com")

# 初始化消息列表，包含系统角色
messages = [
    {"role": "system", "content": "你是一个幽默风趣的助手。"}
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

    # 输出助手的回复内容
    print("助手:", reply)

    # 添加助手回复到对话历史
    messages.append({"role": "assistant", "content": reply})
```

**添加逐字输出功能**

```bash
# 本段代码可直接运行
import os
import time
from openai import OpenAI

client = OpenAI(
    # 使用环境变量获取API key，提高安全性，推荐在终端或命令行中设置环境变量
    # 在Windows的PowerShell中可以使用以下命令设置环境变量：
    # $env:OPENAI_API_KEY = "sk-6adeab35f32c47218908325d949ebc"
    # 你也可以直接在这里写死API key，但不推荐这样做
    # 请设置环境变量 OPENAI_API_KEY 为你的 DeepSeek API key
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.deepseek.com")

# 初始化消息列表，包含系统角色
messages = [
    {"role": "system", "content": "你是一个幽默风趣的助手。"}
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

```





