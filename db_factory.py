import sqlite3 as db


class EmailSettings:
    def __init__(self):
        self.conn = db.connect('settings.db')
        self.conn.row_factory = lambda crs, row: row[0]
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS email_settings(receiver)')

    def read_table(self):
        res = self.cursor.execute('SELECT receiver FROM email_settings')
        return res.fetchone()

    def insert_email(self, email):
        self.cursor.execute(f"""
                INSERT INTO email_settings VALUES
                ('{email}')
        """)
        self.conn.commit()
        self.conn.close()

    def clear_email(self):
        self.cursor.execute("""DROP TABLE IF EXISTS email_settings""")
        self.create_table()



