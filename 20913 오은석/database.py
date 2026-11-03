import sqlite3
from pathlib import Path

# 이 파일과 같은 폴더에 데이터베이스 저장
DB_PATH = Path(__file__).resolve().parent / "movies.db"


def connect_db():
    """데이터베이스에 연결한다."""
    return sqlite3.connect(str(DB_PATH))


def create_table():
    """영화 정보를 저장할 테이블을 생성한다."""
    conn = connect_db()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                year INTEGER
            )
        """)

        conn.commit()

    finally:
        conn.close()


def add_movie(title, director, year):
    """영화의 제목, 감독, 개봉연도를 저장한다."""
    conn = connect_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO movies (
                title,
                director,
                year
            )
            VALUES (?, ?, ?)
            """,
            (title, director, year),
        )

        conn.commit()

    finally:
        conn.close()


def get_all_movies():
    """저장된 영화 전체를 ID 순서로 조회한다."""
    conn = connect_db()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                director,
                year
            FROM movies
            ORDER BY id
        """)

        return cursor.fetchall()

    finally:
        conn.close()


def search_movies(keyword):
    """제목에 검색어가 포함된 영화를 조회한다."""
    conn = connect_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                title,
                director,
                year
            FROM movies
            WHERE title LIKE ?
            ORDER BY id
            """,
            (f"%{keyword}%",),
        )

        return cursor.fetchall()

    finally:
        conn.close()
