
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove

from SanchoApp.flaskForms import RegistrationForm, LoginForm, RegisterProductForm, \
    UpdateProductForm, CreateClientForm, CreateFacturaForm, UpdateClientForm, UpdateFacturaForm
from SanchoApp import login_manager, db
from SanchoApp.databaseModel import User, Producto, Cliente, Factura
from sqlalchemy import asc, desc


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def config_routes(app):

    @app.route("/")
    @app.route("/productos")
    @login_required
    def productos():

        product_record = Producto.query.order_by(
            Producto.categoria).limit(10).all()
        return render_template('productos.html', title='Productos', lista_de_productos=product_record)

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

            return render_template('productos_registrar.html', title='Productos', form=form)

    @app.route("/productos/<string:id>",  methods=['GET', 'POST'])
    @login_required
    def update_products(id):

        # get the user info to initialize the form
        product_to_edit = Producto.query.get(id)

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

                product_to_edit.nombre = form.nombre.data
                product_to_edit.codigo = form.codigo.data
                product_to_edit.categoria = form.categoria.data
                product_to_edit.cantidad = form.cantidad.data
                product_to_edit.bodega = form.bodega.data
                product_to_edit.estado_activo = form.estado_activo.data
                db.session.commit()

                flash(f'Product: {product_to_edit} updated!', 'success')

                return redirect(url_for('productos'))
            else:
                return render_template('productos_editar.html', title='Editar Producto', form=form)

    @app.route("/clientes")
    @login_required
    def clientes():

        client_record = Cliente.query.order_by(Cliente.cedula).limit(10).all()
        return render_template('clientes.html', title='Clientes', lista_de_clientes=client_record)

    @app.route("/clientes/registrar", methods=['GET', 'POST'])
    @login_required
    def registrar_clientes():

        form = CreateClientForm()
        if form.validate_on_submit():

            # save the file in storage manager (mucked by the file system)
            f = form.fotografia.data
            filename_extension = path.splitext(secure_filename(f.filename))[1]
            file_path = Path(
                'SanchoApp',
                'profileImages',
                form.nombre.data + "-" + form.cedula.data + filename_extension
            ).absolute()
            f.save(file_path)

            # save client in the database
            new_client = Cliente(
                nombre=form.nombre.data,
                cedula=form.cedula.data,
                direccion=form.direccion.data,
                telefono=form.telefono.data,
                fotografia=str(file_path)
            )
            db.session.add(new_client)
            db.session.commit()
            flash(f'New client created! {new_client}!', 'success')

            return redirect(url_for('clientes'))

        else:

            return render_template('clientes_registrar.html', title='Clientes', form=form)

    @app.route("/clientes/editar/<string:id>", methods=['GET', 'POST'])
    @login_required
    def editar_clientes(id):

        # get the user info to initialize the form
        client_to_edit = Cliente.query.get(id)

        if client_to_edit is None:
            return "404"
        else:

            form = UpdateClientForm(
                nombre=client_to_edit.nombre,
                cedula=client_to_edit.cedula,
                direccion=client_to_edit.direccion,
                telefono=client_to_edit.telefono
            )

            if form.validate_on_submit():

                # delete the old file:
                remove(client_to_edit.fotografia)

                # save the new file
                f = form.fotografia.data
                filename_extension = path.splitext(
                    secure_filename(f.filename))[1]
                file_path = Path(
                    'SanchoApp',
                    'profileImages',
                    form.nombre.data + "-" + form.cedula.data + filename_extension
                ).absolute()

                # update the db data
                client_to_edit.nombre = form.nombre.data
                client_to_edit.cedula = form.cedula.data
                client_to_edit.direccion = form.direccion.data
                client_to_edit.telefono = form.telefono.data
                client_to_edit.fotografia = str(file_path)
                db.session.commit()
                return redirect(url_for('clientes'))

            else:
                return render_template('clientes_registrar.html', title='Clientes', form=form)

    @app.route("/clientes/eliminar/<string:id>",  methods=['GET', 'POST'])
    @login_required
    def delete_client(id):

        # get the user info to initialize the form
        client_to_delete = Cliente.query.get(id)

        if client_to_delete is None:
            return "404"
        else:

            remove(client_to_delete.fotografia)
            db.session.delete(client_to_delete)
            db.session.commit()

            flash(f'Client {client_to_delete} deleted!', 'warning')
            return redirect(url_for('clientes'))

    @app.route("/facturas")
    @login_required
    def facturas():

        facturas_records = Factura.query.order_by(
            Factura.valor_total).limit(10).all()

        return render_template('facturas.html', title='Facturas', lista_de_facturas=facturas_records)

    @app.route("/facturas/registrar", methods=['GET', 'POST'])
    @login_required
    def registrar_facturas():

        form = CreateFacturaForm(codigo=str(uuid4()))
        productos = Producto.query.order_by(Producto.precio).limit(100).all()

        # generate a list of products to display
        def map_id__name_id(producto):
            return (str(producto.id), producto.nombre + "-" + producto.codigo)
        id__name_map = map(map_id__name_id, productos)
        form.productos.choices = list(id__name_map)

        if form.validate_on_submit():

            lista_productos = list()

            # map the selected options to a list of products:
            for id_producto in form.productos.data:
                lista_productos.append(Producto.query.get(int(id_producto)))

            
            # save factura in the database
            new_factura = Factura(
                cliente_id=Cliente.query.filter_by(
                    cedula=form.cedula_cliente.data).first().id,
                codigo=form.codigo.data,
                fecha=form.fecha.data,
                valor_total=str(form.valor_total.data),
                metodo_pago=form.metodo_pago.data,
                relacion_productos=lista_productos

            )
            db.session.add(new_factura)
            db.session.commit()
            flash(f'New Order created! {new_factura}!', 'success')

            return redirect(url_for('facturas'))

        else:

            return render_template('facturas_registrar.html', title='Facturas', form=form)

    @app.route("/facturas/editar/<string:id>", methods=['GET', 'POST'])
    @login_required
    def editar_facturas(id):

        # get the user info to initialize the form
        factura_to_edit = Factura.query.get(id)

        if factura_to_edit is None:
            return "404"
        else:
                        
            form = UpdateFacturaForm(
                codigo=factura_to_edit.codigo,
                fecha=factura_to_edit.fecha,
                valor_total=float(factura_to_edit.valor_total),
                cedula_cliente=Cliente.query.get(factura_to_edit.cliente_id).cedula,
                metodo_pago=factura_to_edit.metodo_pago
            )

            
            # generate a list of products to display
            productos = Producto.query.order_by(Producto.precio).limit(100).all()
            def map_id__name_id(producto):
                return (str(producto.id), producto.nombre + "-" + producto.codigo)
            id__name_map = map(map_id__name_id, productos)
            form.productos.choices = list(id__name_map)

            # map to create the selected products:
            def map_product_to_id(producto):
                return str(producto.id)
            id_map = map(map_product_to_id, factura_to_edit.relacion_productos)
            print(list(id_map))
            form.productos.default = list(id_map)
            form.productos.selected = list(id_map)
            

            if form.validate_on_submit():

                lista_productos = list()

                # map the selected options to a list of products:
                for id_producto in form.productos.data:
                    lista_productos.append(Producto.query.get(int(id_producto)))

                # update the db data
                factura_to_edit.codigo = form.codigo.data
                factura_to_edit.fecha = form.fecha.data
                factura_to_edit.valor_total = str(form.valor_total.data)
                factura_to_edit.metodo_pago = form.metodo_pago.data
                factura_to_edit.cliente_id = Cliente.query.filter_by(cedula=form.cedula_cliente.data).first().id
                factura_to_edit.relacion_productos = lista_productos
                db.session.commit()
                return redirect(url_for('facturas'))

            else:
                return render_template('facturas_registrar.html', title='Clientes', form=form)

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
        else:
            return render_template('login.html', title='Login', form=form)

    @app.route("/logout", methods=['GET'])
    def logout():
        logout_user()
        flash('You have been logged out!', 'info')
        return redirect(url_for('login'))
