#Inserts new data into our Menu database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('postgresql:///menus')
Base.metadata.bind = engine #makes connection between class definitions and corresponding db tables
DBSession = sessionmaker(bind = engine) #Session allows us to write db commands without sending to databse
                                        #until we commit the session.
session = DBSession()

# #Add a restaurant to the database
# firstRestaurant = Restaurant(name = "Pizza Palace")
# #session.add(firstRestaurant)
#
# #Add menu item
# cheese_pizza = MenuItem(
#     name = "Cheese Pizza",
#     description = "Made with all natural ingredients and fresh mozzarella",
#     course = "Entree",
#     price = "$8.99",
#     restaurant = firstRestaurant
# )
# session.add(cheese_pizza)
# session.commit()

# #Reading data with sqlAlchemy
# firstResult = session.query(Restaurant).first()
# print(firstResult.name)
#
# items = session.query(MenuItem).all()
# for item in items:
#     print(item.name)

#Update data with sqlAlchemy
#SELECT * FROM restaurant r JOIN menu_item mi on r.id=mi.restaurant_id
#WHERE mi.name='Veggie Burger' AND r.name='Urban Burger'
#LIMIT 1;
# urban_veggieBurger = session.query(MenuItem).\
#     join(MenuItem.restaurant).\
#     filter(MenuItem.name == 'Veggie Burger').\
#     filter(Restaurant.name == 'Urban Burger').first()
#
# urban_veggieBurger.price = '$2.99'
# session.add(urban_veggieBurger)
# session.commit()


#Delete data from db
# spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
# session.delete(spinach)
# session.commit()