  
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove
from flask import jsonify


from SanchoApp.Clients.model import CreateClientForm, UpdateClientForm 
from SanchoApp import login_manager, db
from SanchoApp.DatabaseModel import User, Producto, Cliente, Factura
from sqlalchemy import asc, desc

def configure_clients(app):

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
                "static",
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

            return render_template('clientes_registrar.html', title='Registrar cliente', form=form)

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
                    "static",
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
                return render_template('clientes_registrar.html', title='Editar cliente', form=form)

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