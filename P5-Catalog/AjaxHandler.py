import os
from flask import session, make_response
from database_setup import Item, Category, ItemImage
from ResponseData import ResponseData
import Util
from werkzeug.utils import secure_filename
import json

CATEGORY_TEMPLATE = 'partials/catalog_categories.html'
ITEM_TEMPLATE = 'partials/catalog_items.html'

UNRESTRICTED_ACTIONS = {'RenderCatalog', 'RenderItemForm', 'SelectItem'}


class AjaxHandler:
    '''
    Incoming AJAX requests are handed off to this class by the route controller
    for validation and processing
    '''

    def __init__(self, db_session):

        self._db_session = db_session
        self._posted_data = None
        self._posted_file = None
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
        Performs basic validation on an incoming request from the Catalog app.
        '''

        # Ensure we have posted data
        if not self.posted_data:
            response = make_response(json.dumps({"error": "Invalid request."}), 500)
            return response

        # Ensure posted data contains an action
        if not self.posted_data["action"]:
            response = make_response(json.dumps({"error": "Invalid request."}), 500)
            return response

        # Ensure user is authenticated when making restricted calls
        if not session.get('username') and self.posted_data["action"] not in UNRESTRICTED_ACTIONS:
            response = make_response(json.dumps({"error": "User is not authenticated."}), 401)
            return response

        self.action_type = self.posted_data["action"]
        response = make_response(json.dumps({"success": "Valid request."}), 200)
        return response

    def processRequest(self):
        '''
        Does the work prompted by the posted request's given action_type.
        '''

        # Ensure request is good
        validation_response = self.validateRequest()
        if validation_response.status_code != 200:
            print(validation_response.response[0])
            return None

        # Determine request Action Type and execute respective logic
        if self.action_type == "RenderCatalog":
            categories = self.db_session.query(Category).all()
            items = self.db_session.query(Item).all()
            templates = [CATEGORY_TEMPLATE, ITEM_TEMPLATE]
            return ResponseData(categories, items, templates)

        elif self.action_type == "AddCategory":
            name = self.posted_data["name"]
            user_id = session.get('user_id')
            try:
                self.db_session.add(Category(name=name, user_id=user_id))
                self. db_session.commit()
            except Exception as e:
                print("Error adding category. - %s" % e.message)
                self.db_session.rollback()

            categories = self.db_session.query(Category).all()
            templates = [CATEGORY_TEMPLATE]
            return ResponseData(categories, None, templates)

        elif self.action_type == "EditCategory":
            category_id = self.posted_data["id"]
            category_name = self.posted_data["name"]

            category_to_edit = self.db_session.query(Category).filter_by(category_id=category_id).first()

            # Sanity check for user authorization
            if category_to_edit.user_id == session.get('user_id'):
                try:
                    category_to_edit.name = category_name
                    self.db_session.add(category_to_edit)
                    self.db_session.commit()
                except Exception as e:
                    print("Error editing category - {0}".format(e.message))
                    self.db_session.rollback()

                categories = self.db_session.query(Category).all()
                templates = [CATEGORY_TEMPLATE]
                return ResponseData(categories, None, templates)
            else:
                # Throw 403 Error
                print("User is not authorized to perform this action")
                return make_response(json.dumps("403 - User is not authorized"), 403)

        elif self.action_type == "DeleteCategory":
            category_id = self.posted_data["id"]
            images_to_delete = []
            is_error = False

            # Query for the category and its associated Items
            category_to_delete = self.db_session.query(Category).filter_by(category_id=category_id).first()
            category_items = self.db_session.query(Item).filter_by(category_id=category_id).all()

            # Sanity check for user authorization
            if category_to_delete.user_id == session.get('user_id'):
                try:
                    if len(category_items) > 0:
                        item_template = ITEM_TEMPLATE
                        for item in category_items:
                            if item.user_id == session.get('user_id'):
                                # Can only delete category if you own the category AND all items associated to it
                                # Wonky business-logic :/ Also highlights the need for roles in a permissioning system
                                if item.image_id:
                                    image = self.db_session.query(ItemImage).filter_by(image_id=item.image_id).first()
                                    images_to_delete.append(str(image.image_id) + image.extension)

                                    # Remove Image ref from Item entity
                                    item.image_id = None

                                    # Remove Image entity from db
                                    self.db_session.delete(image)

                                # Remove Item entity from db
                                self.db_session.delete(item)
                            else:
                                # User does not own every item within the category
                                is_error = True
                                error_message = "Delete Category Failed - " \
                                                "This category contains items which you do not own"
                                print(error_message)
                                self.db_session.rollback()
                    else:
                        item_template = None

                    # Delete the Category
                    if not is_error:
                        self.db_session.delete(category_to_delete)

                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    if issubclass(type(e), OSError):
                        print("Error deleting category - {0}".format(e.strerror))
                    else:
                        print("Error deleting category - {0}".format(e.message))

                if not is_error:
                    try:
                        self.db_session.commit()
                    except Exception as e:
                        print("Error deleting category - {0}".format(e.message))
                        self.db_session.rollback()

                    # Finally remove images from filesystem. Have to do this after the commit to
                    # prevent users from deleting a category in which they only own some of the associated items
                    for image_name in images_to_delete:
                        os.remove(os.path.join(Util.UPLOAD_FOLDER, image_name))

                categories = self.db_session.query(Category).all()
                if item_template:
                    items = self.db_session.query(Item).all()
                else:
                    items = None

                return ResponseData(categories, items, [CATEGORY_TEMPLATE, item_template])
            else:
                # Throw 403
                print("User is not authorized to perform this action")
                return make_response(json.dumps("User is not authorized"), 403)

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
            user_id = session.get('user_id')
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
                            image_id=item_image.image_id,
                            user_id=user_id
                        ))
                    except Exception as e:
                        is_error = True
                        self.db_session.rollback()
                        print("Error adding item - {0}".format(e.message))

                    # Save image to filesystem (static/img/)
                    if not is_error:
                        try:
                            self.posted_file.save(
                                os.path.join(Util.UPLOAD_FOLDER, str(item_image.image_id)+item_image.extension))
                        except Exception as e:
                            is_error = True
                            self.db_session.rollback()
                            if issubclass(type(e), OSError):
                                print("Error adding item - {0}".format(e.strerror))
                            else:
                                print("Error adding item - {0}".format(e.message))

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
                        description=item_description,
                        user_id=user_id
                    ))
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    print("Error adding item - {0}".format(e.message))

            if not is_error:
                try:
                    self.db_session.commit()
                except Exception as e:
                    print("Error adding item - {0}".format(e.message))
                    self.db_session.rollback()

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
            is_error = False
            item_id = self.posted_data["item_id"]
            item_to_delete = self.db_session.query(Item).filter_by(item_id=item_id).first()
            image_id = None
            image_ext = None

            # Sanity check for user authorization
            if item_to_delete.user_id == session.get('user_id'):
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
                        print("Error deleting item - {0}".format(e.message))

                try:
                    self.db_session.delete(item_to_delete)
                    if image_id and image_ext:
                        os.remove(os.path.join(Util.UPLOAD_FOLDER, str(image_id)+image_ext))
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    if issubclass(type(e), OSError):
                        print("Error deleting item - {0}".format(e.strerror))
                    else:
                        print("Error deleting item - {0}".format(e.message))

                if not is_error:
                    try:
                        self.db_session.commit()
                    except Exception as e:
                        print("Error deleting item - {0}".format(e.message))
                        self.db_session.rollback()

                # Query and return all items
                items = self.db_session.query(Item).all()
                templates = [ITEM_TEMPLATE]
                return ResponseData(None, items, templates)
            else:
                # Throw a 403
                print("User is unauthorized to perform this action")
                return make_response(json.dumps("User is unathorized."), 403)

        elif self.action_type == 'EditItem':
            is_error = False
            item_id = self.posted_data["item_id"]
            has_file = self.posted_data["has_file"]
            item_to_edit = self.db_session.query(Item).filter_by(item_id=item_id).first()
            image_id = item_to_edit.image_id

            # Sanity check for user authorization
            if item_to_edit.user_id == session.get('user_id'):
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
                                print("Error editing item - {0}".format(e.message))
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
                                print("Error editing item - {0}".format(e.message))

                        # Save uploaded image to filesystem (/static/img/)
                        if not is_error:
                            try:
                                self.posted_file.save(
                                    os.path.join(Util.UPLOAD_FOLDER, str(item_image.image_id) + item_image.extension))
                            except Exception as e:
                                is_error = True
                                self.db_session.rollback()
                                if issubclass(type(e), OSError):
                                    print("Error editing item - {0}".format(e.strerror))
                                else:
                                    print("Error editing item - {0}".format(e.message))

                    else:
                        # Not an image - BAD REQUEST (shouldn't have gotten through client-side validation)
                        is_error = True
                        error_message = "Uploaded file must be an image format."
                        pass
                elif image_id and not has_file:
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
                        print("Error editing item - {0}".format(e.message))

                    # Remove the image file from the File System
                    try:
                        os.remove(os.path.join(Util.UPLOAD_FOLDER, str(image_id) + image_extension))
                    except Exception as e:
                        is_error = True
                        self.db_session.rollback()
                        if issubclass(type(e), OSError):
                            print("Error editing item - {0}".format(e.strerror))
                        else:
                            print("Error editing item - {0}".format(e.message))

                # Add non-image related posted data to the Item
                try:
                    item_to_edit.name = self.posted_data["item_name"]
                    item_to_edit.category_id = self.posted_data["category_id"]
                    item_to_edit.description = self.posted_data["description"]
                    self.db_session.add(item_to_edit)
                except Exception as e:
                    is_error = True
                    self.db_session.rollback()
                    print("Error editing item - {0}".format(e.message))

                if not is_error:
                    try:
                        self.db_session.commit()
                    except Exception as e:
                        print("Error editing item - {0}".format(e.message))
                        self.db_session.rollback()

                items = self.db_session.query(Item).all()
                templates = [ITEM_TEMPLATE]
                return ResponseData(None, items, templates)

            else:
                # Throw a 403
                print("User is not authorized to perform this action")
                return make_response(json.dumps("User is unauthorized"), 403)

        else:
            return None
