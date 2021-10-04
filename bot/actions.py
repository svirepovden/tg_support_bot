from telegram import Message
from config import database_name
import time
from database.sql import row_exists, insert, select, update


def save_message(message: Message, support_reply: bool = False):
    chat_id = message.chat.id
    type_ = message.chat.type

    message_id = message.message_id
    if support_reply: content = "RE: " + message.text
    else: content = message.text
    date_ = int(time.mktime(message.date.timetuple()))
    status = 'open'
    print(database_name)

    if row_exists(database_name, 'chats', 'chat_id', str(chat_id)):
        print('row exists')
    else:
        insert(database_name, 'chats', ('chat_id', 'types'), (chat_id, type_))

    if row_exists(database_name, 'messages', 'message_id', str(message_id)):
        print('row exists')
    else:
        insert(database_name, 'messages', ('message_id', 'chat_id', 'content', 'date', 'status'),
               (message_id, chat_id, content, date_, status))


def get_messages(chat: int = None, status: str = 'open') -> str:
    result = f' \n\n {status} Messages:\n'
    chat_id = 0
    chat_counter = 0
    message_counter = 0
    tab = '    '
    if chat:
        table = select(database_name, 'messages', ('status', '=', status), f' AND chat_id = {chat}')
        for row in table:
            message_counter += 1
            result += (tab + str(message_counter) + '. ' + row[2] + '\n')
        print(result)
        return result
    else:
        table = select(database_name, 'messages', ('status', '=', status))
        if not table:
            result += 'There is no messages'
        else:
            for row in table:
                if row[1] != chat_id:
                    chat_id = row[1]
                    chat_counter += 1
                    result += ('\n' + str(chat_counter) + '. Chat /reply_' + str(row[1]) + '\n')
                    message_counter = 1
                    result += (tab + str(message_counter) + '. ' + row[2] + '\n')
                else:
                    message_counter += 1
                    result += (tab + str(message_counter) + '. ' + row[2] + '\n')

        print(result)
        return result


def register_user(message: Message):
    print(message.from_user)
    user_id = message.from_user.id
    username = message.from_user.username
    role = 'guest'
    if not(username):
        username = ''

    if row_exists(database_name, 'users', 'id', str(user_id)):
        print('user exist')
    else:
        insert(database_name, 'users', ('id', 'role', 'username'), (user_id, role, username))


def is_admin(message: Message) -> bool:
    db_users = select(database_name, 'users', where=('id', '=', message.from_user.id))
    # TODO try except out of list error
    # try:
    if db_users[0][1] == 'admin':
        print('admin')
        return True
    elif db_users[0][1] == 'guest':
        print('guest')
        return False
    else:
        print('some one else role')
        return False
    # except


def change_chat_status(status: str, chat_id: int):
    chat = select(database_name, 'messages', where=('chat_id', '=', str(chat_id)))
    for message in chat:
        update(database_name, 'messages', 'status', status, 'message_id', message[0])
