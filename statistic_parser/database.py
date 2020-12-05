from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:12345678@avito_parser_data/avito_parser"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLALCHEMY_DATABASE_URL = "sqlite://///Users/admin/PycharmProjects/avito-tech-mi-backend-trainee-assignment/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# engine = create_engine('sqlite://///Users/admin/PycharmProjects/avito-tech-mi-backend-trainee-assignment/sql_app.db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db = SessionLocal()


