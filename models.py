from sqlalchemy import Column,  String, DateTime, Float
from sqlalchemy.sql.functions import sysdate

from dbconfig import Base
# 模型类，tablename指表名，如果数据库中没有这个表会自动创建，有表则会沿用


class TokenHoldings(Base):
    __tablename__ = "TokenHoldings"
    address = Column(String(100), primary_key=True, index=True)
    symbol = Column(String(50), primary_key=True, index=True)
    date = Column(String(10), primary_key=True, index=True)
    name = Column(String(200))
    balance = Column(Float)
    price = Column(Float)
    totalvalue = Column(Float)
    updatetime = Column(DateTime)
