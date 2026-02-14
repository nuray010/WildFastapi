from platform import release
from tkinter import Image

from sqlalchemy.testing.pickleable import User

from .db import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean,DateTime
from typing import Optional,List
from enum import Enum as PyEnum
from datetime import date,datetime

class StatusChoices(str,PyEnum):
    gold='gold'
    silver='silver'
    bronze='bronze'
    simple ='simple'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    first_name:Mapped[str]=mapped_column(String(30))
    last_name:Mapped[str]=mapped_column(String(50))
    user_name:Mapped[str]=mapped_column(String,unique=True)
    email:Mapped[Optional[str]]=mapped_column(String,unique=True)
    password:Mapped[str]=mapped_column(String)
    age:Mapped[int]=mapped_column(Integer,nullable=True)
    phone_number:Mapped [Optional[int]]=mapped_column(String,nullable=True)
    status:Mapped[StatusChoices]=mapped_column(Enum(StatusChoices),default=StatusChoices.simple,nullable=True)
    date_registered:Mapped[date]=mapped_column(Date,default=date.today())
    user_reviews: Mapped[List['Review']] = relationship(back_populates='user', cascade='all, delete-orphan')
    refresh_tokens:Mapped[List['RefreshToken']] = relationship(back_populates='user_token', cascade='all, delete-orphan')


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('user_profile.id'))
    user_token:Mapped[UserProfile]=relationship(UserProfile,back_populates='refresh_tokens')
    token:Mapped[str] = mapped_column(String)
    create_date:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)










class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name:Mapped[str]=mapped_column(String(30),unique=True)
    category_image:Mapped[str]=mapped_column(String)

    sub_categories:Mapped[List['SubCategory']] = relationship('SubCategory',back_populates='category',cascade='all, delete-orphan')

def __repr__(self):
    return f'{self.category_name}'


class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_category_name:Mapped[str]=mapped_column(String(30))
    category_id:Mapped[int]=mapped_column(ForeignKey('category.id'))

    category: Mapped[Category]=relationship(Category,back_populates='sub_categories')
    products:Mapped[List['Product']] = relationship(back_populates='sub_category',cascade='all, delete-orphan')



class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_category_id:Mapped[int]=mapped_column(ForeignKey('sub_category.id'))

    sub_category:Mapped[SubCategory]=relationship(back_populates='products')

    product_name:Mapped[str]=mapped_column(String(30))
    price:Mapped[int]=mapped_column(Integer)
    article_number:Mapped[int]=mapped_column(Integer)
    description:Mapped[str]=mapped_column(Text)
    video:Mapped[Optional[str]]=mapped_column(String,nullable=True)
    product_type: Mapped[bool] = mapped_column(Boolean)
    created_date:Mapped[date]=mapped_column(Date,default=date.today())

    images:Mapped[List['ProductImage']]=relationship(back_populates='product',cascade='all, delete-orphan')
    product_reviews:Mapped[List['Review']] =relationship(back_populates='product_rev',cascade='all, delete-orphan')


class ProductImage(Base):
    __tablename__ = 'product_image'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image:Mapped[str]=mapped_column(String)
    product_id:Mapped[int]=mapped_column(ForeignKey('product.id'))

    product: Mapped[Product]=relationship(back_populates='images')


class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship(back_populates='user_reviews')

    product_id:Mapped[int]=mapped_column(ForeignKey('product.id'))

    product_rev:Mapped[Product]=relationship(back_populates='product_reviews')

    text:Mapped[str]=mapped_column(Text)
    stars:Mapped[int]=mapped_column(Integer)
    created_date:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)





