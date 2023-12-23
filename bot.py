import config
import sql
import core
import telebot
import random
import datetime
import markup
import sys
from telebot import apihelper

if config.PROXY_URL:
    apihelper.proxy = {'https': config.PROXY_URL}

bot = telebot.TeleBot(config.TOKEN, skip_pending=True)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '👋🏻 Привет! Это бот для бла-бла-бла.\nМы хотим предложить ... .Если у тебя останутся вопросы, нажми <b>Поболтать со специалистом</b> и наши сотрудники в скором времени тебе ответят! \nЕсли тебе все подходит, нажми <b>Оставить свои контакты</b>', parse_mode='html', reply_markup=markup.markup_main())


@bot.message_handler(commands=['agent'])
def agent(message):
    user_id = message.from_user.id

    if core.check_agent_status(user_id) == True: 
        bot.send_message(message.chat.id, '🔑 Вы авторизованы как Агент поддержки', parse_mode='html', reply_markup=markup.markup_agent())

    else:
        take_password_message = bot.send_message(message.chat.id, '⚠️ Тебя нет в базе. Отправь одноразовый пароль доступа.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(take_password_message, get_password_message)


@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.from_user.id

    if str(user_id) == config.ADMIN_ID:
        bot.send_message(message.chat.id, '🔑 Вы авторизованы как Админ', reply_markup=markup.markup_admin())
    else:
        bot.send_message(message.chat.id, '🚫 Эта команда доступна только администратору.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = message.from_user.id
    req_id = core.get_last_req(user_id)

    if message.text == '✏️ Поболтать со специалистом':
        if req_id is None:
            take_new_request = bot.send_message(message.chat.id, 'Введите свое сообщение и наши сотрудники скоро Вам ответят.', reply_markup=markup.markup_cancel())
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.register_next_step_handler(take_new_request, get_new_request)
        else:
            req_id = req_id[0]
            take_additional_message = bot.send_message(message.chat.id, 'Введите свое сообщение и наши сотрудники скоро Вам ответят.', reply_markup=markup.markup_cancel())
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.register_next_step_handler(take_additional_message, get_additional_message, req_id, 'user')
    elif message.text == '✉️ Оставить свои контакты':
        take_contacts = bot.send_message(message.chat.id, 'Для связи оставьте нам ссылку в телеграмме, номер телефона или какую-нибудь другую социальную сеть. Можете указать удобное для Вас время или другие пожелания. Спасибо!', reply_markup=markup.markup_cancel())
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(take_contacts, get_contacts)
    else:
        bot.send_message(message.chat.id, 'Вы возвращены в главное меню. Если хотите написать сообщение, пожалуйста, нажмите <b>Поболтать со специалистом</b> и отправьте своё сообщение через эту форму.', parse_mode='html', reply_markup=markup.markup_main())


def get_password_message(message):
    password = message.text
    user_id = message.from_user.id

    if password == None:
        send_message = bot.send_message(message.chat.id, '⚠️ Вы отправляете не текст. Попробуйте еще раз.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send_message, get_password_message)

    elif password.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено.', reply_markup=markup.markup_main())
        return

    elif core.valid_password(password) == True:
        core.delete_password(password)
        core.add_agent(user_id)

        bot.send_message(message.chat.id, '🔑 Вы авторизованы как Агент поддержки', parse_mode='html', reply_markup=markup.markup_main())
        bot.send_message(message.chat.id, 'Выберите раздел технической панели:', parse_mode='html', reply_markup=markup.markup_agent())

    else:
        send_message = bot.send_message(message.chat.id, '⚠️ Неверный пароль. Попробуй ещё раз.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(send_message, get_password_message)


def get_agent_id_message(message):
    agent_id = message.text

    if agent_id == None:
        take_agent_id_message = bot.send_message(message.chat.id, '⚠️ Вы отправляете не текст. Попробуйте еще раз.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(take_agent_id_message, get_agent_id_message)

    elif agent_id.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено.', reply_markup=markup.markup_main())
        return

    else:
        core.add_agent(agent_id)
        bot.send_message(message.chat.id, '✅ Агент успешно добавлен.', reply_markup=markup.markup_main())
        bot.send_message(message.chat.id, 'Выберите раздел админ панели:', reply_markup=markup.markup_admin())


def get_new_request(message):
    request = message.text
    user_id = message.from_user.id

    if request is None:
        take_new_request = bot.send_message(message.chat.id, '⚠️ Отправляемый вами тип данных не поддерживается в боте.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(take_new_request, get_new_request)

    elif request.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено.', reply_markup=markup.markup_main())
        return

    else:
        req_id = core.new_req(user_id, request)
        bot.send_message(message.chat.id, '✅ Ваше сообщение успешно отправлено!', parse_mode='html', reply_markup=markup.markup_main())

def get_contacts(message):
    request = message.text
    user_id = message.from_user.id
    if request:
        core.add_contacts(user_id, request)
        bot.send_message(message.chat.id, 'Спасибо! Мы свяжемся с Вами в ближайшее время.', parse_mode='html', reply_markup=markup.markup_main())
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так..(\nПовторите заново.', parse_mode='html', reply_markup=markup.markup_main())

def get_additional_message(message, req_id, status):
    additional_message = message.text

    if additional_message == None:
        take_additional_message = bot.send_message(chat_id=message.chat.id, text='⚠️ Отправляемый вами тип данных не поддерживается в боте.', reply_markup=markup.markup_cancel())

        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(take_additional_message, get_additional_message, req_id, status)

    elif additional_message.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено.', reply_markup=markup.markup_main())
        return

    else:
        if additional_message != 'None':
            core.add_message(req_id, additional_message, status)

        text = '✅ Ваше сообщение успешно отправлено!'

        bot.send_message(message.chat.id, text, reply_markup=markup.markup_main())

        if status == 'agent':
            user_id = core.get_user_id_of_req(req_id)

            if additional_message == 'None':
                additional_message = ''
            bot.send_message(user_id, f'⚠️ Получен новый ответ на ваш запрос!\n\n🧑‍💻 Ответ агента поддержки:\n{additional_message}', reply_markup=markup.markup_main())
        
        elif status == 'user':
            agents = core.get_agents_all()

            for agent in agents:
                agent_id = int(agent[0])
                bot.send_message(agent_id, '⚠️ Получен запрос от пользователя, пожалуйста проверьте!', reply_markup=markup.markup_agent())

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.message.chat.id

    if call.message:
        if ('my_reqs:' in call.data) or ('waiting_reqs:' in call.data) or ('answered_reqs:' in call.data) or ('confirm_reqs:' in call.data):
            # Обработчик кнопок для:
            # ❗️ Ожидают ответа от поддержки
            # ⏳ Ожидают ответа от пользователя
            # ✅ Завершенные запросы

            parts = call.data.split(':')
            callback = parts[0]
            number = parts[1]
            markup_and_value = markup.markup_reqs(user_id, callback, number)
            markup_req = markup_and_value[0]
            value = markup_and_value[1]

            if value == 0:
                bot.send_message(chat_id=call.message.chat.id, text='⚠️ Запросы не обнаружены.', reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)
                return

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Нажмите на запрос, чтобы посмотреть историю переписки, либо добавить сообщение:', reply_markup=markup_req)
            except:
                bot.send_message(chat_id=call.message.chat.id, text='Ваши запросы:', reply_markup=markup_req)

            bot.answer_callback_query(call.id)

        #Открыть запрос
        elif 'open_req:' in call.data:
            parts = call.data.split(':')
            req_id = parts[1]
            callback = parts[2]

            req_status = core.get_req_status(req_id)
            request_data = core.get_request_data(req_id, callback)
            len_req_data = len(request_data)

            i = 1
            for data in request_data:
                if i == len_req_data:
                    markup_req = markup.markup_request_action(req_id, req_status, callback)
                else:
                    markup_req = None

                bot.send_message(chat_id=call.message.chat.id, text=data, parse_mode='html', reply_markup=markup_req)

                i += 1

            bot.answer_callback_query(call.id)

        #Добавить сообщение в запрос
        elif 'add_message:' in call.data:
            parts = call.data.split(':')
            req_id = parts[1]
            status_user = parts[2]

            take_additional_message = bot.send_message(chat_id=call.message.chat.id, text='Отправьте ваше сообщение.', reply_markup=markup.markup_cancel())

            bot.register_next_step_handler(take_additional_message, get_additional_message, req_id, status_user)

            bot.answer_callback_query(call.id)

        #Завершить запрос
        elif 'confirm_req:' in call.data:
            parts = call.data.split(':')
            confirm_status = parts[1]
            req_id = parts[2]

            if core.get_req_status(req_id) == 'confirm':
                bot.send_message(chat_id=call.message.chat.id, text="⚠️ Этот запрос уже завершен.", reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)

                return
            
            #Запросить подтверждение завершения
            if confirm_status == 'wait':
                bot.send_message(chat_id=call.message.chat.id, text="Для завершения запроса - нажмите кнопку <b>Подтвердить</b>", parse_mode='html', reply_markup=markup.markup_confirm_req(req_id))
            
            #Подтвердить завершение
            elif confirm_status == 'true':
                core.confirm_req(req_id)
                
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="✅ Запрос успешно завершён.", reply_markup=markup.markup_main())
                except:
                    bot.send_message(chat_id=call.message.chat.id, text="✅ Запрос успешно завершён.", reply_markup=markup.markup_main())

                bot.answer_callback_query(call.id)

        #Вернуться назад в панель агента
        elif call.data == 'back_agent':
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🔑 Вы авторизованы как Агент поддержки', parse_mode='html', reply_markup=markup.markup_agent())
            except:
                bot.send_message(call.message.chat.id, '🔑 Вы авторизованы как Агент поддержки', parse_mode='html', reply_markup=markup.markup_agent())

            bot.answer_callback_query(call.id)

        #Вернуться назад в панель админа
        elif call.data == 'back_admin':
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🔑 Вы авторизованы как Админ', parse_mode='html', reply_markup=markup.markup_admin())
            except:
                bot.send_message(call.message.chat.id, '🔑 Вы авторизованы как Админ', parse_mode='html', reply_markup=markup.markup_admin())

            bot.answer_callback_query(call.id)

        #Добавить агента
        elif call.data == 'add_agent':
            take_agent_id_message = bot.send_message(chat_id=call.message.chat.id, text='Чтобы добавить агента поддержки - введите его ID Telegram.', reply_markup=markup.markup_cancel())
            bot.register_next_step_handler(take_agent_id_message, get_agent_id_message)

        #Все агенты
        elif 'all_agents:' in call.data:
            number = call.data.split(':')[1]
            markup_and_value = markup.markup_agents(number)
            markup_agents = markup_and_value[0]
            len_agents = markup_and_value[1]

            if len_agents == 0:
                bot.send_message(chat_id=call.message.chat.id, text='⚠️ Агенты не обнаружены.', reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)
                return

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Нажмите на агента поддержки, чтобы удалить его', parse_mode='html', reply_markup=markup_agents)
            except:
                bot.send_message(call.message.chat.id, 'Нажмите на агента поддержки, чтобы удалить его', parse_mode='html', reply_markup=markup_agents)

            bot.answer_callback_query(call.id)

        #Удалить агента
        elif 'delete_agent:' in call.data:
            agent_id = call.data.split(':')[1]
            core.delete_agent(agent_id)

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Нажмите на агента поддержки, чтобы удалить его', parse_mode='html', reply_markup=markup.markup_agents('1')[0])
            except:
                bot.send_message(call.message.chat.id, 'Нажмите на агента поддержки, чтобы удалить его', parse_mode='html', reply_markup=markup.markup_agents('1')[0])

            bot.answer_callback_query(call.id)

        #Все пароли
        elif 'all_passwords:' in call.data:
            number = call.data.split(':')[1]
            markup_and_value = markup.markup_passwords(number)
            markup_passwords = markup_and_value[0]
            len_passwords = markup_and_value[1]

            if len_passwords == 0:
                bot.send_message(chat_id=call.message.chat.id, text='⚠️ Пароли не обнаружены.', reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)
                return

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Нажмите на пароль, чтобы удалить его', parse_mode='html', reply_markup=markup_passwords)
            except:
                bot.send_message(call.message.chat.id, 'Нажмите на пароль, чтобы удалить его', parse_mode='html', reply_markup=markup_passwords)

            bot.answer_callback_query(call.id)

        #Удалить пароль
        elif 'delete_password:' in call.data:
            password = call.data.split(':')[1]
            core.delete_password(password)

            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Нажмите на пароль, чтобы удалить его', parse_mode='html', reply_markup=markup.markup_passwords('1')[0])
            except:
                bot.send_message(call.message.chat.id, 'Нажмите на пароль, чтобы удалить его', parse_mode='html', reply_markup=markup.markup_passwords('1')[0])

            bot.answer_callback_query(call.id)

        #Сгенерировать пароли
        elif call.data == 'generate_passwords':
            #10 - количество паролей, 16 - длина пароля
            passwords = core.generate_passwords(10, 16) 
            core.add_passwords(passwords)

            text_passwords = ''
            i = 1
            for password in passwords:
                text_passwords += f'{i}. {password}\n'
                i += 1

            bot.send_message(call.message.chat.id, f"✅ Сгенерировано {i-1} паролей:\n\n{text_passwords}", parse_mode='html', reply_markup=markup.markup_main())
            bot.send_message(call.message.chat.id, 'Нажмите на пароль, чтобы удалить его', parse_mode='html', reply_markup=markup.markup_passwords('1')[0])

            bot.answer_callback_query(call.id)
        
        #Показать имеющиеся контакты
        elif call.data == 'contacts':
            contacts_text = ''
            i = 1
            contacts = core.get_contacts()
            if contacts:
                for contact_id, contact_info, date in contacts:
                    contacts_text += f'{i}. Пользователь {contact_id}\n{contact_info}\n({date})\n'
                    i += 1

                bot.send_message(call.message.chat.id, f"В базе имеется {len(contacts)} сведений о контактах:\n\n{contacts_text}", parse_mode='html', reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)
            
            else:
                bot.send_message(call.message.chat.id, f"В базе нет сведений о контактах пользователей", parse_mode='html', reply_markup=markup.markup_main())
                bot.answer_callback_query(call.id)

        #Остановить бота
        elif 'stop_bot:' in call.data:
            status = call.data.split(':')[1]

            #Запросить подтверждение на отключение
            if status == 'wait':
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы точно хотите отключить бота?", parse_mode='html', reply_markup=markup.markup_confirm_stop())
                except:
                    bot.send_message(call.message.chat.id, f"Вы точно хотите отключить бота?", parse_mode='html', reply_markup=markup.markup_confirm_stop())

            #Подтверждение получено
            elif status == 'confirm':
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Бот оключен.')
                except:
                    bot.send_message(chat_id=call.message.chat.id, text='✅ Бот оключен.')

                bot.answer_callback_query(call.id)
                bot.stop_polling()
                sys.exit()


if __name__ == "__main__":
    bot.polling(none_stop=True)
