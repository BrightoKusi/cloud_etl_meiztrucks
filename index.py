import configparser
import redshift_connector
import boto3
import pandas as pd
import psycopg2 
import logging

from sqlalchemy import create_engine
from utils.helper import create_bucket
from sql_statements.create import dev_tables, transformed_tables
from sql_statements.transform import transformation_queries

s3_path = 's3://{}/{}.csv'

config  = configparser.ConfigParser()
config.read('.env')

access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']
bucket_name = config['AWS']['bucket_name']
region = config['AWS']['region']
arn = config['AWS']['arn']

db_host = config['DB_CONN']['host']
db_user = config['DB_CONN']['user']
db_password = config['DB_CONN']['password']
db_database = config['DB_CONN']['database']

dwh_host = config['DWH_CONN']['host']
dwh_user = config['DWH_CONN']['username']
dwh_password = config['DWH_CONN']['password']
dwh_database = config['DWH_CONN']['database']



# FETCH DATA FROM POSTGRES TO S3 BUCKET DATA LAKE USING PANDAS AND BOTO3

# # 1. Create bucke
create_bucket(access_key, secret_key, bucket_name, region)

db_tables = ['banks', 'customers', 'exchange_rates', 'items', 'transactions']


# 2. Create slqalchemy connection
conn = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_database}")
print('connection successful')


# # 3. Fetch data from postgresql to s3 bucket (Data Lake)
db_tables = ['banks', 'customers', 'exchange_rates', 'items', 'transactions']

for table in db_tables:
    query = f'SELECT * FROM {table}'
    df = pd.read_sql_query(query, conn)

    df.to_csv(
        s3_path.format(bucket_name, table)
        , index=False
        , storage_options={
            'key': access_key
            , 'secret': secret_key
        })
print('done')


#MOVE DATA FROM DATA LAKE TO DATA WAREHOUSE (REDSHIFT CLUSTER)

# Step 4: Create connection to redshift
dwh_conn = redshift_connector.connect(
    host= dwh_host,
    database=dwh_database,
    user= dwh_user,
    password=dwh_password
 )
print('dwh_connection established')

cursor = dwh_conn.cursor()


# Step 5. Create the dev schema
dev_schema = 'raw_data'
cursor.execute(f'CREATE SCHEMA {dev_schema};')
dwh_conn.commit()


# Step 6. create similar database tables in dev_schema as data lake
for query in dev_tables:
    print(f'================ {query[:300]}')
    cursor.execute(query)
    dwh_conn.commit()
print('done')

 
#Step 7. Copy data from datalake to redshift cluster 
for table in db_tables:
    query = f'''
        copy {dev_schema}.{table} 
        from '{s3_path.format(bucket_name, table)}'
        iam_role '{arn}'
        delimiter ','
        ignoreheader 1;
    '''
    cursor.execute(query)
    dwh_conn.commit()
print('done')



# ---Step 8. Create staging schema for the star schema
staging_schema = 'staging'
create_staging_schema_query = f'''CREATE SCHEMA {staging_schema};'''
cursor.execute(create_staging_schema_query)
dwh_conn.commit()

# ---Step 9. Create the star schema tables
for query in transformed_tables:
    print(f'================ {query[:2000]}')
    cursor.execute(query)
    dwh_conn.commit()

# ---Step 10. Excute queries and load data into star schema tables
for query in transformation_queries:
    print(f'''------------- {query[:4000]}''')
    cursor.execute(query)
    dwh_conn.commit()

cursor.close()
dwh_conn.close()