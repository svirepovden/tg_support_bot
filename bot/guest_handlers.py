from .actions import save_message, register_user
from telegram.ext import (CommandHandler, MessageHandler, Filters, CallbackContext,
                          ConversationHandler)


def start(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to support bot\n\nText your issue")
    register_user(update.message)
    return TEXT_ISSUE


def echo(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="We've got your message")
    save_message(update.message)


def exit_(update, context):
    print('guest exit')
    return ConversationHandler.END


TEXT_ISSUE = range(1)

guest_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TEXT_ISSUE: [MessageHandler(Filters.text & (~Filters.command), echo)]
        },
        fallbacks=[CommandHandler('exit', exit_)]
    )
