import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, DateTime, Table, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import datetime

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(300), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zipCode = Column(String(25), nullable=False)
    website = Column(String)
    maximumCapacity = Column(Integer)
    currentOccupancy = Column(Integer)

    #Check Constraint
    #CheckConstraint(currentOccupancy <= maximumCapacity)


class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    special_needs = Column(String)
    picture = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    birthDate = Column(Date)
    gender = Column(String(20), nullable=False)
    weight = Column(Numeric)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    puppyProfile = relationship(PuppyProfile, uselist=False, backref="puppy") #One-One relationship with PuppyProfile
    adopters = relationship('Adopter', secondary='adoption') #Many-to-Many relationship


class Adopter(Base):
    __tablename__ = 'adopter'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(100))
    puppies = relationship(Puppy, secondary='adoption')


class Adoption(Base):
    __tablename__ = 'adoption'

    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    adopter_id = Column(Integer, ForeignKey('adopter.id'))
    adoption_time = Column(DateTime, default=datetime.datetime.utcnow())
    puppy = relationship(Puppy, backref=backref("adopter_assoc"))
    adopter = relationship(Adopter, backref=backref("puppy_assoc"))


engine = create_engine('postgresql:///puppyshelter')
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)