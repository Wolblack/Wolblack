from pathlib import Path
import sqlite3
DB_PATH=Path(__file__).resolve().parent.parent/'database'/'world.db'; DB_PATH.parent.mkdir(parents=True,exist_ok=True)
def connect():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
 c=connect(); c.executescript('''CREATE TABLE IF NOT EXISTS world(id INTEGER PRIMARY KEY CHECK(id=1),tick INTEGER NOT NULL DEFAULT 0,year INTEGER NOT NULL DEFAULT 1,day INTEGER NOT NULL DEFAULT 1,language_version INTEGER NOT NULL DEFAULT 1); INSERT OR IGNORE INTO world(id) VALUES(1); CREATE TABLE IF NOT EXISTS agents(id TEXT PRIMARY KEY,name TEXT NOT NULL,x INTEGER NOT NULL,y INTEGER NOT NULL,age INTEGER NOT NULL,energy INTEGER NOT NULL,curiosity REAL NOT NULL,personality TEXT NOT NULL,goal TEXT NOT NULL,alive INTEGER NOT NULL DEFAULT 1,knowledge_json TEXT NOT NULL DEFAULT '{}',memory_json TEXT NOT NULL DEFAULT '[]',vocabulary_json TEXT NOT NULL DEFAULT '{}'); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,tick INTEGER NOT NULL,kind TEXT NOT NULL,description TEXT NOT NULL);'''); c.commit(); c.close()
