import unittest
from server.db import DatabaseManager

class TestDatabaseMethods(unittest.TestCase):

    def test_create_table(self):
        test_db = DatabaseManager(':memory:')
        cursor = test_db.connection.cursor()
        test_db.create_table('test', [('ID', 'INTEGER'), ('name', 'TEXT')])
        columns = cursor.execute('PRAGMA table_info("test");').fetchall()

        self.assertEqual(columns[0][1], 'ID')
        self.assertEqual(columns[0][2], 'INTEGER')
        self.assertEqual(columns[1][1], 'name')
        self.assertEqual(columns[1][2], 'TEXT')


if __name__ == '__main__':
    unittest.main()