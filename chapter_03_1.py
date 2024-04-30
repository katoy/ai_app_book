# 必要なパッケージをインストールするためのコメントは適切に文書化されていますが、
# このコードスニペットでは実行できないため、通常はスクリプトの先頭に記載します。
# pip install -U langchain-openai

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

lim = ChatOpenAI()  # ChatOpenAI のインスタンスを作成

message = 'Hi, ChatGPT!'  # 人間のメッセージ

# system_message = 'You are a helpful assistant.'
system_message = 'You are a helpful assistant. please reply in japanese.'

# メッセージリストを定義
messages = [
    SystemMessage(content=system_message), # システムメッセージ
    HumanMessage(content=message) # 人間のメッセージ
]

# ChatOpenAI の invoke メソッドを使用して応答を生成
response = lim.invoke(messages)  # 'invoke' を使用して API を呼び出す
print(response)
# print(response.content)  # 応答の内容だけを表示
