import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(80), nullable=False)
    category_id = Column(Integer, primary_key=True)


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship(Category)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'item_id' : self.item_id,
        }



engine = create_engine('postgresql:///catalog')
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)