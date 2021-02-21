"""SFTPでリモートサーバからローカルにファイルを取得しGCSに移動する"""

import os
import paramiko
import sys
import subprocess
from datetime import datetime, timedelta
from google.cloud import secretmanager, storage
import consts

# SecretManager情報を環境変数から取得する
SECRET_NAME = os.environ.get('secret_name') #シークレット名
SECRET_VARSION = os.environ.get('secret_version') #バージョン

# SFTP接続先情報を環境変数から取得する
HOST = os.environ.get('SFTP_HOST') #IPアドレス
PORT = os.environ.get('SFTP_PORT') #ポート
USER = os.environ.get('SFTP_USERNAME') #ユーザ名

# ファイル情報
FILE_NAME = 'test.txt' #取得するファイル名称
REMOTE_PATH = '/home/ubuntu/' #ダウンロード対象パス
LOCAL_PATH = '/tmp/' #ダウンロードするローカルパス
DESTINATION_BUCKET = consts.PROJECT_ID + '-csv-bucket' #アップロードするGCSパス
DIRECTORY_NAME = 'test/'

MAX_TRY_NUM = 3

# 昨日日付を取得する
today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_str = datetime.strftime(yesterday, '%Y%m%d')
print("Yesterday is {}".format(yesterday_str))

# SFTP接続パスワードをSecretManagerから取得する
secret_manager_client = secretmanager.SecretManagerServiceClient()
name = secret_manager_client.secret_version_path(consts.PROJECT_ID, SECRET_NAME, SECRET_VARSION)
response = secret_manager_client.access_secret_version(request={"name": name})
password = response.payload.data.decode('UTF-8')

# SFTPで昨日日付のファイルを取得する
sftp_client = paramiko.SSHClient()
sftp_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
sftp_client.connect(HOST, port=PORT, username=USER, password=password)
for i in range(1, MAX_TRY_NUM + 1):
    try:
        print("connect {}th started...".format(i))
        sftp_connection = sftp_client.open_sftp()
        sftp_connection.get(REMOTE_PATH + FILE_NAME + '.' + yesterday_str, LOCAL_PATH + FILE_NAME)
    # TODO:例外内容によって処理を変える
    except Exception as e:
        print("connect {}th failed!({}/{}) {}".format(i, i, MAX_TRY_NUM, e))
    # 失敗しなかった時はループを抜ける
    else:
        print("Successfully get {} from {}!".format(REMOTE_PATH + FILE_NAME + '.' + yesterday_str, HOST))
        break
else:
    sftp_client.close()
    print("Connect all failed!")
    sys.exit()

# GCSへアップロードする前に行う処理をここに記述する
# command = 'gsutil mv {0} gs://{1}/test/'.format(LOCAL_PATH, DESTINATION_BUCKET)
# ret = subprocess.run(command.split())

# # ローカルからGCSへファイルをコピーする
storage_client = storage.Client()
bucket = storage_client.bucket(DESTINATION_BUCKET)
blob = bucket.blob(DIRECTORY_NAME + FILE_NAME)
for i in range(1, MAX_TRY_NUM + 1):
    try:
        print("upload {}th started...".format(i))
        blob.upload_from_filename(LOCAL_PATH + FILE_NAME)
    except Exception as e:
        print("upload {}th failed!({}/{}) {}".format(i, i, MAX_TRY_NUM, e))
    # 失敗しなかった時はループを抜ける
    else:
        print(
            'Successfully upload {} to {}.'.format(
                LOCAL_PATH + FILE_NAME, DESTINATION_BUCKET + '/' + DIRECTORY_NAME + FILE_NAME
            )
        )
        break
else:
    print("Upload all failed!")
    sys.exit()

# # ローカルからファイルを削除する
os.remove(LOCAL_PATH + FILE_NAME)
print('File {} deleted.'.format(LOCAL_PATH + FILE_NAME))
