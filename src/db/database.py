from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


# подключаюсь к базе данных с именем и паролем
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
