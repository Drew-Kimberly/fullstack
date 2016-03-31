from database_setup import Item, Category

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
        if self.action_type == "testAjax":
            return self.posted_data["id"]
        elif self.action_type == "GetCategories":
            categories = self.dbSession.query(Category).all()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]
        else:
            return None
