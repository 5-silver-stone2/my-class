import sqlite3
DB_NAME = 'songs.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS songs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL DEFAULT '앨범없음',
    rating INTEGER DEFAULT 0,
    finished INTEGER DEFAULT 0)""")

    columns = [column[1] for column in cursor.execute("PRAGMA table_info(songs)")]
    if 'album' not in columns:
        cursor.execute("ALTER TABLE songs ADD COLUMN album TEXT NOT NULL DEFAULT '앨범없음'")

    conn.commit()
    conn.close()


def add_song(title, artist, album):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO songs(title, artist, album) VALUES (?, ?, ?)
    """,(title, artist, album))

    conn.commit()
    conn.close()

def get_all_songs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, title, artist, album, rating, finished FROM songs ORDER BY id""")

    rows = cursor.fetchall()
    conn.close()
    return rows

#create_table()
#add_song('어린왕자','생택쥐페리')
#add_song('데미안','헤르만헤세')
#print(get_all_songs())

def update_rating(_id, rating):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""UPDATE songs SET rating = ? WHERE id = ?""",(rating, _id))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed

#print(update_rating(1,4))
#print(get_all_songs())

def toggle_finished(song_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT finished FROM songs WHERE id = ?
    """,(song_id,))
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

    cursor.execute("""UPDATE songs SET finished = ? WHERE id = ?
    """,(new_status, song_id))
    conn.commit()
    conn.close()
    return True

#toggle_finished(1)
#print(get_all_songs())

def delete_song(song_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM songs WHERE id =?
    """, (song_id,))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed    

def search_songs(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, title, artist, album, rating, finished
    FROM songs
    WHERE title LIKE ?
    ORDER BY id
    """, (f"%{keyword}%",)) #%는 압뒤로 다른 문자가 있어도 된다는표시

    rows = cursor.fetchall()
    conn.close()
    return rows