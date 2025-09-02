import os
from azure.cosmos import CosmosClient, PartitionKey

# 1. 接続情報をセット
endpoint = "<ここにCosmos DBのURI>"
key = "<ここにCosmos DBのPRIMARY KEY>"

# 2. クライアント作成
client = CosmosClient(endpoint, key)

# 3. データベースとコンテナ（テーブルのようなもの）を作成
database_name = "cosmicworks"
container_name = "products"

# データベースがなければ作成
database = client.create_database_if_not_exists(id=database_name)

# コンテナがなければ作成（パーティションキーは/category）
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400
)

# 4. データを追加（upsert: 既存なら上書き、なければ新規作成）
item = {
    "id": "item1",
    "category": "gear-surf-surfboards",
    "name": "Yamba Surfboard",
    "quantity": 12,
    "sale": False
}
container.upsert_item(item)

# 5. データを取得（idとパーティションキーで指定）
read_item = container.read_item(item="item1", partition_key="gear-surf-surfboards")
print("読み取ったアイテム：", read_item)

# 6. クエリで検索（同じカテゴリの商品を全部取得）
query = "SELECT * FROM products p WHERE p.category = @category"
items = list(container.query_items(
    query=query,
    parameters=[{"name": "@category", "value": "gear-surf-surfboards"}],
    enable_cross_partition_query=False
))
print("クエリ結果：", items)