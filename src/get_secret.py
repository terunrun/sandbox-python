'''Secret Manager から情報を取得する'''

from google.cloud import secretmanager
import consts

SECRET_NAME = 'test_secret'
SECRET_VARSION = '1'

client = secretmanager.SecretManagerServiceClient()
name = client.secret_version_path(consts.PROJECT_ID, SECRET_NAME, SECRET_VARSION)
print('target secret access path is {}'.format(name))
response = client.access_secret_version(request={"name": name})

print('secret is {}'.format(response.payload.data.decode('UTF-8')))
