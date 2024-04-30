# pip install -U langchain-openai

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

message = "Writing a book about creating an AI app with ChatGPT and Streamlit. Let's come up with one title."  # 人間のメッセージ

system_message = 'You are a helpful assistant.'

# メッセージリストを定義
messages = [
    SystemMessage(content=system_message), # システムメッセージ
    HumanMessage(content=message) # 人間のメッセージ
]

for temperature in [0, 0.5, 1]:
    lim = ChatOpenAI(temperature=temperature)
    print(f'[==== Temperature: {temperature} ====]')

    for i in range(5):  # 各温度で3つの異なる応答を生成
        response = lim.invoke(messages)
        print(response.content)
