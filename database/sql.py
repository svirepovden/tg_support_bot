import sqlite3


def row_exists(database: str, table: str, column: str, value: str) -> bool:
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        # TODO different queries for different types of value
        sql_query = f'''SELECT 1 from {table} where {column} = {value};'''

        cur.execute(sql_query)
        try:
            record = bool(cur.fetchone()[0])
            cur.close()
            return record
        except TypeError as error:
            cur.close()
            if error == "'NoneType' object is not subscriptable":
                print('row does not exist in db')
            else:
                print('Error: ', error)
            return False
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
        return False
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')


def insert(database: str, table: str, columns: tuple, values: tuple):
    columns_str = ', '.join(columns)
    values_str = ''

    for value in values:
        if isinstance(value, int):
            values_str = values_str + str(value) + ", "
        elif isinstance(value, float):
            values_str = values_str + str(value) + ", "
        elif isinstance(value, str):
            values_str = values_str + "'" + value + "', "
        else:
            print(type(value))
            print('type is not int, float or string')
    values_str = values_str[:-2]

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        sql_query = f'''INSERT INTO {table} ({columns_str}) VALUES ({values_str})'''
        print(sql_query)

        cur.execute(sql_query)
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')


def select(database: str, table: str, where: tuple = None, opt: str = '') -> list:
    if where:
        where_str = ''.join(where[:2])
        last = where[2:][0]
        if isinstance(last, int):
            where_str += str(last)
        elif isinstance(last, float):
            where_str += str(last)
        elif isinstance(last, str):
            where_str += ("'" + last + "'")
        else:
            print('not int, float, or str')
        sql_query = f'''SELECT * FROM {table} WHERE {where_str}{opt};'''
    else:
        sql_query = f'''SELECT * FROM {table}{opt} ;'''

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        cur.execute(sql_query)
        record = cur.fetchall()
        print(record)
        cur.close()
        return record
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
        return []
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')


def update(database: str, table: str, column: str, value, id_column: str, id_value):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sql_query = None
        if isinstance(value, str) and isinstance(id_value, str):
            sql_query = f'''UPDATE {table} SET {column}='{value}' WHERE {id_column}='{id_value}' ;'''
        elif (isinstance(value, str) and isinstance(id_value, int) or
              isinstance(value, str) and isinstance(id_value, float)):
            sql_query = f'''UPDATE {table} SET {column}='{value}' WHERE {id_column}={id_value}; '''
        elif (isinstance(value, int) and isinstance(id_value, str) or
              isinstance(value, float) and isinstance(id_value, str)):
            sql_query = f'''UPDATE {table} SET {column}={value} WHERE {id_column}='{id_value}'; '''
        elif (isinstance(value, int) and isinstance(id_value, int) or
              isinstance(value, float) and isinstance(id_value, float)):
            sql_query = f'''UPDATE {table} SET {column}={value} WHERE {id_column}={id_value}; '''
        else:
            print('wrong value type, must be str, int or float')

        print(sql_query)
        cur.execute(sql_query)
        record = cur.fetchall()
        print(record)
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Sqlite connection error ', error)
    finally:
        if (conn):
            conn.close()
            print('Sqlite connection closed')


