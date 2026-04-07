def load_config():
    # Здесь мы указываем параметры подключения
    # Раз у тебя "trust", пароль можно оставить пустым или вообще убрать
    return {
        "host": "localhost",
        "database": "postgres", # Проверь имя своей базы в pgAdmin!
        "user": "postgres",
        "password": "",         # Для режима trust оставляем пустым
        "port": 5432
    }