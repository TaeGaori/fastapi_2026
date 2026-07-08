from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'

    메뉴코드 = Column(String(30), primary_key=True)   # 빈칸 1, 빈칸 2
    메뉴명 = Column(String(50), nullable=False)     # 빈칸 3
    가격 = Column(Integer, nullable=False)            # 빈칸 4

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 빈칸 5, 6
    주문일시 = Column(Date, nullable=False)   # 빈칸 7
    테이블번호 = Column(Integer, nullable=False)
    메뉴코드 = Column(String(10), nullable=False)
    수량 = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('테이블번호', '메뉴코드', '수량', name='uq_orders_key'),  # 빈칸 8, 9, 10
    )