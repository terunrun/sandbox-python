"""システム日付（日本時間）を取得する"""

from datetime import datetime, timedelta, timezone
import pprint

JST = timezone(timedelta(hours=+9), 'JST')
jst_now = datetime.now(JST)
today = jst_now.strftime('%Y%m%d')
pprint.pprint("Today is {}".format(today))