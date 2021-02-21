"""指定のBigQueryテーブルの最終更新日が処理実行日と同一かどうかを判定する"""

from datetime import datetime, timedelta, timezone
from google.cloud import bigquery
import get_today
import pprint
import consts

TABLE_NAME = 'import.test_table'

client = bigquery.Client(consts.PROJECT_ID)
table = client.get_table(table=TABLE_NAME)
table_last_modified_jst = table.modified + timedelta(hours=+9)
pprint.pprint('{} modified at {}'.format(TABLE_NAME, table_last_modified_jst))

table_last_modified_jst_str = table_last_modified_jst.strftime("%Y%m%d") 
pprint.pprint('modified date is {}'.format(table_last_modified_jst_str))

today = get_today()
pprint.pprint('today is {}'.format(today))

if today == table_last_modified_jst_str:
    pprint.pprint('{} is modified today'.format(TABLE_NAME))
else:
    pprint.pprint('{} is not modified today'.format(TABLE_NAME))
