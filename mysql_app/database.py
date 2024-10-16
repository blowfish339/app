from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:1234@localhost/mydatabase", pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)