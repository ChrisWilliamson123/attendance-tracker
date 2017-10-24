import datetime, unittest
from server.db import DatabaseManager

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.test_db = DatabaseManager(':memory:')

    def test_create_table(self):
        self.test_db.create_table('test', [('ID', 'INTEGER'), ('name', 'TEXT')])
        columns = self.test_db.get_table_info('test')

        self.assertEqual(columns[0][1], 'ID')
        self.assertEqual(columns[0][2], 'INTEGER')
        self.assertEqual(columns[1][1], 'name')
        self.assertEqual(columns[1][2], 'TEXT')

    def tearDown(self):
        self.test_db.close_connection()


if __name__ == '__main__':
    unittest.main()