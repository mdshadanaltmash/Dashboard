import os
from PIL import Image
from flask import url_for,current_app

def add_profile_pic(pic_updload,username):
    filename=pic_updload.filename
    ext_type=filename.split('.')[-1]

    storage_filename=str(username)+'.'+ext_type
    file_path=os.path.join(current_app.root_path,'static\profile_pics',storage_filename)
    output_size=(200,200)
    pic=Image.open(pic_updload)
    pic.thumbnail(output_size)
    pic.save(file_path)

    return storage_filename