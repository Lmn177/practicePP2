import psycopg2
from config import host, user, password, db_name

try:
    conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    print("Успешное подключение!")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")