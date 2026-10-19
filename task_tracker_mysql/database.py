from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Format: mysql+pymysql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/tracker_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()