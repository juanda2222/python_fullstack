
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user

from SanchoApp.flaskForms import RegistrationForm, LoginForm
from SanchoApp import login_manager
from SanchoApp.databaseModel import User
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def config_routes(app):

    @app.route("/")
    @app.route("/home")
    @login_required
    def home():
        """
        print(current_user.is_authenticated)
        print(current_user.__dict__)

        if current_user.is_authenticated:
            return redirect(url_for('login'))
        """
        return render_template('home.html', posts=posts)

    @app.route("/about")
    @login_required
    def about():
        return render_template('about.html', title='About')

    @app.route("/register", methods=['GET', 'POST'])
    def register():

        # go to home if logged in
        if current_user.is_authenticated:
            return redirect(url_for('home'))


        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data, 
                email=form.email.data,
                password=form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) # authenticate to the login manager
            flash(f'Account created for {form.username.data}!', 'success')
    
            return redirect(url_for('home'))

        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():

        # redirect to home if the user is authenticated:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = LoginForm()
        if form.validate_on_submit():

            # generate a table User structure for the db
            user_database_record = User.query.filter_by(username=form.username.data).first()

            # validate the user:
            if not (form.username.data == 'admin' and form.password.data == 'password'):
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))

            else:
                flash('You have been logged in!', 'success')
                login_user(user_database_record, remember=form.remember.data) # pass to the authenticator the user data
                return redirect(url_for('home'))

        return render_template('login.html', title='Login', form=form)

    
    @app.route("/logout", methods=['GET'])
    def logout():
        logout_user()
        flash('You have been logged out!', 'info')
        return redirect(url_for('login'))

    
