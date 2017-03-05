import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os

access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', None)
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

conn = S3Connection(access_key_id, secret_access_key)
bucket = conn.get_bucket('elasticbeanstalk-us-west-2-404441904824')
k = Key(bucket)
k.key = 'QuotesJson.txt'

def load():
	k.get_contents_to_filename('json.txt')