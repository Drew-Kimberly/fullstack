import os
from database_setup import Item, Category, ItemImage
from ResponseData import ResponseData
import Util
from werkzeug.utils import secure_filename

CATEGORY_TEMPLATE = 'partials/catalog_categories.html'
ITEM_TEMPLATE = 'partials/catalog_items.html'


class AjaxHandler:

    '''This class...'''

    def __init__(self, db_session):
        '''
        '''
        self._db_session = db_session
        self._posted_data = None
        self._posted_file = None
        self.user_state = None
        self.action_context = None
        self.action_type = None

    # Properties

    @property
    def db_session(self):
        return self._db_session

    @property
    def posted_data(self):
        return self._posted_data

    @posted_data.setter
    def posted_data(self, value):
        self._posted_data = value

    @property
    def posted_file(self):
        return self._posted_file

    @posted_file.setter
    def posted_file(self, value):
        self._posted_file = value


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
            categories = self.db_session.query(Category).all()
            items = self.db_session.query(Item).all()
            templates = [CATEGORY_TEMPLATE, ITEM_TEMPLATE]
            return ResponseData(categories, items, templates)

        elif self.action_type == "GetCategories":
            categories = self.db_session.query(Category).all()
            template_name = None
            return [template_name, categories]

        elif self.action_type == "RenderCategories":
            categories = self.db_session.query(Category).all()
            template_name = 'partials/catalog_categories.html'
            return [template_name, categories]

        elif self.action_type == "AddCategory":
            name = self.posted_data["name"]
            self.db_session.add(Category(name=name))
            self. db_session.commit()
            categories = self.db_session.query(Category).all()

            templates = [CATEGORY_TEMPLATE]
            return ResponseData(categories, None, templates)

        elif self.action_type == "EditCategory":
            category_id = self.posted_data["id"]
            category_name = self.posted_data["name"]

            category_to_edit = self.db_session.query(Category).filter_by(category_id=category_id).first()
            category_to_edit.name = category_name
            self.db_session.add(category_to_edit)
            self.db_session.commit()

            categories = self.db_session.query(Category).all()
            templates = [CATEGORY_TEMPLATE]
            return ResponseData(categories, None, templates)

        elif self.action_type == "DeleteCategory":
            category_id = self.posted_data["id"]
            category_to_delete = self.db_session.query(Category).filter_by(category_id=category_id).first()
            category_items = self.db_session.query(Item).filter_by(category_id=category_id).all()
            if len(category_items) > 0:
                item_template = ITEM_TEMPLATE
                for item in category_items:
                    self.db_session.delete(item)
            else:
                item_template = None
            self.db_session.delete(category_to_delete)
            self.db_session.commit()

            categories = self.db_session.query(Category).all()
            if item_template:
                items = self.db_session.query(Item).all()
            else:
                items = None

            return ResponseData(categories, items, [CATEGORY_TEMPLATE, ITEM_TEMPLATE])

        elif self.action_type == "GetItems":
            items = self.db_session.query(Item).all()

            template_name = None
            return [template_name, items]

        elif self.action_type == 'RenderItems':
            items = self.db_session.query(Item).all()

            template_name = 'partials/catalog_items.html'
            return [template_name, items]

        elif self.action_type == 'RenderItemForm':
            item_id = self.posted_data["item_id"]
            categories = self.db_session.query(Category).all()

            # Check if we're editing an existing item or adding a new one
            item = self.db_session.query(Item).filter_by(item_id=item_id).first()
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
            is_error = False

            if self.posted_file:
                if Util.is_image(self.posted_file.filename):
                    try:
                        image_name = secure_filename(self.posted_file.filename)
                        item_image = ItemImage(
                            name=image_name,
                            extension=os.path.splitext(image_name)[1],
                            friendly_name=os.path.splitext(image_name)[0],
                            size=self.posted_data["file_size"],
                            type=self.posted_data["file_type"]
                        )
                        self.db_session.add(item_image)
                        self.db_session.flush()

                        self.db_session.add(Item(
                            name=item_name,
                            category_id=item_category_id,
                            description=item_description,
                            image_id=item_image.image_id
                        ))
                    except Exception as e:
                        is_error = True
                        self.db_session.rollback()
                        print(e.message)

                    # Save image to filesystem (static/img/)
                    if not is_error:
                        try:
                            self.posted_file.save(
                                os.path.join(Util.UPLOAD_FOLDER, str(item_image.image_id)+item_image.extension))
                        except Exception as e:
                            is_error = True
                            self.db_session.rollback()
                            if issubclass(type(e), OSError):
                                print(e.strerror)
                            else:
                                print(e.message)

                else:
                    # Not an image - flash error message and do not save item
                    is_error = True
                    error_message = "Uploaded file must be an image format."
                    pass
            else:
                # No Image Uploaded
                try:
                    self.db_session.add(Item(
                        name=item_name,
                        category_id=item_category_id,
                        description=item_description
                    ))
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    print(e.message)

            if not is_error:
                self.db_session.commit()

            # Retrieve list of all items to display
            items = self.db_session.query(Item).all()

            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        elif self.action_type == 'SelectItem':
            item_id = self.posted_data["item_id"]
            selected_item = [self.db_session.query(Item).filter_by(item_id=item_id).first()]
            category = [selected_item[0].category]
            templates = ['partials/viewitem.html']
            return ResponseData(category, selected_item, templates)

        elif self.action_type == 'DeleteItem':
            # Delete Item from database
            item_id = self.posted_data["item_id"]
            item_to_delete = self.db_session.query(Item).filter_by(item_id=item_id).first()
            is_error = False
            image_id = None
            image_ext = None
            if item_to_delete.image_id:
                image_id = item_to_delete.image_id
                image_ext = item_to_delete.image.extension

                # Delete Image entity from database
                try:
                    image = self.db_session.query(ItemImage).filter_by(image_id=image_id).first()
                    self.db_session.delete(image)
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    print(e.message)

            try:
                self.db_session.delete(item_to_delete)
                if image_id and image_ext:
                    os.remove(os.path.join(Util.UPLOAD_FOLDER, str(image_id)+image_ext))
            except Exception as e:
                is_error = True
                self.db_session.rollback()
                if issubclass(type(e), OSError):
                    print(e.strerror)
                else:
                    print(e.message)

            if not is_error:
                self.db_session.commit()

            # Query and return all items
            items = self.db_session.query(Item).all()
            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        elif self.action_type == 'EditItem':
            is_error = False
            item_id = self.posted_data["item_id"]
            item_to_edit = self.db_session.query(Item).filter_by(item_id=item_id).first()
            image_id = item_to_edit.image_id

            if self.posted_file:
                if Util.is_image(self.posted_file.filename):
                    image_name = secure_filename(self.posted_file.filename)
                    image_extension = os.path.splitext(image_name)[1]
                    image_friendly_name = os.path.splitext(image_name)[0]
                    image_size = self.posted_data["file_size"],
                    image_type = self.posted_data["file_type"]

                    if image_id:
                        # Item already has an associated image
                        try:
                            item_image = self.db_session.query(ItemImage).filter_by(image_id=image_id).first()
                            item_image.name = image_name
                            item_image.extension = image_extension
                            item_image.friendly_name = image_friendly_name
                            item_image.size = image_size
                            item_image.type = image_type

                            self.db_session.add(item_image)
                        except Exception as e:
                            is_error = True
                            self.db_session.rollback()
                            print(e.message)
                    else:
                        # Item has no associated image
                        try:
                            item_image = ItemImage(
                                name=image_name,
                                extension=image_extension,
                                friendly_name=image_friendly_name,
                                size=image_size,
                                type=image_type
                            )
                            self.db_session.add(item_image)
                            self.db_session.flush()

                            item_to_edit.image_id = item_image.image_id
                        except Exception as e:
                            is_error = True
                            self.db_session.rollback()
                            print(e.message)

                    # Save uploaded image to filesystem (/static/img/)
                    if not is_error:
                        try:
                            self.posted_file.save(
                                os.path.join(Util.UPLOAD_FOLDER, str(item_image.image_id) + item_image.extension))
                        except Exception as e:
                            is_error = True
                            self.db_session.rollback()
                            if issubclass(type(e), OSError):
                                print(e.strerror)
                            else:
                                print(e.message)

                else:
                    # Not an image - BAD REQUEST (shouldn't have gotten through client-side validation)
                    is_error = True
                    error_message = "Uploaded file must be an image format."
                    pass
            elif image_id:
                # Case where user deletes previous image and posts Item without uploading a new image
                image_extension = item_to_edit.image.extension

                # Disassociate the Item with the image's ID
                item_to_edit.image_id = None

                # Remove the Image from the ItemImage table
                try:
                    item_image = self.db_session.query(ItemImage).filter_by(image_id=image_id).first()
                    self.db_session.delete(item_image)
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    print(e.message)

                # Remove the image file from the File System
                try:
                    os.remove(os.path.join(Util.UPLOAD_FOLDER, str(image_id) + image_extension))
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    if issubclass(type(e), OSError):
                        print(e.strerror)
                    else:
                        print(e.message)

            # Add non-image related posted data to the Item
            try:
                item_to_edit.name = self.posted_data["item_name"]
                item_to_edit.category_id = self.posted_data["category_id"]
                item_to_edit.description = self.posted_data["description"]
                self.db_session.add(item_to_edit)
            except Exception as e:
                is_error = True
                self.db_session.rollback()
                print(e.message)

            if not is_error:
                self.db_session.commit()

            items = self.db_session.query(Item).all()
            templates = [ITEM_TEMPLATE]
            return ResponseData(None, items, templates)

        else:
            return None
