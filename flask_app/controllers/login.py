from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods = ["POST"])
def register_user():
        if not User.validate_user_info(request.form):
            return redirect('/')
        data ={
            'first_name': request.form['first_name'],
            'last_name': request.form ['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user = User.create_user(data)
        session['id']= user
        session['first_name']= request.form['first_name']
        return redirect('/success')

@app.route('/success')
def success():
    if 'id' not in session:
        flash('Please log in to view this page')
        return redirect('/')
    return render_template('success.html')

@app.route('/login/user', methods=["POST"])
def login_user():
    users = User.get_user_email(request.form)
    if len(users)!= 1:
        flash('User does not exist. Please register!')
        return redirect('/')
    user = users[0]
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Password for the given user is incorrect.")
        return redirect('/')
    session['id']= user.id
    session['first_name']= user.first_name
    return redirect('/success')

@app.route('/logout/user')
def logout_user():
    session.clear()
    return redirect('/')
    