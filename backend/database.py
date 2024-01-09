import sqlite3
import json


class Database:
    def __init__(self, db_name='ele495.db'):
        self.db_name = db_name
        self.conn = self.connect_database()
        self.create_table()

    def connect_database(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'Processing',
                description TEXT DEFAULT 'Not available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_session(self, name):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO session (name) VALUES (?)', (name,))
        self.conn.commit()

    def get_all_session(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM session ORDER BY created_at DESC')
        all_sessions = cursor.fetchall()

        list = []
        for session in all_sessions:
            session_dict = {
                'id': session[0],
                'name': session[1],
                'status': session[2],
                'description': session[3],
                'created_at': str(session[4])
            }
            list.append(session_dict)

        return list

    def update_session(self, id, status, explanation):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE session SET status=?, description=? WHERE id=?', (status, explanation, id,))
        self.conn.commit()

    def delete_session(self, id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM session WHERE id = ?', (id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
