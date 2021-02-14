"""ファイルを比較し差分があるかどうかを判定する"""

import consts
import logging
import os
import subprocess
import sys

DESTINATION_BUCKET_1 = consts.PROJECT_ID + '-csv-bucket'
DESTINATION_BUCKET_2 = consts.PROJECT_ID + '-csv-bucket' + '/backup'

# ログを指定ファイルに出力する
logging.basicConfig(filename='src/logger.log', level=logging.DEBUG)

# files = ['test_1.txt', 'test_2.txt']
files = ['test_1.txt']

for file in files:
    # ファイルをローカルにコピーする
    command = 'gsutil cp gs://{0}/{1} /tmp/diff/{1}'.format(DESTINATION_BUCKET_1, file)
    ret = subprocess.run(command.split())

    # 比較対象ファイルをローカルにコピーする
    command = 'gsutil cp gs://{0}/{1} /tmp/diff/backup_{1}'.format(DESTINATION_BUCKET_2, file)
    ret = subprocess.run(command.split())

    # 比較対象ファイルを取得できたかどうかチェックする
    if not os.path.isfile(f'/tmp/diff/backup_{file}'):
        # return kwargs['templates_dict']['next_task_ids_when_diff']
        logging.info('比較対象ファイルを取得できない')

    # ファイルを比較する
    command = 'diff /tmp/diff/{0} /tmp/diff/backup_{0}'.format(file)
    ret = subprocess.run(command.split(), stdout=subprocess.PIPE)
    output = ret.stdout
    # 結果を行ごとにリストにする。
    lines = output.splitlines()

    # TODO:ここまでの処理でエラーが起きたら場合でも削除できるようにする
    # ローカルファイルを削除する。
    command = 'rm -f /tmp/diff/{0}'.format(file)
    ret = subprocess.run(command.split())
    command = 'rm -f /tmp/diff/backup_{0}'.format(file)
    ret = subprocess.run(command.split())

    # 差分ありのファイルがある（差分リストの中身が存在する）時点で後続処理を実行する
    if lines:
        logging.info('diff length: %s', len(lines))
        # return kwargs['templates_dict']['next_task_ids_when_diff']
        logging.info('%s に差分が存在するため終了', file)
        sys.exit()
    logging.info('%s に差分が存在しないため続行', file)
    continue

# 全てのファイルに差分がない場合は後続処理を実行しない
# return kwargs['templates_dict']['next_task_ids_when_no_diff']
logging.info('差分ありのファイルが存在しない')
