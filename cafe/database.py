from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Base

DB_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/cafedb'

engine = create_engine(DB_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def init_db(drop_existion: bool = True):
    if drop_existion:
        Base.metadata.drop_all(bind=engine)
        print('[database]기존 테이블 삭제')

    Base.metadata.create_all(bind=engine)
    print('[database]테이블 준비 완료')

def get_session():
    return SessionLocal()