import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

'''
I didn't like wiping my data when recreating my database every time a schema update was needed,
so I began using Alembic, an open sourced db migration tool built on top of SQLAlchemy.
Really cool and easy, especially with the autogeneration feature!
Docs can be found here: https://alembic.readthedocs.org/en/latest/
'''


Base = declarative_base()


class User(Base):
    __tablename__ = 'catalog_user'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))
    name = Column(String(100), nullable=False)


class ItemImage(Base):
    __tablename__ = 'item_image'

    image_id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    friendly_name = Column(String(80), nullable=False)
    extension = Column(String(8), nullable=False)
    size = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'image_id': self.image_id,
            'name': self.name,
            'friendly_name': self.friendly_name,
            'extension': self.extension,
            'size': self.size,
            'type': self.type
        }


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(80), nullable=False, unique=True)
    category_id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('catalog_user.user_id'), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'category_id': self.category_id,
            'created_on': str(self.created_on),
            'last_updated': str(self.last_updated),
            'user_id': self.user_id
        }


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=func.now())  # PostgreSQL
    # created_on = Column(TIMESTAMP, nullable=False)  # MySQL
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())  # PostgreSQL
    # last_updated = Column(TIMESTAMP, nullable=False)  # MySQL
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    image_id = Column(Integer, ForeignKey('item_image.image_id'), nullable=True)
    user_id = Column(Integer, ForeignKey('catalog_user.user_id'), nullable=False)
    category = relationship(Category)
    image = relationship(ItemImage)
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'description': self.description,
            'item_id': self.item_id,
            'created_on': str(self.created_on),
            'last_updated': str(self.last_updated),
        }


engine = create_engine('postgresql:///catalog')
# engine = create_engine('mysql://andkim:andkim@localhost:3306/catalog', pool_recycle=3600)
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
