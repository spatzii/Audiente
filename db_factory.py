import sqlite3 as db


def create_table():
    con = db.connect('settings.db')
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS email_settings(receiver)')
    con.close()


def read_table():
    con = db.connect('settings.db')
    con.row_factory = lambda crs, row: row[0]
    cursor = con.cursor()
    res = cursor.execute('SELECT receiver FROM email_settings')
    return res.fetchone()


def insert_email(email):
    con = db.connect('settings.db')
    cursor = con.cursor()
    cursor.execute(f"""
            INSERT INTO email_settings VALUES
            ('{email}')
    """)
    con.commit()
    con.close()


def clear_email():
    con = db.connect('settings.db')
    cursor = con.cursor()
    cursor.execute("""DROP TABLE IF EXISTS email_settings""")
    create_table()



