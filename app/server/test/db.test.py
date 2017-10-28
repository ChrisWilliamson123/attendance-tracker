import datetime, unittest
from server.db import DatabaseManager

class TestDatabaseMethods(unittest.TestCase):

    def assertRowSame(self, row, ticket):
        self.assertEqual(row[0], ticket['id'])
        self.assertEqual(row[1], ticket['direction'])
        self.assertEqual(row[2], ticket['action'])
        self.assertEqual(row[3], ticket['message'])
        self.assertEqual(row[4], ticket['time'])

    def setUp(self):
        self.test_db = DatabaseManager(':memory:')
        self.test_db.create_table('test', [('ID', 'INTEGER'), ('name', 'TEXT')])
        self.test_db.create_table("event",  [('ticket_id', 'INTEGER'),
                                             ('direction', 'INTEGER'),
                                             ('action', 'INTEGER'),
                                             ('message', 'TEXT'),
                                             ('time', 'INTEGER')])

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

    def test_insert_event(self):
        event = {'id':1, 'direction':1, 'action':1, 'message':'', 'time':1}
        self.test_db.insert_event(event)
        result = list(self.test_db.execute('SELECT * FROM event'))
        self.assertRowSame(result[0], event)
        self.assertEqual(len(result), 1)

    def test_get_entries_for_ticket(self):
        event = {'id':1, 'direction':1, 'action':1, 'message':'', 'time':1}
        self.test_db.insert_event(event)
        event['id'] = 2
        self.test_db.insert_event(event)
        result = list(self.test_db.get_entries_for_ticket(2));
        self.assertRowSame(result[0], event)
        self.assertEqual(len(result), 1)

    def test_get_all_entries(self):
        event = {'id':1, 'direction':1, 'action':1, 'message':'', 'time':1}
        self.test_db.insert_event(event)
        event['id'] = 2
        self.test_db.insert_event(event)
        result = list(self.test_db.get_all_entries());
        self.assertRowSame(result[1], event)
        event['id'] = 1
        self.assertRowSame(result[0], event)
        self.assertEqual(len(result), 2)

    def tearDown(self):
        self.test_db.close_connection()

    


if __name__ == '__main__':
    unittest.main()
