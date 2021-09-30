from telegram.ext import (Updater,
                          CommandHandler, MessageHandler,
                          Filters, CallbackContext,
                          ConversationHandler)
from bot.actions import save_message, register_user, is_admin, get_messages, change_chat_status
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to support bot\n\nText your issue")
    register_user(update.message)
    return TEXT_ISSUE


def echo(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="We've got your message")
    save_message(update.message)


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


SHOW_MESSAGES, REPLY, GET_ANSWER, CHAT_ACTIONS = range(4)
TEXT_ISSUE = range(1)
chat_id = None  # used for storing to what chat answer must go


def bot_main(TOKEN: str):
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    guest_conv_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            TEXT_ISSUE: [echo_handler]
        },
        fallbacks=[CommandHandler('exit', exit_)]
    )
    dispatcher.add_handler(guest_conv_handler)

    admin_handler = CommandHandler('admin', admin)
    show_messages_handler = CommandHandler('show_messages', show_messages)
    reply_chat_handler = MessageHandler(Filters.regex(r'/reply_[0-9]*'), reply_chat)
    close_chat_handler = MessageHandler(Filters.regex(r'/close_[0-9]*'), close_chat_option)
    await_chat_handler = MessageHandler(Filters.regex(r'/await_[0-9]*'), await_chat_option)
    admin_conv_handler = ConversationHandler(
        entry_points=[admin_handler],
        states={
            SHOW_MESSAGES: [show_messages_handler],
            REPLY: [reply_chat_handler],
            GET_ANSWER: [MessageHandler(Filters.all, get_answer)],
            CHAT_ACTIONS: [close_chat_handler, await_chat_handler]
        },
        fallbacks=[CommandHandler('exit', exit_)]
    )
    dispatcher.add_handler(admin_conv_handler)

    updater.start_polling()
    updater.idle()
