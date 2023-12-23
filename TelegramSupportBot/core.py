import config
import datetime
import random
import sqlite3


# Добавить агента
def add_agent(agent_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"INSERT INTO agents (`agent_id`) VALUES ('{agent_id}')")
    con.commit()

    cur.close()
    con.close()

# Создать запрос
def new_req(user_id, request):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    # Добавить запрос в БД
    cur.execute(f"INSERT INTO requests (`user_id`, `req_status`) VALUES ('{user_id}', 'waiting')") 

    # Получить айди добавленного запроса
    req_id = cur.lastrowid

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    # Добавить сообщение для запроса
    cur.execute(f"INSERT INTO messages (`req_id`, `message`, `user_status`, `date`) VALUES ('{req_id}', '{request}', 'user', '{date_now}')")

    con.commit()

    cur.close()
    con.close()

    return req_id

# Добавить сообщение
def add_message(req_id, message, user_status):
    if user_status == 'user':
        req_status = 'waiting'
    elif user_status == 'agent':
        req_status = 'answered'

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    # Добавить сообщение для запроса
    cur.execute(f"INSERT INTO messages (`req_id`, `message`, `user_status`, `date`) VALUES ('{req_id}', '{message}', '{user_status}', '{date_now}')")
    
    # Изменить статус запроса
    cur.execute(f"UPDATE requests SET `req_status` = '{req_status}' WHERE `req_id` = '{req_id}'")
    
    con.commit()

    cur.close()
    con.close()

# Добавить пароли
def add_passwords(passwords):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    for password in passwords:
        cur.execute(f"INSERT INTO passwords (`password`) VALUES ('{password}')")
        
    con.commit()

    cur.close()
    con.close()

# Проверить статус агента
def check_agent_status(user_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT * FROM agents WHERE `agent_id` = '{user_id}'")
    agent = cur.fetchone()

    cur.close()
    con.close()

    if agent == None:
        return False
    else:
        return True

# Проверить валидность пароля
def valid_password(password):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT * FROM passwords WHERE `password` = '{password}'")
    password = cur.fetchone()

    cur.close()
    con.close()

    if password == None:
        return False
    else:
        return True

# Получить иконку статуса запроса
def get_icon_from_status(req_status, user_status):
    if req_status == 'confirm':
        return '✅'

    elif req_status == 'waiting':
        if user_status == 'user':
            return '⏳'
        elif user_status == 'agent':
            return '❗️'

    elif req_status == 'answered':
        if user_status == 'user':
            return '❗️'
        elif user_status == 'agent':
            return '⏳'            

# Сгенерировать пароли
def generate_passwords(number, lenght):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    passsords = []
    for _ in range(number):
        password = ''
        for _ in range(lenght):
            password += random.choice(chars)

        passsords.append(password)

    return passsords

# Получить юзер айди пользователя, создавшего запрос
def get_user_id_of_req(req_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `user_id` FROM requests WHERE `req_id` = '{req_id}'")
    user_id = cur.fetchone()[0]

    cur.close()
    con.close()

    return user_id

# Получить статус запроса
def get_req_status(req_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `req_status` FROM requests WHERE `req_id` = '{req_id}'")
    req_status = cur.fetchone()[0]

    cur.close()
    con.close()

    return req_status


# Удалить пароль
def delete_password(password):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("DELETE FROM passwords WHERE password = ?", (password,))
    con.commit()

    cur.close()
    con.close()


# Удалить агента
def delete_agent(agent_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute("DELETE FROM agents WHERE agent_id = ?", (agent_id,))
    con.commit()

    cur.close()
    con.close()


# Завершить запрос
def confirm_req(req_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"UPDATE requests SET `req_status` = 'confirm' WHERE `req_id` = '{req_id}'")
    con.commit()

    cur.close()
    con.close()

# Получить пароли с лимитом
def get_passwords(number):
    limit = (int(number) * 10) - 10

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `password` FROM passwords LIMIT {limit}, 10")
    passwords = cur.fetchall()

    cur.close()
    con.close()

    return passwords

# Получить агентов с лимитом
def get_agents(number):
    limit = (int(number) * 10) - 10

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `agent_id` FROM agents LIMIT {limit}, 10")
    agents = cur.fetchall()

    cur.close()
    con.close()

    return agents

# Получить мои запросы с лимитом
def my_reqs(number, user_id):
    limit = (int(number) * 10) - 10

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `req_id`, `req_status` FROM requests WHERE `user_id` = '{user_id}' ORDER BY `req_id` DESC LIMIT {limit}, 10")
    reqs = cur.fetchall()

    cur.close()
    con.close()

    return reqs

# Получить запросы по статусу с лимитом
def get_reqs(number, callback):
    limit = (int(number) * 10) - 10
    req_status = callback.replace('_reqs', '')

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `req_id`, `req_status` FROM requests WHERE `req_status` = '{req_status}' ORDER BY `req_id` DESC LIMIT {limit}, 10")
    reqs = cur.fetchall()

    cur.close()
    con.close()

    return reqs

# Получить историю запроса
def get_request_data(req_id, callback):
    if 'my_reqs' in callback:
        get_dialog_user_status = 'user'
    else:
        get_dialog_user_status = 'agent'

    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    cur.execute(f"SELECT `message`, `user_status`, `date` FROM messages WHERE `req_id` = '{req_id}'")
    messages = cur.fetchall()

    cur.close()
    con.close()

    data = []
    text = ''
    i = 1

    for message in messages:
        message_value = message[0]
        user_status = message[1]
        date = message[2] 

        if user_status == 'user':
            if get_dialog_user_status == 'user':
                text_status = '👤 Ваше сообщение'
            else:
                text_status = '👤 Сообщение пользователя'
        elif user_status == 'agent':
            text_status = '🧑‍💻 Агент поддержки'

        # Бэкап для текста
        backup_text = text
        text += f'{text_status}\n{date}\n{message_value}\n\n'

        # Если размер текста превышает допустимый в Telegram, то добавить первую часть текста и начать вторую
        if len(text) >= 4096:
            data.append(backup_text)
            text = f'{text_status}\n{date}\n{message_value}\n\n'

        # Если сейчас последняя итерация, то проверить не является ли часть текста превыщающий допустимый размер (4096 символов). Если превышает - добавить часть и начать следующую. Если нет - просто добавить последнюю часть списка.
        if len(messages) == i:
            if len(text) >= 4096:
                data.append(backup_text)
                text = f'{text_status}\n{date}\n{message_value}\n\n'
            
            data.append(text)

        i += 1

    return data

# Проверить статус последнего сообщения
def get_last_req(user_id):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    query = """
        SELECT req_id
        FROM requests
        WHERE user_id = ?
            AND req_status IN ('waiting', 'answered')
        ORDER BY req_id DESC
        LIMIT 1;
    """
    cur.execute(query, (user_id,))
    result = cur.fetchone()

    cur.close()
    con.close()

    return result

# Добавить в базу контактные сведения пользователя
def add_contacts(user_id, contact_info):
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    sql_query = "INSERT INTO contacts (user_id, user_contacts, date) VALUES (?, ?, ?)"
    data = (user_id, contact_info, date_now)

    cur.execute(sql_query, data)
    con.commit()

    cur.close()
    con.close()

# Получить из базы контактные сведения пользователей
def get_contacts():
    con = sqlite3.connect(config.SQLite)
    cur = con.cursor()

    sql_query = """
        SELECT c.user_id, c.user_contacts, c.date
        FROM contacts c
        INNER JOIN (
            SELECT user_id, MAX(date) AS max_date
            FROM contacts
            GROUP BY user_id
        ) sub ON c.user_id = sub.user_id AND c.date = sub.max_date
        """

    # Выполнение SQL-запроса
    cur.execute(sql_query)
    result = cur.fetchall()

    cur.close()
    con.close()

    return result
