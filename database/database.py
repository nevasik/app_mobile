import sqlite3
import os

def init_db():
    try:
        os.mkdir('/Users/mac/PycharmProjects/app_poplaukhin')
        db_path = os.path.abspath("/Users/mac/PycharmProjects/app_poplaukhin")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('admin', 'user')),
            secret_question TEXT,
            secret_answer TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO categories (name)
        VALUES
            ('Рыба'), 
            ('Мясо'),
            ('Хлеб'),
            ('Овощи'),
            ('Фрукты')
        """)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        ''')

        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('admin', 'admin', 'admin');
        """)

        conn.commit()
        print("База данных успешно инициализирована.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        if conn:
            conn.close()