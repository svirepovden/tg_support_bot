from bot.bot import bot_main
from database import schema
import config


if __name__ == '__main__':
    if schema.check_struct(config.database_name):
        print('Database structure is fine')
        database_name = config.database_name
    else:
        print('Database structure is not fine, recreating structure')
        schema.create_struct(config.database_name)
        if schema.check_struct(config.database_name):
            print('Database structure is fine')
        else:
            print('Unable to create database structure')
            exit(1)

    bot_main(config.TOKEN)

