
dim_banks = '''
    INSERT INTO staging.dim_banks(
    bank_id
    , code
    , name
    )
    SELECT b._id, b.code, b.name FROM raw_data.banks b;
'''

dim_customers = '''
    INSERT INTO staging.dim_customers(
    customer_id
    ,name
    ,email
    ,registered_at
    ,registeration_hour
)
    SELECT c.id, c.name, c.email, c.registered_at, extract(HOUR from c.registered_at) From raw_data.customers c;
'''

dim_items = '''
INSERT INTO staging.dim_items(
    customer_id
    ,name
    ,selling_price
    ,cost_price
)
    SELECT i.id , i.name, i.selling_price, i.cost_price FROM raw_data.items i;
'''

dim_dates = '''
    INSERT INTO staging.dim_dates (
        date
        , year
        , month
        , quarter
    )
    SELECT t.date, EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date), EXTRACT(QUARTER FROM t.date) FROM raw_data.transactions t;
'''

ft_transactions = '''
INSERT INTO staging.ft_transactions
(
    item_id
    ,customer_id
    ,bank_id
    ,selling_price
    ,cost_price
    ,qty
    ,exchange_rate
    ,transaction_date
)
    SELECT t.id, t.item_id, t.customer_id, t.bank_id, i.selling_price, i.cost_price, t.date, t.qty, 
    e.rate, t.date, EXTRACT(MONTH FROM t.date), EXTRACT(QUARTER FROM t.date), NULL, NULL, NULL, NULL
    FROM raw_data.transactions t
        LEFT JOIN raw_data.items i 
            ON t.item_id = i.id
        LEFT JOIN raw_data.exchange_rates e 
            ON t.bank_id = e.bank_id;
'''

transformation_queries = [dim_dates, dim_banks, dim_customers, dim_items, ft_transactions]

