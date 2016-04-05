from database_setup import Item, Category
import bleach

class AjaxHandler:
    '''This class...'''

    def __init__(self, dbSessionMaker):
        '''
        '''
        self._dbSessionMaker = dbSessionMaker
        self._posted_data = None
        self.user_state = None
        self.action_context = None
        self.action_type = None

    # Properties

    @property
    def dbSessionMaker(self):
        return self._dbSessionMaker

    @property
    def posted_data(self):
        return self._posted_data

    @posted_data.setter
    def posted_data(self, value):
        self._posted_data = value

    # Methods

    def validateRequest(self):
        '''
        '''

        # Ensure we have posted data
        if not self.posted_data:
            return False

        # Ensure posted data contains an action
        if not self.posted_data["action"]:
            return False

        self.action_type = self.posted_data["action"]

        return True


    def processRequest(self):
        '''
        '''

        # Ensure request is good
        if not self.validateRequest():
            return None

        # Create SQLAlchemy Session
        dbSession = self.dbSessionMaker()

        # Determine request Action Type and execute respective logic
        if self.action_type == "RenderCatalog":
            categories = dbSession.query(Category).all()
            items = dbSession.query(Item).all()
            dbSession.close()
            template_name = 'catalog.html'
            return [template_name, categories, items]

        elif self.action_type == "GetCategories":
            categories = dbSession.query(Category).all()
            template_name = None
            dbSession.close()
            return [template_name, categories]

        elif self.action_type == "RenderCategories":
            categories = dbSession.query(Category).all()
            template_name = 'partials/catalog_categories.html'
            dbSession.close()
            return [template_name, categories]

        elif self.action_type == "AddCategory":
            name = self.posted_data["name"]
            dbSession.add(Category(name=name))
            dbSession.commit()
            categories = dbSession.query(Category).all()
            dbSession.close()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]

        elif self.action_type == "EditCategory":
            category_id = self.posted_data["id"]
            category_name = self.posted_data["name"]

            category_to_edit = dbSession.query(Category).filter_by(category_id=category_id).first()
            category_to_edit.name = category_name
            dbSession.add(category_to_edit)
            dbSession.commit()

            categories = dbSession.query(Category).all()
            dbSession.close()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]

        elif self.action_type == "DeleteCategory":
            category_id = self.posted_data["id"]
            category_to_delete = dbSession.query(Category).filter_by(category_id=category_id).first()
            dbSession.delete(category_to_delete)
            dbSession.commit()

            categories = dbSession.query(Category).all()
            dbSession.close()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]

        elif self.action_type == "GetItems":
            items = dbSession.query(Item).all()
            dbSession.close()

            template_name = None
            return [template_name, items]

        elif self.action_type == 'RenderItems':
            items = dbSession.query(Item).all()
            dbSession.close()

            template_name = 'partials/catalog_items.html'
            return [template_name, items]

        elif self.action_type == 'RenderItemForm':
            item_id = self.posted_data["item_id"]

            # Check if we're editing an existing item or adding a new one
            item = dbSession.query(Item).filter_by(item_id=item_id).first()
            if item:
                category_id = self.posted_data["category_id"]
                name = self.posted_data["name"]
                description = self.posted_data["description"]
                return ""
            else:
                categories = dbSession.query(Category).all()
                dbSession.close()
                template_name = 'partials/additem.html'
                return [template_name, categories]

        elif self.action_type == 'AddItem':
            item_name = self.posted_data["name"]
            item_category_id = self.posted_data["category_id"]
            item_description = self.posted_data["description"]

            # Add the item to database
            dbSession.add(Item(
                name=item_name,
                category_id=item_category_id,
                description=item_description
            ))
            dbSession.commit()

            # Retrieve list of all items to display
            items = dbSession.query(Item).all()
            dbSession.close()

            template_name = 'partials/catalog_items.html'
            return [template_name, items]

        else:
            dbSession.close()
            return None
