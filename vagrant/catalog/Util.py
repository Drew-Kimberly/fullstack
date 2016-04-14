# Utility functions/constants that can be used throughout the Catalog app.

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Returns True if the given file has an image file extension
def is_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Given a full filename, returns an array such that the first entry
# is the friendly file name (no extension) and the second entry
# is the file extension
def split_filename_and_extension(filename):
    pass
