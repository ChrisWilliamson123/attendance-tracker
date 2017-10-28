import sqlite3

class DatabaseManager():
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.db_file = database_file

    def close_connection(self):
        self.connection.close();

    def execute(self, query, args=None):
        cursor= self.connection.cursor()
        if args:
            print('Executing query with args: {}, {}'.format(query, args))
            if type(args) is list:
                return cursor.executemany(query, args)
            else:
                return cursor.execute(query, args)
        else:
            print('Executing query: {}'.format(query))
            return cursor.execute(query)

    def field_list_to_string(self, field_list):
        return ','.join(['"{}" "{}"'.format(x[0], x[1]) for x in field_list])

    def get_table_info(self, table_name):
        query = 'PRAGMA table_info("{}")'.format(table_name)
        return self.execute(query).fetchall()

    def create_table(self, name, fields):
        query = 'CREATE TABLE {} ({})'.format(name, self.field_list_to_string(fields))
        self.execute(query)

    def insert_into(self, table_name, values):
        if type(values) is list:
            columns = len(values[0])
        else:
            columns = len(values)
        query = 'INSERT INTO {} VALUES ({})'.format(table_name, '?,'*(columns-1) + '?')
        self.execute(query, values)

    def select_from(self, table_name, fields):
        query = 'SELECT {} from {}'.format(','.join(fields), table_name)
        return self.execute(query).fetchall()


