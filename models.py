from typing import Optional, List
from datetime import datetime

from sqlalchemy import String, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



Base = declarative_base()
db = SQLAlchemy(model_class=Base, engine_options=dict(echo=True))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    password_: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean(), default=True)
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")

    @property
    def password(self):
        return self.password_
    
    @password.setter
    def password(self, pwd):
        self.password_ = generate_password_hash(pwd)

    def is_verify_password(self, pwd):
        return check_password_hash(self.password_, pwd)
    
class Menu(db.Model):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    ingredients: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)

class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    order: Mapped[dict] = mapped_column(JSON())
    user: Mapped[User] = relationship(foreign_keys='User.id', back_populates="orders")

class Reservation(db.Model):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime())
    table_number: Mapped[int] = mapped_column()
    numbers: Mapped[int] = mapped_column()
    user: Mapped[User] = relationship(foreign_keys='User.id', back_populates="reservations")

