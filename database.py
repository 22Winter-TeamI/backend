from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/bomastick" #로컬로 설정했을 경우 본인의 컴퓨터에 맞게 1234는 mysql비밀번호 bomastick은 데이터베이스 이름



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()