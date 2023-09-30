# cloud_etl_meiztrucks
cloud_etl_meiztrucks

ABOUT THE BUSINESS
Meiz Trucks is a corporate trucks dealer with its head office in the United States. 
They sell trucks of different makes and models to resellers and final users located in Nigeria.
The trucks are valued in the company’s local currency(USD), but are sold in the customer’s local currency.

Meiz Trucks Possible Business Questions
Q1. The exchange rate that was applied to a particular item purchase.
Q2. Monthly and Quarterly gains and losses
Q3. Items with the most purchases
Q4. Hour of day of the most registration
Q5. Number of Zero (0) exchange rates per bank
These questions are to guide you through developing a scalable Data Warehousing system for the
business

Tools and Dependencies
- AWS [BOTO3, s3 bucket(Data Lake), redshift cluster(Data Warehouse)]
- Pandas
- Python
- Postgresql
- Psycopg2 
- Redshift_connector


Outcome
Data was extracted from postgresql and stored in a data lake. A warehouse was formed and data was copied to two schemas: raw_data and transformed_data(star schema)

