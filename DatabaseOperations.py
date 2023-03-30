import sqlite3 as db
import streamlit as st


class EmailSettings:
    """Creates users with email & selected slot for sending email information"""

    def __init__(self):
        self.conn = db.connect('settings.db')
        self.conn.row_factory = lambda crs, row: row[0]
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        return self.cursor.execute('CREATE TABLE IF NOT EXISTS email_settings(receiver VARCHAR(255) UNIQUE, slot)')

    def fetch_receivers(self):
        res = self.cursor.execute('SELECT receiver FROM email_settings')
        return res.fetchall()

    def fetch_slot(self, email):
        res = self.cursor.execute(f"""SELECT slot FROM email_settings WHERE receiver = ('{email}')""")
        return res.fetchone()

    def delete_user(self, email):
        self.cursor.execute(f"""DELETE FROM email_settings WHERE receiver = '{email}'""")
        self.conn.commit()
        self.conn.close()

    def add_user(self, email, slot):
        try:
            self.cursor.execute(f"""INSERT INTO email_settings (receiver, slot) VALUES ('{email}', '{slot}')""")
        except db.IntegrityError:
            st.warning('Adresa de email este deja înregistrată.')
        self.conn.commit()
        self.conn.close()

    def update_slot(self, email, slot):
        self.cursor.execute(f"""UPDATE email_settings SET slot = '{slot}' WHERE receiver = '{email}'""")
        self.conn.commit()
        self.conn.close()









