import sqlite3
import os

def get_db_path():
    # 🔥 Render path
    if os.environ.get("RENDER"):
        return "/opt/render/project/src/server_api/database/db.sqlite3"
    else:
        # 💻 Local path
        return "server_api/database/db.sqlite3"

def get_connection():
    path = get_db_path()

    print("🔥 DB PATH:", path)

    conn = sqlite3.connect(path)
    return conn