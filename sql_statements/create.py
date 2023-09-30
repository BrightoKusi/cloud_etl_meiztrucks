schema_name = 'raw_data'

# =============================================== FOR DEV SCHEMA
banks = '''CREATE TABLE IF NOT EXISTS raw_data.banks
(
    _id VARCHAR PRIMARY KEY NOT NULL ,
    code INTEGER,
    name VARCHAR
);'''


customers = '''CREATE TABLE IF NOT EXISTS raw_data.customers(

    id integer PRIMARY KEY NOT NULL,
    name character varying,
    email character varying,
    registered_at timestamp);'''

exchange_rates = '''CREATE TABLE IF NOT EXISTS raw_data.exchange_rates(
    date DATE,
    bank_id VARCHAR (50),
    rate NUMERIC (10,2));'''



items = '''CREATE TABLE IF NOT EXISTS raw_data.items(
id INTEGER,
name VARCHAR,
selling_price NUMERIC,
cost_price NUMERIC); '''

transactions = '''CREATE TABLE IF NOT EXISTS raw_data.transactions (
id BIGINT,
customer_id INTEGER,
item_id BIGINT,
date DATE,
bank_id VARCHAR,
qty INTEGER);'''


raw_data_tables = [banks, customers, exchange_rates, items, transactions]








transformed_schema = 'transformed_data'

# =============================================== FOR STAR SCHEMA

dim_banks = '''CREATE TABLE IF NOT EXISTS staging.dim_banks
(
    _id VARCHAR PRIMARY KEY NOT NULL ,
    code INTEGER,
    name VARCHAR
);'''

dim_customers = '''CREATE TABLE IF NOT EXISTS staging.dim_customers(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR,
    email VARCHAR,
    registered_at TIMESTAMP,
    registeration_hour INTEGER );'''


dim_items = '''CREATE TABLE IF NOT EXISTS staging.dim_items(
id INTEGER,
name VARCHAR,
selling_price NUMERIC,
cost_price NUMERIC); '''



dim_dates = '''CREATE TABLE IF NOT EXISTS staging.dim_dates(
    date DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER
);'''

ft_transactions = '''CREATE TABLE IF NOT EXISTS staging.ft_transactions(
    id INTEGER PRIMARY KEY NOT NULL,
    item_id INTEGER,
    customer_id INTEGER,
    bank_id  VARCHAR,
    selling_price NUMERIC,
    cost_price NUMERIC,
    qty INTEGER,
    exchange_rate INTEGER,
    transaction_date DATE,
    month INTEGER,
    quarter INTEGER,
    monthly_gains INTEGER,
    quarterly_gains INTEGER,
    monthly_loss INTEGER,
    quarterly_loss INTEGER
);'''


dev_tables = [banks, customers, exchange_rates, items, transactions]
transformed_tables = [dim_banks, dim_customers, dim_dates, dim_items, ft_transactions]