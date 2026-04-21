import psycopg2
from config import load_config

# 1
def search_contacts(pattern):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s::varchar, %s::varchar, %s::varchar)", (f_name, l_name, phone))
                rows = cur.fetchall()
                if not rows:
                    print("Ничего не найдено.")
                else:
                    print(f"\n{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Телефон':<15}")
                    print("-" * 55)
                    for row in rows:
                        print(f"{row[0]:<5} {row[1]:<15} {row[2] if row[2] else '':<15} {row[3]:<15}")
    except Exception as e:
        print(f"Ошибка поиска: {e}")

#  2. 
def upsert_contact(f_name, l_name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s, %s)", (f_name, l_name, phone))
                conn.commit()
                print(f"Контакт {f_name} успешно обработан (добавлен/обновлен).")
    except Exception as e:
        print(f"Ошибка при выполнении upsert: {e}")

# 3
def get_paginated(limit, offset):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()
                print(f"\n--- Страница (Limit: {limit}, Offset: {offset}) ---")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Ошибка пагинации: {e}")

# 4 
def delete_contact(search_val):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact_v2(%s)", (search_val,))
                conn.commit()
                print(f"Запись с параметром '{search_val}' удалена.")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")

# --- ГЛАВНОЕ МЕНЮ ---
def main():
    while True:
        print("\n--- PhoneBook Practice 8 (PostgreSQL Procs) ---")
        print("1. Добавить или Обновить контакт (Upsert)")
        print("2. Поиск по имени/фамилии/телефону")
        print("3. Показать список с пагинацией")
        print("4. Удалить контакт (по имени или номеру)")
        print("5. Выход")
        
        choice = input("Выберите действие (1-5): ")
        
        if choice == '1':
            fn = input("Имя: ")
            ln = input("Фамилия: ")
            ph = input("Телефон: ")
            upsert_contact(fn, ln, ph)
            
        elif choice == '2':
            q = input("Введите текст для поиска: ")
            search_contacts(q)
            
        elif choice == '3':
            try:
                l = int(input("Сколько записей показать? (Limit): "))
                o = int(input("Сколько пропустить? (Offset): "))
                get_paginated(l, o)
            except ValueError:
                print("Введите числовые значения!")
            
        elif choice == '4':
            p = input("Введите имя или номер телефона для удаления: ")
            delete_contact(p)
            
        elif choice == '5':
            print("Работа завершена.")
            break

if __name__ == '__main__':
    main()