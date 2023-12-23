import os
import sqlite3
import config


def create_table_agents():
    """
    Создает таблицу 'agents' в базе данных SQLite для хранения агентов.

    Таблица содержит следующие поля:
    - id: INTEGER, автоинкрементирующийся идентификатор записи
    - agent_id: VARCHAR(20), идентификатор агента

    """
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS agents(id INTEGER PRIMARY KEY AUTOINCREMENT, agent_id VARCHAR(20))")
    cur.execute("PRAGMA encoding='utf-8'")

    cur.close()
    con.close()


def create_table_passwords():
    """
    Создает таблицу 'passwords' в базе данных SQLite для хранения паролей.

    Таблица содержит следующие поля:
    - id: INTEGER, автоинкрементирующийся идентификатор записи
    - password: VARCHAR(20), пароль

    """
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY AUTOINCREMENT, password VARCHAR(20))")
    cur.execute("PRAGMA encoding='utf-8'")

    cur.close()
    con.close()

def create_table_requests():
    """
    Создает таблицу 'requests' в базе данных SQLite для хранения запросов.

    Таблица содержит следующие поля:
    - req_id: INTEGER, автоинкрементирующийся идентификатор запроса
    - user_id: VARCHAR(20), идентификатор пользователя
    - req_status: VARCHAR(20), статус запроса

    """
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS requests(req_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id VARCHAR(20), req_status VARCHAR(20))")
    cur.execute("PRAGMA encoding='utf-8'")

    cur.close()
    con.close()


def create_table_messages():
    """
    Создает таблицу 'messages' в базе данных SQLite для хранения сообщений.

    Таблица содержит следующие поля:
    - id: INTEGER, автоинкрементирующийся идентификатор записи
    - req_id: VARCHAR(20), идентификатор запроса
    - message: VARCHAR(4096), сообщение
    - user_status: VARCHAR(20), статус пользователя
    - date: VARCHAR(50), дата

    """
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, req_id VARCHAR(20), message VARCHAR(4096), user_status VARCHAR(20), date VARCHAR(50))")
    cur.execute("PRAGMA encoding='utf-8'")

    cur.close()
    con.close()

def create_table_contacts():
    """
    Создает таблицу 'contacts' в базе данных SQLite для хранения сообщений.

    Таблица содержит следующие поля:
    - id: INTEGER, автоинкрементирующийся идентификатор записи
    - user_id: VARCHAR(20), идентификатор пользователя
    - user_contacts: VARCHAR(1024), сведения о пользователе
    - date: VARCHAR(50), дата добавления
    """
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS contacts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(20),
                    user_contacts VARCHAR(1024),
                    date VARCHAR(50)
                )""")
    cur.execute("PRAGMA encoding='utf-8'")

    cur.close()
    con.close()


database_file = os.path.join(os.getcwd(), config.SQLite)
conn = sqlite3.connect(database_file)
conn.close()

create_table_agents()
create_table_passwords()
create_table_requests()
create_table_messages()
create_table_contacts()
