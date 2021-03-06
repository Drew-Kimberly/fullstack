import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id')) #Creates foreign key relationship

    restaurant = relationship(Restaurant) #Gives access to the restaurant instance (?)








engine = create_engine('postgresql:///menus')
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)