CREATE OR REPLACE PROCEDURE upsert_contact(p_first_name VARCHAR, p_last_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    -- Мы ищем контакт по ИМЕНИ и ФАМИЛИИ (используем TRIM, чтобы убрать лишние пробелы)
    IF EXISTS (SELECT 1 FROM phonebook WHERE TRIM(first_name) = TRIM(p_first_name) AND TRIM(last_name) = TRIM(p_last_name)) THEN
        UPDATE phonebook 
        SET phone_number = p_phone 
        WHERE TRIM(first_name) = TRIM(p_first_name) AND TRIM(last_name) = TRIM(p_last_name);
        RAISE NOTICE 'Контакт % обновлен', p_first_name;
    ELSE
        -- Если такого сочетания Имя+Фамилия нет, создаем новый
        INSERT INTO phonebook (first_name, last_name, phone_number) 
        VALUES (p_first_name, p_last_name, p_phone);
        RAISE NOTICE 'Контакт % добавлен', p_first_name;
    END IF;
END;
$$;