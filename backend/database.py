import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('mounam.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY, text TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS saved
                 (id INTEGER PRIMARY KEY, text TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_to_history(text):
    conn = sqlite3.connect('mounam.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO history (text, timestamp) VALUES (?, ?)", (text, timestamp))
    conn.commit()
    conn.close()

def save_to_saved(text):
    conn = sqlite3.connect('mounam.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO saved (text, timestamp) VALUES (?, ?)", (text, timestamp))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('mounam.db')
    c = conn.cursor()
    c.execute("SELECT text, timestamp FROM history")
    data = [{'text': row[0], 'timestamp': row[1]} for row in c.fetchall()]
    conn.close()
    return data

def get_saved():
    conn = sqlite3.connect('mounam.db')
    c = conn.cursor()
    c.execute("SELECT text, timestamp FROM saved")
    data = [{'text': row[0], 'timestamp': row[1]} for row in c.fetchall()]
    conn.close()
    return data