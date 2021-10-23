from admin_dashboard import app, login_manager
from flask import redirect,url_for,flash,request
from flask.templating import render_template
from admin_dashboard.forms import LoginForm, RegistrationForm, UpdateAccount
import json
import os
from admin_dashboard.models import User, UsersDB
from admin_dashboard.picture_handler import add_profile_pic
from flask_login import login_user,logout_user,login_required,current_user


@app.route('/')
def home():
    return  render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_records = UsersDB()
    user = user_records.getAllUser()
    user_account_type = user_records.getUser(current_user.email)['Account_Type']
    return render_template('dashboard.html',user=user, total_user = len(user),account_type=user_account_type,
            current_user=current_user)

@app.route('/about',methods=['GET','POST'])
@login_required
def about():
    form=UpdateAccount()
    if form.validate_on_submit():
        if form.profile_image.data:
            print('yes')
            username=current_user.username
            pic=add_profile_pic(form.profile_image.data,username)
        return(redirect(url_for('about')))
    profile_image=url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('about.html',form=form,profile_image=profile_image)

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_records = UsersDB()
        user = user_records.getUser(email)
        if user:
            if user.get('Password') == password:
                if user.get('Account_Type')==form.account_type.data:
                    login_user(User(user['Email'],user['Name'],user['Username'],user['Password'],user['Picture']))
                    flash('You have been Logged In!')
                    next=request.args.get('next')
                    if next is None or next[0]=='/':
                        next=url_for('welcome_user')
                    return(redirect(next))
                else:
                    msg=f"You are not {form.account_type.data}"
                    redirect(url_for('login'))
            else:
                msg='Invalid Username/Password'
                redirect(url_for('login'))
        else:
            msg='Invalid Username/Password'
            redirect(url_for('login'))
    return render_template('login.html',form=form, msg=msg)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('home'))

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        pic='static/profile_pics/default.png'
        if form.profile_image.data:
            print('yes')
            username=current_user.username
            pic=add_profile_pic(form.profile_image.data,username)
        user_details = {
            'Name': form.f_name.data,
            'Email': form.email.data,
            'Username': form.username.data,
            'Password': form.password.data,
            'Picture': pic,
            'Gender': form.gender.data,
            'Education': form.education.data,
            'Hobbies': request.form.getlist("mycheckbox"),
            'Status': 'Active',
            'Account_Type': 'Normal'
        }
        
        print(user_details)
        with open ('user_data.json','r+') as data_file:
            file_data=json.load(data_file)
            file_data['user_details'].append(user_details)
            data_file.seek(0)
            json.dump(file_data,data_file, indent = 4)
        return redirect(url_for('login'))

    return render_template('register.html',form=form)


@login_manager.user_loader
def load_user(email):
    user_records = UsersDB()
    user = user_records.getUser(email)
    if not user:
        return None
    return User(user['Email'],user['Name'],user['Username'],user['Password'],user['Picture'])

if __name__=='__main__':
    app.run(debug=True)
