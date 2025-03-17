from sqlalchemy import Column, Integer, BigInteger, String, Text, Double, ForeignKey,Boolean
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

    location = relationship("Location",back_populates="user")
    order = relationship("Order",back_populates="user")



class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(Text,nullable=True)

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

class Location(Base):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    address: Mapped[str] = mapped_column(String,nullable=True)
    longitude: Mapped[int] = mapped_column(Double,nullable=True)
    latitude: Mapped[int] = mapped_column(Double,nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger,ForeignKey(User.id, ondelete = "CASCADE"))

    user = relationship("User",back_populates="location")
    order = relationship("Order",back_populates="location")




class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger,ForeignKey(User.id,ondelete="CASCADE"))
    location_id: Mapped[int] = mapped_column(Integer,ForeignKey(Location.id, ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String,default="pending")

    location = relationship("Location",back_populates="order")
    user = relationship("User",back_populates="order")
    order_product = relationship("OrderProduct",back_populates="order")

class OrderProduct(Base):
    __tablename__ = "order_product"
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True,autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Order.id, ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer,nullable=True)
    product_id: Mapped[int] = mapped_column(Integer,ForeignKey(SapCategory.id,ondelete="CASCADE"))
    price: Mapped[int] = mapped_column(Double,nullable=True)

    order = relationship("Order", back_populates="order_product")


