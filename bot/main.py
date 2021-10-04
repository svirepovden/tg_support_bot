from telegram.ext import Updater
from .guest_handlers import guest_conv_handler
from .admin_handlers import admin_conv_handler
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def bot_main(TOKEN: str):
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(guest_conv_handler)

    dispatcher.add_handler(admin_conv_handler)

    updater.start_polling()
    updater.idle()
