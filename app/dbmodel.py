from datetime import datetime

import psycopg2


class Database:
    _host = 'localhost'
    _database = 'piastrix'
    _username = 'piastrix'
    _password = 'kgao39pu0loih'

    def __init__(self):
        self._connection = psycopg2.connect(dbname=self._database, user=self._username,
                                            password=self._password, host=self._host)
        self._cursor = self._connection.cursor()
        self._connection.autocommit = True

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __del__(self):
        self._cursor.close()
        self._connection.close()

    def get_order_id(self):
        self._cursor.execute('SELECT MAX(id) FROM payment')
        for row in self._cursor:
            return row[0]
        return 0

    def write_payment(self, order_id, currency, amount, description, message):
        self._cursor.execute('INSERT INTO payment(id, currency, amount, created_at, description, message) ' +
                             'VALUES (%s, %s, %s, %s, %s, %s)',
                             (order_id, currency, amount, datetime.now(), description, message))
