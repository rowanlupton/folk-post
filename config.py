import os
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['secret_key']
DB_NAME = 'folk-post'


# MONGO_URI = 'mongodb://folk-post:'+os.environ['mongodb-password']+'@folk-post-shard-00-00-jwcpw.mongodb.net:27017,folk-post-shard-00-01-jwcpw.mongodb.net:27017,folk-post-shard-00-02-jwcpw.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=folk-post-shard-0&authSource=admin'
MONGO_DBNAME = 'folk-post'