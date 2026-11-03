import sqlite3

DB_FILE = "omniphysics.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Chat History table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. User Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Simulation Configurations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulation_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_name TEXT,
            config_json TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_note(topic: str, content: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_notes (topic, content) VALUES (?, ?)",
        (topic, content)
    )
    conn.commit()
    conn.close()

def save_simulation_config(config_name: str, config_json: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO simulation_configs (config_name, config_json) VALUES (?, ?)",
        (config_name, config_json)
    )
    conn.commit()
    conn.close()