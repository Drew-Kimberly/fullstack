from database_setup import Item, Category
from ResponseData import ResponseData

CATEGORY_TEMPLATE = 'partials/catalog_categories.html'
ITEM_TEMPLATE = 'partials/catalog_items.html'


class AjaxHandler:

    '''This class...'''

    def __init__(self, dbSession):
        '''
        '''
        self._dbSession = dbSession
        self._posted_data = None
        self.user_state = None
        self.action_context = None
        self.action_type = None

    # Properties

    @property
    def dbSession(self):
        return self._dbSession

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

        # Determine request Action Type and execute respective logic
        if self.action_type == "RenderCatalog":
            categories = self.dbSession.query(Category).all()
            items = self.dbSession.query(Item).all()
            templates = [CATEGORY_TEMPLATE, ITEM_TEMPLATE]
            return ResponseData(categories, items, templates)

        elif self.action_type == "GetCategories":
            categories = self.dbSession.query(Category).all()
            template_name = None
            return [template_name, categories]

        elif self.action_type == "RenderCategories":
            categories = self.dbSession.query(Category).all()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]

        elif self.action_type == "AddCategory":
            name = self.posted_data["name"]
            self.dbSession.add(Category(name=name))
            self. dbSession.commit()
            categories = self.dbSession.query(Category).all()

            templates = [CATEGORY_TEMPLATE]
            return ResponseData(categories, None, templates)

        elif self.action_type == "EditCategory":
            category_id = self.posted_data["id"]
            category_name = self.posted_data["name"]

            category_to_edit = self.dbSession.query(Category).filter_by(category_id=category_id).first()
            category_to_edit.name = category_name
            self.dbSession.add(category_to_edit)
            self.dbSession.commit()

            categories = self.dbSession.query(Category).all()
            templates = [CATEGORY_TEMPLATE]
            return ResponseData(categories, None, templates)

        elif self.action_type == "DeleteCategory":
            category_id = self.posted_data["id"]
            category_to_delete = self.dbSession.query(Category).filter_by(category_id=category_id).first()
            category_items = self.dbSession.query(Item).filter_by(category_id=category_id).all()
            if len(category_items) > 0:
                item_template = ITEM_TEMPLATE
                for item in category_items:
                    self.dbSession.delete(item)
            else:
                item_template = None
            self.dbSession.delete(category_to_delete)
            self.dbSession.commit()

            categories = self.dbSession.query(Category).all()
            if item_template:
                items = self.dbSession.query(Item).all()
            else:
                items = None

            return ResponseData(categories, items, [CATEGORY_TEMPLATE, ITEM_TEMPLATE])

        elif self.action_type == "GetItems":
            items = self.dbSession.query(Item).all()

            template_name = None
            return [template_name, items]

        elif self.action_type == 'RenderItems':
            items = self.dbSession.query(Item).all()

            template_name = 'partials/catalog_items.html'
            return [template_name, items]

        elif self.action_type == 'RenderItemForm':
            item_id = self.posted_data["item_id"]
            categories = self.dbSession.query(Category).all()

            # Check if we're editing an existing item or adding a new one
            item = self.dbSession.query(Item).filter_by(item_id=item_id).first()
            if item:
                templates = ['partials/edititem.html']
                return ResponseData(categories, [item], templates)
            else:
                templates = ['partials/additem.html']
                return ResponseData(categories, None, templates)

        elif self.action_type == 'AddItem':
            item_name = self.posted_data["name"]
            item_category_id = self.posted_data["category_id"]
            item_description = self.posted_data["description"]

            # Add the item to database
            self.dbSession.add(Item(
                name=item_name,
                category_id=item_category_id,
                description=item_description
            ))
            self.dbSession.commit()

            # Retrieve list of all items to display
            items = self.dbSession.query(Item).all()

            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        elif self.action_type == 'SelectItem':
            item_id = self.posted_data["item_id"]
            selected_item = [self.dbSession.query(Item).filter_by(item_id=item_id).first()]
            category = [selected_item[0].category]
            templates = ['partials/viewitem.html']
            return ResponseData(category, selected_item, templates)

        elif self.action_type == 'DeleteItem':
            item_id = self.posted_data["item_id"]
            item_to_delete = self.dbSession.query(Item).filter_by(item_id=item_id).first()
            self.dbSession.delete(item_to_delete)
            self.dbSession.commit()

            items = self.dbSession.query(Item).all()
            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        elif self.action_type == 'EditItem':
            item_id = self.posted_data["item_id"]
            item_to_edit = self.dbSession.query(Item).filter_by(item_id=item_id).first()
            item_to_edit.name = self.posted_data["item_name"]
            item_to_edit.category_id = self.posted_data["category_id"]
            item_to_edit.description = self.posted_data["description"]
            self.dbSession.add(item_to_edit)
            self.dbSession.commit()

            items = self.dbSession.query(Item).all()
            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        else:
            return None
