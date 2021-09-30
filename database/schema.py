import sqlite3

SQL_SCHEMA_MESSAGES = '''CREATE TABLE "messages" (
	"message_id"	INTEGER NOT NULL,
	"chat_id"	INTEGER NOT NULL,
	"content"	TEXT NOT NULL,
	"date"	INTEGER NOT NULL,
	"status"	TEXT NOT NULL DEFAULT 'open',
	FOREIGN KEY("chat_id") REFERENCES "chats"("chat_id"),
	PRIMARY KEY("message_id")
);'''

SQL_SCHEMA_CHATS = '''CREATE TABLE "chats" (
	"chat_id"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("chat_id")
);'''

SQL_SCHEMA_USERS = '''CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"role"	TEXT NOT NULL,
	"username"	TEXT,
	PRIMARY KEY("id")
);'''


def check_table(database_name, table: str, schema: str) -> bool:
    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cur.execute(f'''
        SELECT sql
        FROM sqlite_master
        WHERE tbl_name = '{table}';''')
        record = cur.fetchall()
        try:
            # print(record[0][0] + ';')
            # print(1)
            # print(schema)
            # print(1)
            result = (record[0][0] + ';') == schema

        except IndexError as error:
            print('Failed to fetch data ', error)
            result = False

        cur.close()
        return result
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
        return False
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')


def check_struct(database_name) -> bool:

    return (check_table(database_name, 'users', SQL_SCHEMA_USERS) &
            check_table(database_name, 'messages', SQL_SCHEMA_MESSAGES) &
            check_table(database_name, 'chats', SQL_SCHEMA_CHATS))


def create_struct(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()

        sql_query = SQL_SCHEMA_MESSAGES
        cur.execute(sql_query)

        sql_query = SQL_SCHEMA_USERS
        cur.execute(sql_query)

        cur.close()
        result = True
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
        result = False
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')
    return result
