"""gcsバケットに指定名称のオブジェクトがあるか？"""

from google.cloud import storage
import consts
import pprint

BUCKET_NAME = consts.PROJECT_ID + '-csv-bucket'
# get list

client = storage.Client()

bucket = client.get_bucket(BUCKET_NAME)
blob = bucket.get_blob('test.txt')
if blob:
    pprint.pprint('blobs!!!!')
    pprint.pprint(vars(blob))
blobs = bucket.list_blobs()
for obj in blobs:
    pprint.pprint('-------->')
    pprint.pprint(vars(obj))
    # get
    blob = bucket.get_blob(obj.name)
    pprint.pprint('\t-------->')
    pprint.pprint(vars(blob))
