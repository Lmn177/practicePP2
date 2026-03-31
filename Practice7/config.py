import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    # Определяем абсолютный путь к папке, где лежит этот файл (config.py)
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Соединяем путь папки с именем файла базы данных
    full_path = os.path.join(base_path, filename)

    parser = ConfigParser()
    parser.read(full_path)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {full_path} file')

    return config