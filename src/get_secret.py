"""Secret Manager から情報を取得する"""

from google.cloud import secretmanager
import ast
import consts

SECRET_NAME = os.environ.get('SECRET_NAME')
SECRET_VARSION = os.environ.get('SECRET_VARSION')

client = secretmanager.SecretManagerServiceClient()
name = client.secret_version_path(consts.PROJECT_ID, SECRET_NAME, SECRET_VARSION)
print('target secret access path is {}'.format(name))
response = client.access_secret_version(request={'name': name})
data = response.payload.data.decode('UTF-8')

try:
    # 取得したSecretは文字列であるため、辞書に持ち換える
    dic = ast.literal_eval(data)
    for key, value in dic.items():
        print('key is {}, value is {}'.format(key, value))
    print('value_1 is {}'.format(dic['key1']))
    print('value_2 is {}'.format(dic['key2']))
    print('value_3 is {}'.format(dic['key3']))
except ValueError:
    # Secretが辞書形式でない場合は、文字列をそのまま表示する
    print('Secret is not dictionary!')
    print('Secret value is {}'.format(data))
except Exception:
    print('Can not convert because unexpected error!')