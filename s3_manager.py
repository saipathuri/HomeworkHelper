import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import pickle

access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', None)
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

conn = S3Connection(access_key_id, secret_access_key)
bucket = conn.get_bucket('elasticbeanstalk-us-west-2-404441904824')
k = Key(bucket)
k.key = 'data'

def save(data_to_save):
	pickle.dump(data_to_save, open('/tmp/save.p', 'wb'))
	k.set_contents_from_file(open('/tmp/save.p', 'rb'))
	print('saved data to s3')

def load():
	k.get_contents_to_filename('/tmp/save.p')
	data = pickle.load(open('/tmp/save.p', 'rb'))
	print('loaded data from s3')
	return data