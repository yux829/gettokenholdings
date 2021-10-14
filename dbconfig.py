from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///asset.db", connect_args={"check_same_thread": False},pool_pre_ping=True)
# mysql
#engine = create_engine("mysql+pymysql://root:123456@localhost/testdb")
# 注意命名为SessionLocal，与sqlalchemy的session分隔开
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base =declarative_base()    
