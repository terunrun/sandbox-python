"""システム日付（日本時間）を取得する"""

from datetime import datetime, timedelta, timezone

# デフォルトのタイムゾーンのまま取得する
now = datetime.now()
print("Now is {}".format(now))
today = now.strftime('%Y%m%d')
print("Today is {}".format(today))

# 日付だけならより簡単に
today = datetime.today()
print("Today is {}".format(datetime.strftime(today, '%Y%m%d')))
yesterday = today - timedelta(days=1)
print("Yesterday is {}".format(datetime.strftime(yesterday, '%Y%m%d')))

# 日本時間で取得する（デフォルトのタイムゾーンがUTCの場合）
jst = timezone(timedelta(hours=+9), 'JST')
jst_now = datetime.now(jst)
print("Now(JST) is {}".format(jst_now))
jst_today = jst_now.strftime('%Y%m%d')
print("Today(JST) is {}".format(jst_today))
