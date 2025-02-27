from sqlalchemy import Column, Integer, BigInteger, String, Text, Double, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base

class PlayerScore(Base):
    __tablename__ = "playerscore"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    score = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[str] = mapped_column(String, nullable=True)


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)

    sap_category = relationship("SapCategory", back_populates="category")


class SapCategory(Base):
    __tablename__ = 'sap_category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(Text, nullable=True)
    title: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Double)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id, ondelete="CASCADE"))

    category = relationship("Category", back_populates="sap_category")
