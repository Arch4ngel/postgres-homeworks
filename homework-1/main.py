"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
import os


def read_csv(filepath):
    """Функция для получения данных из CSV"""
    csv_data = []
    with open(os.path.join(os.path.dirname(__file__),
                           f'{filepath}'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            csv_data.append(i)
    return csv_data


postgres_pass = os.getenv('POSTGRES_KEY')

with psycopg2.connect(host="localhost", database="north", user="postgres", password=postgres_pass) as conn:
    with conn.cursor() as cur:
        for row in read_csv('north_data/employees_data.csv'):
            cur.execute(f"INSERT INTO employees VALUES({int(row['employee_id'])}, '{row['first_name']}', "
                        f"'{row['last_name']}', '{row['title']}', "
                        f"'{row['birth_date']}', '{row['notes']}');")
        for row in read_csv('north_data/customers_data.csv'):
            quotes = '\''
            cur.execute(f"INSERT INTO customers VALUES('{row['customer_id']}', "
                        f"'{row['company_name'].replace(quotes, '')}', "
                        f"'{row['contact_name']}');")
        for row in read_csv('north_data/orders_data.csv'):
            cur.execute(f"INSERT INTO orders VALUES({int(row['order_id'])}, '{row['customer_id']}', "
                        f"{int(row['employee_id'])}, '{row['order_date']}',"
                        f"'{row['ship_city']}');")
