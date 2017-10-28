import sqlite3

class DatabaseManager():
    instance = None
    def __init__(self, database_file=None):
        if not DatabaseManager.instance:
            DatabaseManager.instance = DatabaseManager.__DatabaseManager(database_file)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __DatabaseManager:
        def __init__(self, database_file):
            self.connection = sqlite3.connect(database_file)

        def close_connection(self):
            self.connection.close();

        def __execute(self, query, args=None):
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

        def __field_list_to_string(self, field_list):
            return ','.join(['"{}" "{}"'.format(x[0], x[1]) for x in field_list])

        def __insert_into(self, table_name, values):
            if type(values) is list:
                columns = len(values[0])
            else:
                columns = len(values)
            query = 'INSERT INTO {} VALUES ({})'.format(table_name, '?,'*(columns-1) + '?')
            self.__execute(query, values)
            self.connection.commit()
    
        def __select_from(self, table_name, fields):
            query = 'SELECT {} from {}'.format(','.join(fields), table_name)
            return self.__execute(query).fetchall()

        def get_table_info(self, table_name):
            query = 'PRAGMA table_info("{}")'.format(table_name)
            return self.__execute(query).fetchall()

        def create_table(self, name, fields):
            query = 'CREATE TABLE {} ({})'.format(name, self.__field_list_to_string(fields))
            self.__execute(query)

        def insert_event(self, gate_passage):
            values = (int(gate_passage['id']), int(gate_passage['direction']), int(gate_passage['action']), gate_passage['message'], gate_passage['time'])
            self.__insert_into('event', values)

        def get_entries_for_ticket(self, ticket_id):
            query = 'SELECT * from event WHERE ticket_id == {}'.format(ticket_id)
            return self.__execute(query).fetchall()
    
        def get_all_entries(self):
            query = 'SELECT * from event'
            return self.__execute(query).fetchall()

