import sqlite3

class DatabaseManager():
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)

    def close_connection(self):
        self.connection.close();

    def field_list_to_string(self, field_list):
        return ','.join(['"{}" "{}"'.format(x[0], x[1]) for x in field_list])

    def get_table_info(self, table_name):
        cursor = self.connection.cursor()
        query = 'PRAGMA table_info("{}")'.format(table_name)
        return cursor.execute(query).fetchall()

    def create_table(self, name, fields):
        cursor = self.connection.cursor()
        query = 'CREATE TABLE {} ({})'.format(name, self.field_list_to_string(fields))
        cursor.execute(query)
