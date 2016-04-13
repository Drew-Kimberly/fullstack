from werkzeug.routing import BaseConverter


class ItemConverter(BaseConverter):
    item = None

    def set_item(self, item):
        self.item = item

    def get_item(self):
        return self.item

    def to_python(self, value):
        return self.get_item()

    def to_url(self, value):
        self.set_item(value)
        return BaseConverter.to_url(self, value.name)


class CategoryConverter(BaseConverter):
    category = None

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def to_python(self, value):
        return self.get_category()

    def to_url(self, value):
        self.set_category(value)
        return BaseConverter.to_url(self, value.name)