import sqlite3
DB_NAME = 'books.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    rating INTEGET DEFAULT 0,
    finished INTRGET DEFAULT 0)""")

    conn.commit()
    conn.close()

def add_book(title, author):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO BOOKS(title, author) VALUES (?, ?)
    """,(title, author))

    conn.commit()
    conn.close()

def get_all_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, title, author, rating, finished FROM books ORDER BY id""")

    rows = cursor.fetchall()
    conn.close()
    return rows

#create_table()
#add_book('어린왕자','생택쥐페리')
#add_book('데미안','헤르만헤세')
#print(get_all_books())

def update_rating(book_id, rating):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""UPDATE books SET rating = ? WHERE id = ?""",(rating, book_id))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed

#print(update_rating(1,4))
#print(get_all_books())

def toggle_finished(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT finished FROM books WHERE id = ?
    """,(book_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return False
    print(row)
    current_status = row[0]
    if current_status==0:
        new_status = 1
    else:
        new_status = 0

    cursor.execute("""UPDATE books SET finished = ? WHERE id = ?
    """,(new_status, book_id))
    conn.commit()
    conn.close()
    return True

#toggle_finished(1)
#print(get_all_books())

def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM books WHERE id =?
    """, (book_id))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed    

def search_books(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, title, author, rating, finished
    FROM books
    WHERE title LIKE ?
    ORDER BY id
    """, (f"%{keyword}%",)) #%는 압뒤로 다른 문자가 있어도 된다는표시

    rows = cursor.fetchall()
    conn.close()
    return rows