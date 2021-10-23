from flask_login import UserMixin
import json

class User(UserMixin):
    def __init__(self,email,name,username,password,profile_image):
        self.email=email
        self.name=name
        self.username=username
        self.password=password
        self.profile_image=profile_image
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.email

class UsersDB(UserMixin):
    
    def getUser(self,email):
        with open ('user_data.json','r+') as data_file:
            file_data=json.load(data_file)
            for user in file_data['user_details']:
                if user.get('Email') == email:
                    return user
            else:
                return None
    def getAllUser(self):
        with open('user_data.json','r+') as data_file:
            file_data=json.load(data_file)
            return(file_data['user_details'])
    def getUserByUserName(self,username):
        with open ('user_data.json','r+') as data_file:
            file_data=json.load(data_file)
            for user in file_data['user_details']:
                if user.get('Username') == username:
                    return user
            else:
                return None
    
    def update_image(self, email, image):
        with open ('user_data.json','r+') as data_file:
            file_data=json.load(data_file)
            for user in file_data['user_details']:
                if user.get('Email') == email:
                    user['Picture']=image