import psycopg2
from config import load_config

def connect():
    """ Подключение к серверу PostgreSQL """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            print('Успешное подключение к базе данных PostgreSQL!')
            return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка подключения: {error}")

if __name__ == '__main__':
    connect()