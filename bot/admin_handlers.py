from .actions import is_admin, get_messages, save_message, change_chat_status
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext,
                          ConversationHandler)


def admin(update, context: CallbackContext):
    if is_admin(update.message):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This is Admin Panel\n\n/show_messages")
        return SHOW_MESSAGES
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You have no permission for that")


def show_messages(update, context: CallbackContext):
    if is_admin(update.message):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_messages() + get_messages(status='in_process'))
        return REPLY


def reply_chat(update, context):
    if is_admin(update.message):
        global chat_id
        chat_id = int(update.message.text[7:])
        reply = 'You are replying to ' + str(chat_id) + '\n' + get_messages(chat_id)

        print(reply)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=reply)
        return GET_ANSWER


def get_answer(update, context):
    if is_admin(update.message):
        global chat_id
        save_message(update.message, True)
        context.bot.send_message(chat_id=chat_id, text=update.message.text)
        chat_options = 'Chat options:\n' + '/close_' + str(chat_id) + '\n /await_' + str(chat_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=chat_options)
        chat_id = None
        print('answered')
        return CHAT_ACTIONS
# TODO get questions in realtime while answering


def close_chat_option(update, context):
    if is_admin(update.message):
        chat = int(update.message.text[7:])
        print('close ', chat)
        change_chat_status('closed', chat)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='chat was closed\n\n/show_messages')
        return SHOW_MESSAGES


def await_chat_option(update, context):
    if is_admin(update.message):
        chat = int(update.message.text[7:])
        print('await ', chat)
        change_chat_status('in_process', chat)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='chat is in awaited mode\n\n /show_messages')
        return SHOW_MESSAGES


def exit_(update, context):
    if is_admin(update.message):
        print('admin exit')
    else:
        print('guest exit')
    return ConversationHandler.END


chat_id = None  # used for storing to what chat answer must go
SHOW_MESSAGES, REPLY, GET_ANSWER, CHAT_ACTIONS = range(4)

admin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('admin', admin)],
    states={
        SHOW_MESSAGES: [CommandHandler('show_messages', show_messages)],
        REPLY: [MessageHandler(Filters.regex(r'/reply_[0-9]*'), reply_chat)],
        GET_ANSWER: [MessageHandler(Filters.all, get_answer)],
        CHAT_ACTIONS: [MessageHandler(Filters.regex(r'/close_[0-9]*'), close_chat_option),
                       MessageHandler(Filters.regex(r'/await_[0-9]*'), await_chat_option)]
    },
    fallbacks=[CommandHandler('exit', exit_)]
)
