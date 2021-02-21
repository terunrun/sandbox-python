"""任意のURLへリクエストを発行する"""

import requests
import google.auth.transport.requests
import google.oauth2.id_token
import consts

FUNCTION_NAME = 'hello_world'
URL = 'https://{}-{}.cloudfunctions.net/{}'.format(consts.DEFAULT_LOCATION, consts.PROJECT_ID, FUNCTION_NAME)
REQUEST_PARAMETER = ''

# # URLに対するトークンを取得
request = google.auth.transport.requests.Request()
target_audience = URL
id_token = google.oauth2.id_token.fetch_id_token(request, target_audience)

# GETリクエストにパラメーターを追加
payload = REQUEST_PARAMETER if REQUEST_PARAMETER else {}
headers = {'Authorization': 'Bearer {}'.format(id_token)}

response = requests.get(URL, headers=headers, params=payload)
response.raise_for_status()
print(response.text)
