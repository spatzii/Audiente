import sqlite3 as db


class EmailSettings:
    """Creates ONE email id with selected slot for sending email information. Replaced for every address change"""

    def __init__(self):
        self.conn = db.connect('settings.db')
        self.conn.row_factory = lambda crs, row: row[0]
        self.cursor = self.conn.cursor()

    def create_table(self):
        return self.cursor.execute('CREATE TABLE IF NOT EXISTS email_settings(id INT, receiver, slot)')

    def fetch_receiver(self):
        res = self.cursor.execute('SELECT receiver FROM email_settings')
        return res.fetchone()

    def fetch_slot(self):
        res = self.cursor.execute('SELECT slot FROM email_settings')
        return res.fetchone()

    def update_email(self, email):
        self.cursor.execute(f"""UPDATE email_settings SET receiver = '{email}' WHERE id=1""")
        self.conn.commit()
        self.conn.close()

    def update_slot(self, slot):
        self.cursor.execute(f"""UPDATE email_settings SET slot = '{slot}' WHERE id=1""")
        self.conn.commit()
        self.conn.close()









