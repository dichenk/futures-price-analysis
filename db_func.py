import psycopg2
import time as tm
import os
from dotenv import load_dotenv


load_dotenv()
host = os.getenv('host')
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')
period = 3600

def check_prices():

    insert_query_b = f'''
        SELECT SUM(change_price) FROM BTCUSDT_FUTURE_PRICES
        WHERE time_check > {int(tm.time()) - period}
    '''
    insert_query_e = f'''
        SELECT SUM(change_price) FROM ETHUSDT_FUTURE_PRICES
        WHERE time_check > {int(tm.time()) - period}
    '''

    try:
        with psycopg2.connect(host=host, database=database, user=user, password=password, port=port) as con:
            with con.cursor() as cur:
                cur.execute(insert_query_b)
                result_b = cur.fetchone()[0]
                cur.execute(insert_query_e)
                result_e = cur.fetchone()[0]
                return result_b, result_e
    except psycopg2.Error as err:
        print(err)
        
def write_data(coin, price, time_check, change_price):

    data = (price, time_check, change_price)

    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {coin}_FUTURE_PRICES (
            price numeric(12, 5),
            time_check integer,
            change_price numeric(12, 5)
        )
    '''
    insert_query = f'''
        INSERT INTO {coin}_FUTURE_PRICES (price, time_check, change_price)
        VALUES (%s, %s, %s)
    '''

    try:
        with psycopg2.connect(host=host, database=database, user=user, password=password, port=port) as connection:
            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                cursor.execute(insert_query, data)
    except psycopg2.Error as err:
        print('Error connecting to database ', err)