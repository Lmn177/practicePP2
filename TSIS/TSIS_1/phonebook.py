import psycopg2
import json
import csv
import os
from config import host, user, password, db_name

# --- HELPER FUNCTIONS ---

def get_connection():
    try:
        return psycopg2.connect(host=host, user=user, password=password, database=db_name)
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def get_file_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

# --- IMPORT / EXPORT LOGIC ---
# (Тут твои функции import/export остаются без изменений)
def export_to_json(filename="contacts.json"):
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    try:
        cur.execute("SELECT c.name, c.email, c.birthday, g.name, array_agg(p.phone || ':' || p.type) FROM contacts c LEFT JOIN groups g ON c.group_id = g.id LEFT JOIN phones p ON c.id = p.contact_id GROUP BY c.id, g.name")
        data = [{"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4]} for r in cur.fetchall()]
        with open(get_file_path(filename), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"\n[!] Экспортировано в {filename}")
    finally:
        cur.close(); conn.close()

def import_from_json(filename="contacts.json"):
    path = get_file_path(filename)
    if not os.path.exists(path): print("Файл не найден."); return
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                cur.execute("DELETE FROM contacts WHERE name = %s", (item['name'],))
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id", (item['group'],))
                g_id = cur.fetchone()[0]
                cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id", (item['name'], item['email'], item['birthday'], g_id))
                c_id = cur.fetchone()[0]
                for p_entry in item.get('phones', []):
                    p_num, p_type = p_entry.split(':')
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (c_id, p_num, p_type))
        conn.commit()
    finally:
        cur.close(); conn.close()

def import_from_csv(filename="contacts.csv"):
    path = get_file_path(filename)
    if not os.path.exists(path):
        print(f"Файл не найден: {path}")
        return

    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Проверим, распознались ли заголовки
            if reader.fieldnames is None:
                print("Ошибка: Файл пуст или не содержит заголовков!")
                return
                
            for row in reader:
                # Вставка группы
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id", 
                            (row.get('group', 'Other'),))
                g_id = cur.fetchone()[0]

                # Вставка контакта
                cur.execute("""
                    INSERT INTO contacts (name, email, birthday, group_id) 
                    VALUES (%s, %s, %s, %s) 
                    ON CONFLICT (name) DO UPDATE 
                    SET email=EXCLUDED.email, birthday=EXCLUDED.birthday, group_id=EXCLUDED.group_id 
                    RETURNING id
                """, (row['name'], row.get('email'), row.get('birthday'), g_id))
                c_id = cur.fetchone()[0]

                # Вставка телефона
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                            (c_id, row.get('phone'), row.get('phone_type', 'mobile')))
        
        conn.commit()
        print("[!] Импорт из CSV прошел успешно.")
        
    except KeyError as e:
        print(f"Ошибка в структуре CSV: отсутствует столбец {e}")
        conn.rollback()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        conn.rollback()
    finally:
        cur.close(); conn.close()

# --- SEARCH & NAVIGATION ---

def browse_with_pagination():
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    limit, offset = 5, 0
    while True:
        cur.execute("SELECT c.name, c.email, g.name, c.birthday FROM contacts c LEFT JOIN groups g ON c.group_id = g.id ORDER BY c.name LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        print(f"\n--- Страница (Offset: {offset}) ---")
        for r in rows: print(f"[{r[2] or 'No Group'}] {r[0]} | Email: {r[1]} | Bday: {r[3]}")
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break
    cur.close(); conn.close()

def search_interface():
    query = input("\nВведите имя или телефон: ")
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for r in cur.fetchall(): print(f"Имя: {r[0]:<20} | Email: {r[1]:<20} | Телефон: {r[2]}")
    cur.close(); conn.close()

def advanced_search():
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    
    email_part = input("Часть email: ").strip()
    group_part = input("Название группы: ").strip()
    print("Сортировать по: 1. Имя, 2. Дата рождения, 3. Дата добавления")
    sort_choice = input("Выберите (1-3): ")
    
    sort_map = {'1': 'c.name', '2': 'c.birthday', '3': 'c.created_at'} # убедись, что поле даты создания существует
    sort_by = sort_map.get(sort_choice, 'c.name')

    # БАЗОВЫЙ ЗАПРОС
    query = """
        SELECT c.name, c.email, g.name, c.birthday 
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE 1=1
    """
    params = []

    # ДИНАМИЧЕСКИЕ ФИЛЬТРЫ
    if email_part:
        query += " AND c.email ILIKE %s"
        params.append(f"%{email_part}%")
        
    if group_part:
        query += " AND g.name ILIKE %s"
        params.append(f"%{group_part}%")

    query += f" ORDER BY {sort_by}"

    # ОТЛАДКА: Распечатает запрос прямо в консоль
    print(f"\n[DEBUG SQL]: {query}")
    print(f"[DEBUG PARAMS]: {params}")

    cur.execute(query, params)
    rows = cur.fetchall()

    if not rows:
        print("Ничего не найдено.")
    else:
        for r in rows:
            print(f"| {r[0]} | Email: {r[1]} | Группа: {r[2] or 'Без группы'} | ДР: {r[3]}")

    cur.close(); conn.close()

def main_menu():
    actions = {
        '1': browse_with_pagination,
        '2': search_interface,
        '3': export_to_json,
        '4': import_from_json,
        '5': import_from_csv,
        '6': advanced_search # Добавили новый пункт
    }
    while True:
        print("\n=== PHONEBOOK SYSTEM (PRACTICE 9) ===")
        print("1. Листать (Пагинация)\n2. Поиск\n3. Экспорт JSON\n4. Импорт JSON\n5. Импорт CSV\n6. Расширенный поиск\n0. Выход")
        choice = input("Выберите: ")
        if choice == '0': break
        if choice in actions: actions[choice]()
        else: print("Неверный выбор.")

if __name__ == "__main__":
    main_menu()