
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4

from SanchoApp.flaskForms import RegistrationForm, LoginForm, RegisterProductForm, UpdateProductForm
from SanchoApp import login_manager, db
from SanchoApp.databaseModel import User, Producto
from sqlalchemy import asc, desc


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def config_routes(app):

    @app.route("/")
    @app.route("/productos")
    @login_required
    def productos():

        product_record = Producto.query.order_by(Producto.categoria).limit(10).all()
        return render_template('productos.html', title='Productos', lista_de_productos=product_record)


    @app.route("/productos/<string:id>",  methods=['GET', 'POST'])
    @login_required
    def update_products(id):

        # get the user info to initialize the form
        product_to_edit = Producto.query.get(id)
        print(product_to_edit)
        if product_to_edit is None:
            return "404"
        else:

            # initialize the form with the requested data
            form = UpdateProductForm(
                nombre=product_to_edit.nombre,
                codigo=product_to_edit.codigo,
                precio=product_to_edit.precio,
                categoria=product_to_edit.categoria,
                cantidad=product_to_edit.cantidad,
                bodega=product_to_edit.bodega,
                estado_activo=product_to_edit.estado_activo
            )

            # update the record if submitted:
            if form.validate_on_submit():
                """
                product_to_edit.nombre=form.nombre.data,
                product_to_edit.codigo=form.codigo.data,
                db.session.commit()
                print(product_to_edit)

                flash(f'Product: {product_to_edit} updated!', 'success')
                """
                return redirect(url_for('productos'))
            
            return render_template('editar_producto.html', title='Editar Producto', form=form)

    @app.route("/productos/registrar", methods=['GET', 'POST'])
    @login_required
    def registrar_productos():

        form = RegisterProductForm()
        if form.validate_on_submit():
            new_product = Producto(
                nombre=form.nombre.data,
                codigo=str(uuid4()),
                precio=form.precio.data,
                categoria=form.categoria.data,
                cantidad=form.cantidad.data,
                bodega=form.bodega.data,
                estado_activo=form.estado_activo.data
            )
            db.session.add(new_product)
            db.session.commit()
            flash(f'New product created! {new_product}!', 'success')

            return redirect(url_for('productos'))

        else:

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
            # authenticate to the login manager
            login_user(new_user, remember=True)
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
            user_database_record = User.query.filter_by(
                username=form.username.data).first()

            # validate the user:
            if not (form.username.data == 'admin' and form.password.data == 'password'):
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))

            else:
                flash('You have been logged in!', 'success')
                # pass to the authenticator the user data
                login_user(user_database_record, remember=form.remember.data)
                return redirect(url_for('productos'))

        return render_template('login.html', title='Login', form=form)

    @app.route("/logout", methods=['GET'])
    def logout():
        logout_user()
        flash('You have been logged out!', 'info')
        return redirect(url_for('login'))
