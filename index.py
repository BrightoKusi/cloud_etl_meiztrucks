import configparser
config  = configparser.ConfigParser()
config.read('.env')
import boto3
import pandas as pd
import psycopg2 
import logging
from sqlalchemy import create_engine
from utils.helper import create_s3_bucket
#from sql_statements.create import db_tables

s3_path = 's3://{}/{}.csv'

access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']
bucket_name = config['AWS']['bucket_name']
region = config['AWS']['region']
role = config['AWS']['arn']

db_host = config['DB_CONN']['host']
db_user = config['DB_CONN']['user']
db_password = config['DB_CONN']['password']
db_database = config['DB_CONN']['database']



# FETCH DATA FROM POSTGRES TO S3 BUCKET DATA LAKE USING PANDAS AND BOTO3

# 1. Create bucket
create_s3_bucket(access_key, secret_key, bucket_name, region)


# 2. Create slqalchemy connection
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_database}")
print('connection successful')


# 3. Fetch data from postgresql to s3 bucket (Data Lake)
db_tables = ['banks', 'customers', 'exchange_rates', 'items', 'transactions']
for table in db_tables:
    query = f''' SELECT * FROM {table}'''
    logging.info(f'===========Executing {query}')
    df = pd.read_sql_query(query, engine)

    df.to_csv(
        s3_path.format(bucket_name, table)
        , index=False
        , storage_options={
            'key': access_key
            , 'secret': secret_key
        }
 )


# MOVE DATA FROM DATA LAKE TO DATA WAREHOUSE (REDSHIFT CLUSTER)


