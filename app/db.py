from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# MySQL Connection URL (pymysql 사용)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM Base 클래스
Base = declarative_base()

# 테이블 자동 생성
def init_db():
    Base.metadata.create_all(bind=engine)

# FastAPI 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
