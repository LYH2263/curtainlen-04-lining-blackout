from app.db import connect

def get_all():
    c = connect()
    try:
        return {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        c.close()

def set_many(items: dict):
    c = connect()
    try:
        c.executemany("INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)", [(k, str(v)) for k, v in items.items()])
        c.commit()
    finally:
        c.close()
