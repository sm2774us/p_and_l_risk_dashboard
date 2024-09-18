import pandas as pd
import psycopg2

def fetch_market_data():
    conn = psycopg2.connect(
        dbname="portfolio_db", user="user", password="password", host="localhost", port="5432"
    )
    query = "SELECT * FROM market_data;"
    data = pd.read_sql(query, conn)
    conn.close()
    return data
