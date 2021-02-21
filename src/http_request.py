"""任意のURLへリクエストを発行する"""

# https://note.nkmk.me/python-requests-usage/
import requests
import consts

FUNCTION_NAME = 'hello_world'
URL = 'https://{}-{}.cloudfunctions.net/{}'.format(consts.DEFAULT_LOCATION, consts.PROJECT_ID, FUNCTION_NAME)
REQUEST_PARAMETER = ''

# GETリクエストにパラメーターを追加
payload = REQUEST_PARAMETER if REQUEST_PARAMETER else {}

# リクエストを発行し結果を得る
response = requests.get(URL, params=payload)
response.raise_for_status()

# responseから様々な情報を取得可能
print(response.url)
print(response.status_code)
print(response.headers)
print(response.encoding)
print(response.text)
