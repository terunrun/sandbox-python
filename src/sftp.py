"""SFTPでリモートサーバからローカルにファイルを取得しGCSに移動する"""

import consts
import os
import paramiko
import subprocess

# SFTP接続先の設定
HOST = '接続先IPアドレス'
PORT = 22
USER = 'ユーザ名'
PASSWORD = 'パスワード'
REMOTE_PATH = 'ダウンロード対象パス'
LOCAL_PATH = 'ダウンロードするローカルパス'
DESTINATION_BUCKET = 'アップロードするGCSパス'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(HOST, port=PORT, username=USER, password=PASSWORD)
try:
    sftp_connection = client.open_sftp()
    sftp_connection.get(REMOTE_PATH, LOCAL_PATH)
finally:
    client.close()

# TODO:リトライ設定を実装する
# or
# google-cloud-storageパッケージを使用する
command = 'gsutil mv {0} gs://{1}/test/'.format(LOCAL_PATH, DESTINATION_BUCKET)
ret = subprocess.run(command.split())
