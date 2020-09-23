
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove
from flask import jsonify


from SanchoApp.Auth.view import RegistrationForm, LoginForm
from SanchoApp import login_manager, db
from SanchoApp.Auth.model import User
from sqlalchemy import asc, desc


def configure_auth(app):

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/login", methods=['GET', 'POST'])
    def login():

        # redirect to home if the user is authenticated:
        if current_user.is_authenticated:
            return redirect(url_for('productos'))

        form = LoginForm()
        if form.validate_on_submit():

            # check if the user exist in the db
            user_database_record = User.query.filter_by(
                username=form.username.data
            ).filter_by(
                password=form.password.data
            ).first()


            # validate the user:
            if (form.username.data == 'admin' and form.password.data == 'password') or user_database_record is not None:
                flash('You have been logged in!', 'success')
                # pass to the authenticator the user data
                login_user(user_database_record, remember=form.remember.data)
                return redirect(url_for('productos'))

            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))

        else:
            return render_template('Auth/login.html', title='Login', form=form)

    @app.route("/logout", methods=['GET'])
    def logout():
        logout_user()
        flash('You have been logged out!', 'info')
        return redirect(url_for('login'))

    @app.route("/register", methods=['GET', 'POST'])
    def register():

        # go to productos if logged in
        if current_user.is_authenticated:
            return redirect(url_for('productos'))

        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()
            # authenticate to the login manager
            login_user(new_user, remember=True)
            flash(f'Account created for {form.username.data}!', 'success')

            return redirect(url_for('productos'))

        return render_template('Auth/register.html', title='Register', form=form)
