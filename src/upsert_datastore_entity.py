"""ETL月次バッチKindの処理完了フラグを設定する"""

from datetime import datetime, timedelta, timezone
from google.cloud import datastore
import consts
import pprint

KIND_NAME = "OperationDate"
KEY = "20210205"
COLUMN_1 = "ActiveFlg"
VALUE_1 = 1
COLUMN_2 = "date"
VALUE_2 = "20210205"
# COLUMN_3 = ""
# VALUE_3 = ""

JST = timezone(timedelta(hours=+9), 'JST')
jst_now = datetime.now(JST)

client = datastore.Client(consts.PROJECT_ID)
key = client.key(KIND_NAME, KEY)
entity = datastore.Entity(key=key)
# TODO: 既存のカラムを全て指定しない場合、指定しないカラムは失くなってしまうことを回避する
entity.update({
    COLUMN_1: VALUE_1,
    COLUMN_2: VALUE_2,
    # COLUMN_3: VALUE_3,
})
client.put(entity)
pprint.pprint('put entity for {} in {}.'.format(KEY, KIND_NAME))