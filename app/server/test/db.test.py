import datetime, unittest
from server.db import DatabaseManager

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.test_db = DatabaseManager(':memory:')
        self.test_db.create_table('test', [('ID', 'INTEGER'), ('name', 'TEXT')])

    def test_create_table(self):
        columns = self.test_db.get_table_info('test')

        self.assertEqual(columns[0][1], 'ID')
        self.assertEqual(columns[0][2], 'INTEGER')
        self.assertEqual(columns[1][1], 'name')
        self.assertEqual(columns[1][2], 'TEXT')

    def test_insert_into_select_from(self):
        self.test_db.insert_into('test', (1, 'Chris'))
        results = self.test_db.select_from('test', ['ID', 'name'])
        self.assertEqual(results, [(1, 'Chris')])

    def test_multi_insert(self):
        data = [(x, 'test') for x in range(1, 101)]
        self.test_db.insert_into('test', data)
        results = self.test_db.select_from('test', ['ID', 'name'])
        self.assertEqual(results, data)

    def tearDown(self):
        self.test_db.close_connection()


if __name__ == '__main__':
    unittest.main()