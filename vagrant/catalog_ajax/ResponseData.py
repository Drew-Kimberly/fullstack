'''
ResponseData class will provide a serializable object
for representing the response data returned from the AjaxHandler.

Properties:
    Categories - Collection of Category objects (can be None)
    Items - Collection of Item Objects (can be None)
    templates - array of template names that will need to be re-rendered per the request
'''


class ResponseData:

    def __init__(self, categories, items, templates):
        self.categories = categories
        self.items = items
        self.templates = templates

