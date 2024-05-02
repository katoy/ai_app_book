# See
# https://platform.openai.com/docs/models
#   モデル一覧
#
# https://di-acc2.com/programming/python/26024/#index_id13
#   Pythonで最新のGPTモデル情報を一括取得する

from openai import OpenAI
import pandas as pd
from datetime import datetime

def safe_parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp)
    except (TypeError, ValueError, OverflowError):
        return None

# APIクライアントの初期化（正しいAPIキーを設定）
client = OpenAI()

# モデルリストを取得
model_list = client.models.list().data

# リストの作成
created_at_list = []
model_id_list = []
object_list = []
owned_by_list = []

for model in model_list:
    # 'created'属性が存在しない場合はNoneを返します
    created_at = getattr(model, 'created', None)
    created_at_list.append(safe_parse_timestamp(created_at))
    model_id_list.append(getattr(model, 'id', 'Unknown'))
    object_list.append(getattr(model, 'object', 'Unknown'))
    owned_by_list.append(getattr(model, 'owned_by', 'Unknown'))

# データフレームの作成
df = pd.DataFrame({
    "created": created_at_list,
    "model_id": model_id_list,
    "object": object_list,
    "owned_by": owned_by_list
})

# データフレームを日付で降順に並び替え
df = df.sort_values("created", ascending=False).reset_index(drop=True)

# DataFrameをMarkdown形式で出力
print(df.to_markdown(index=False))
