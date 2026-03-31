import psycopg2
import csv
from config import load_config

# --- 1. Функция создания таблицы ---
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone_number VARCHAR(20) UNIQUE NOT NULL
    );
    """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

# --- 2. Функция добавления контакта вручную ---
def add_contact(f_name, l_name, phone):
    sql = "INSERT INTO phonebook(first_name, last_name, phone_number) VALUES(%s, %s, %s)"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f_name, l_name, phone))
                conn.commit()
                print(f"Контакт {f_name} успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")

# --- 3. Функция импорта из CSV ---
def import_from_csv(file_path):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute(
                            "INSERT INTO phonebook (first_name, last_name, phone_number) "
                            "VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING",
                            (row['first_name'], row['last_name'], row['phone_number'])
                        )
                conn.commit()
                print("Данные из CSV успешно импортированы!")
    except Exception as e:
        print(f"Ошибка при импорте CSV: {e}")

# --- 4. Функция поиска ---
def search_contacts(name_query):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s OR last_name LIKE %s", 
                            (f'%{name_query}%', f'%{name_query}%'))
                rows = cur.fetchall()
                if not rows:
                    print("Ничего не найдено.")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Ошибка поиска: {e}")

# --- 5. Функция удаления ---
def delete_contact(phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
                conn.commit()
                print(f"Контакт с номером {phone} удален.")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")

def get_all_contacts():
    """ Выводит весь список контактов из базы данных """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # 1. Выполняем запрос на выборку всех данных
                cur.execute("SELECT id, first_name, last_name, phone_number FROM phonebook ORDER BY id")
                
                # 2. Получаем все строки
                rows = cur.fetchall()
                
                # 3. Проверяем, есть ли данные
                if not rows:
                    print("\nСписок контактов пуст.")
                    return

                print("\n--- Список всех контактов ---")
                # Печатаем заголовок для красоты
                print(f"{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Телефон':<15}")
                print("-" * 55)
                
                # 4. Проходим циклом по каждой строке и выводим
                for row in rows:
                    # row - это кортеж (id, name, surname, phone)
                    print(f"{row[0]:<5} {row[1]:<15} {row[2] if row[2] else '':<15} {row[3]:<15}")
                
                print("-" * 55)
                print(f"Всего найдено записей: {len(rows)}")

    except Exception as e:
        print(f"Ошибка при получении списка: {e}")

# --- ГЛАВНОЕ МЕНЮ (ОБЪЕДИНЕНИЕ) ---
def main():
    create_table() 
    
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Добавить контакт вручную")
        print("2. Импортировать из CSV")
        print("3. Показать все контакты")  # <-- НОВЫЙ ПУНКТ
        print("4. Поиск по имени/фамилии")
        print("5. Удалить по номеру телефона")
        print("6. Выход")
        
        choice = input("Выберите действие (1-6): ")
        
        if choice == '1':
            fn = input("Имя: ")
            ln = input("Фамилия: ")
            ph = input("Телефон: ")
            add_contact(fn, ln, ph)
            
        elif choice == '2':
            import_from_csv('Practice7/contacts.csv') 
            
        elif choice == '3':
            get_all_contacts()  # <-- ВЫЗОВ НОВОЙ ФУНКЦИИ
            
        elif choice == '4':
            q = input("Введите имя для поиска: ")
            search_contacts(q)
            
        elif choice == '5':
            p = input("Введите номер телефона для удаления: ")
            delete_contact(p)
            
        elif choice == '6':
            print("До свидания!")
            break
if __name__ == '__main__':
    main()