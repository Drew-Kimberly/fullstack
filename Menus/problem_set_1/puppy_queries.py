__author__ = 'Admin'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ps1_db_setup import Base, Shelter, Puppy, Adopter, Adoption, PuppyProfile
import datetime
from dateutil import relativedelta

engine = create_engine('postgresql:///puppyshelter')
Base.metadata.bind = engine #makes connection between class definitions and corresponding db tables
DBSession = sessionmaker(bind = engine) #Session allows us to write db commands without sending to databse
                                        #until we commit the session.
session = DBSession()

#1) Query all of the uppies and return the results in ascending alphabetical order
# sorted_puppies = session.query(Puppy).order_by(Puppy.name.asc()).all()
#for puppy in sorted_puppies:
    #print(puppy.name)


#2) Query all of the puppies that are less than 6 months old organized by the youngest first
# six_months_ago = datetime.date.today() - relativedelta.relativedelta(months=6)
# youngest_puppies = session.query(Puppy).\
#                     filter(Puppy.birthDate > six_months_ago).\
#                     order_by(Puppy.birthDate).all()
# for puppy in youngest_puppies:
#     print(puppy.birthDate)


#3) Query all puppies by ascending weight
# puppies = session.query(Puppy).\
#             order_by(Puppy.weight.asc()).all()
# for puppy in puppies:
#     print(puppy.weight)


#4) Query all puppies grouped by the shelter in which they are staying
# puppies = session.query(Puppy).\
#             order_by(Puppy.shelter_id.asc()).all()
# for puppy in puppies:
#     print(puppy.name + " : " + puppy.shelter.name)


#Checks a puppy into a given shelter if the shelter capacity permits.
#If the shelter is already at capacity, let's the user know.
def checkPuppyIntoShelter(puppyName, puppyGender, shelterId, puppyBirthdate=None,
                          puppyWeight=None, puppyPicture=None):
    shelterRecord = session.query(Shelter).\
                     filter(Shelter.id == shelterId).one()
    if shelterRecord.maximumCapacity != None and shelterRecord.currentOccupancy == shelterRecord.maximumCapacity:
        print(shelterRecord.name + " is currently at maximum capacity, sorry!")
        return
    puppy = Puppy(
        name = puppyName,
        gender = puppyGender,
        birthDate = puppyBirthdate,
        weight = puppyWeight,
        picture = puppyPicture,
        shelter_id = shelterId
    )
    session.add(puppy)
    session.commit()

    #Must update the occupancy count for the shelter
    shelter = session.query(Shelter).filter(Shelter.id == puppy.shelter_id).one()
    if shelter.currentOccupancy != None:
        shelter.currentOccupancy += 1
        session.add(shelter)
        session.commit()


#Adopts a puppy based on its id. Accepts array of adopter ids of the family members
#who are responsible for the puppy. Adopted puppies should stay in the database
#but should no longer be taking up an occupancy spot in the shelter.
def adoptPuppy(puppyId, adopters):
    for adopter in adopters:
        session.add(Adoption( #Add an adoption entry for each adopter
            puppy_id = puppyId,
            adopter_id = adopter,
            adoption_time = datetime.datetime.utcnow()
        ))
        session.commit()
    puppy = session.query(Puppy).filter(Puppy.id == puppyId).one()
    shelter = session.query(Shelter).filter(Shelter.id == puppy.shelter_id).one()
    if shelter.currentOccupancy != None:
        shelter.currentOccupancy -= 1
        session.add(shelter)
        session.commit()


# checkPuppyIntoShelter("Coco", "female", 1, datetime.date.today() - datetime.timedelta(weeks=15), 32.113567)
# checkPuppyIntoShelter("Boxer", "male", 1, datetime.date.today() - datetime.timedelta(weeks=5), 132.35)

#Add adopters
# adopters = [
#     Adopter(
#         firstName = 'John',
#         lastName = 'Doe'
#     ),
#     Adopter(
#         firstName = 'Jane',
#         lastName = 'Doe'
#     ),
#     Adopter(
#         firstName = 'Sam',
#         lastName = 'Doe'
#     ),
#     Adopter(
#         firstName = 'Sally',
#         lastName = 'Doe'
#     ),
#     Adopter(
#         firstName = 'Drew',
#         lastName = 'Kimberly'
#     ),
# ]
# for adopter in adopters:
#     session.add(adopter)
#
# session.commit()

#adoptPuppy(103, [5])
adoptPuppy(103, [1, 2, 3, 4])
adoptPuppy(6, [1, 2, 3, 4])

puppy = session.query(Puppy).filter_by(id=103).one()
print(puppy.adopters[0].firstName)


