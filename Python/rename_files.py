import os
import string

def rename_files():
    path = "E:\\\\Udacity\\Python\\prank\\"
    files = os.listdir(path)

    for file in files:
        os.rename(path + file, path + ''.join(filter(lambda c: not c.isdigit(), str(file))))
        

rename_files()
