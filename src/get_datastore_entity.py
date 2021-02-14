"""Datastoreから稼働カレンダーKindのEntityを取得する"""

from google.cloud import datastore
import consts
import pprint

KIND_NAME = "OperationDate"
FILETERING_COLUMN_1 = "ActiveFlg"
FILETERING_OPERATOR_1 = "="
FILETERING_VALUE_1 = "0"
# FILETERING_COLUMN_2 = ""
# FILETERING_OPERATOR_2 = ""
# FILETERING_VALUE_2 = ""
# ORDER_BY_COLUMN = ""

client = datastore.Client(consts.PROJECT_ID)
query = client.query(kind=KIND_NAME)
query.add_filter(FILETERING_COLUMN_1, FILETERING_OPERATOR_1, FILETERING_VALUE_1)
# query.add_filter(FILETERING_COLUMN_2, FILETERING_OPERATOR_2, FILETERING_VALUE_2)
# query.order = [ORDER_BY_COLUMN]
result = query.fetch(1)
pprint.pprint('result for datastore query: {}, type: {}'.format(result, type(result)))
for r in result:
    pprint.pprint(r)