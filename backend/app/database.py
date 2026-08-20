from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL database connection
DATABASE_URL = "mysql+pymysql://root:sonu@localhost:3306/resume_tracker"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    try:
        connection = engine.connect()
        print("MySQL connection successful!")
        connection.close()
    except Exception as e:
        print("MySQL connection failed!")
        print(e)