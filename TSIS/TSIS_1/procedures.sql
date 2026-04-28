-- Добавление телефона к существующему контакту
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    VALUES ((SELECT id FROM contacts WHERE name = p_contact_name), p_phone, p_type);
END;
$$;

-- Перемещение в группу (с созданием если её нет)
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    g_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO g_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = g_id WHERE name = p_contact_name;
END;
$$;

-- Расширенный поиск
CREATE OR REPLACE FUNCTION search_contacts(search_val VARCHAR)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || search_val || '%' 
       OR c.email ILIKE '%' || search_val || '%'
       -- Если хочешь искать по телефону, нужно добавить JOIN с таблицей phones;
       -- но пока оставим этот вариант для простоты.
       ;
END;
$$ LANGUAGE plpgsql;