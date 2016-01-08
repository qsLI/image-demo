import sqlite3
from datetime import datetime
DATABASE = 'C:\Users\KL\PycharmProjects\untitled\database.db'  # must be full path


def connect_db():
    try:
        sqlite_conn = sqlite3.connect(DATABASE)
        return sqlite_conn
    except sqlite3.Error, e:
        print "connection error: ", "\n", e.args[0]


if __name__ == "__main__":
    conn = connect_db()
    name = "image_1"
    date = datetime.now()
    with open(r"C:\Users\KL\PycharmProjects\untitled\img\test.jpg", 'rb') as f:
        data = f.read(-1)
    sql_add = """
                INSERT INTO img(name, date, data) VALUES (?, ?, ?);
              """

    try:
        for x in range(6):
            conn.cursor().execute(sql_add, (name, date, buffer(data)))
        conn.commit()
    except Exception,e:
        print "error " + e.message
