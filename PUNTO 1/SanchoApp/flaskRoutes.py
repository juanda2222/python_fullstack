
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user

from SanchoApp.flaskForms import RegistrationForm, LoginForm, RegisterProduct
from SanchoApp import login_manager
from SanchoApp.databaseModel import User
posts = [
    {
        'nombre': 'Perros el corral',
        'codigo': 'f343rwekroq2oe',
        'categoria': 'Comestibles',
        'precio': '12000',
        'cantidad': 12,
        'bodega': "Bodega Cali"
    },
    {
        'nombre': 'hamburguesas don pedro',
        'codigo': 'sdgndfg4t4tw',
        'categoria': 'Comestibles',
        'precio': '32000',
        'cantidad': 5,
        'bodega': "Bodega Cali"
    },
    {
        'nombre': 'Tijeras',
        'codigo': '34km3kefmwd',
        'categoria': 'utencilios',
        'precio': '4000',
        'cantidad': 50,
        'bodega': "Bodega Medellin"
    },
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def config_routes(app):

    @app.route("/")
    @app.route("/productos")
    @login_required
    def productos():

        return render_template('productos.html', title='Productos', posts=posts)

    @app.route("/productos/registrar")
    @login_required
    def registrar_productos():
        
        form = RegisterProduct()
        if form.validate_on_submit():
            
            flash(f'New product created! {str(form)}!', 'success')

        return render_template('registrar_productos.html', title='Productos', form=form)


    @app.route("/clientes")
    @login_required
    def clientes():
        return render_template('clientes.html', title='Clientes')

    @app.route("/facturas")
    @login_required
    def facturas():
        return render_template('facturas.html', title='Facturas')

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
            login_user(new_user, remember=True) # authenticate to the login manager
            flash(f'Account created for {form.username.data}!', 'success')
    
            return redirect(url_for('productos'))

        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():

        # redirect to home if the user is authenticated:
        if current_user.is_authenticated:
            return redirect(url_for('productos'))
        
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
                return redirect(url_for('productos'))

        return render_template('login.html', title='Login', form=form)

    
    @app.route("/logout", methods=['GET'])
    def logout():
        logout_user()
        flash('You have been logged out!', 'info')
        return redirect(url_for('login'))

    
