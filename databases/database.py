from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from urllib.parse import quote_plus

conn = f"""{settings.DATABASE_URL}"""
params = quote_plus(conn)
conn_str = f"mssql+pyodbc:///?autocommit=true&odbc_connect={params}"



engine = create_engine(conn_str, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()