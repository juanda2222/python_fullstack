  
from flask import Flask, session, render_template, url_for, flash, redirect, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove
from flask import jsonify


from SanchoApp.Clients.view import CreateClientForm, UpdateClientForm 
from SanchoApp import login_manager, db
from SanchoApp.Clients.model import Cliente
from sqlalchemy import asc, desc


DEFAULT_USER_PICTURE_STATIC_PATH = "profileImages/default.png"


def configure_clients(app):

    @app.route("/clientes")
    @login_required
    def clientes():

        client_record = Cliente.query.order_by(Cliente.cedula).limit(10).all()
        return render_template('Clients/clientes.html', title='Clientes', lista_de_clientes=client_record)

    @app.route("/clientes/registrar", methods=['GET', 'POST'])
    @login_required
    def registrar_clientes():

        form = CreateClientForm()
        if form.validate_on_submit():

            # save the file in storage manager (mucked by the file system and served as a static file)
            public_file_url = url_for('static', filename=DEFAULT_USER_PICTURE_STATIC_PATH )
            if form.fotografia.data is not None:
                f = form.fotografia.data
                filename_extension = path.splitext(secure_filename(f.filename))[1]
                file_static_path = 'profileImages/'+form.nombre.data + "-" + form.cedula.data + filename_extension
                local_file_path = Path('SanchoApp', "static", file_static_path)
                f.save(local_file_path)
                public_file_url = url_for("static", filename=file_static_path)

            # save client in the database
            new_client = Cliente(
                nombre=form.nombre.data,
                cedula=form.cedula.data,
                direccion=form.direccion.data,
                telefono=form.telefono.data,
                fotografia=public_file_url
            )
            db.session.add(new_client)
            db.session.commit()
            flash(f'New client created! {new_client}!', 'success')

            return redirect(url_for('clientes'))

        else:

            return render_template('Clients/clientes_registrar.html', title='Registrar cliente', form=form)

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

                # save the new file
                if form.fotografia.data is not None:
                    
                    # delete the old picture
                    local_file_path = Path(
                        'SanchoApp', 
                        client_to_edit.fotografia
                        ).absolute()
                    remove(local_file_path)

                    # save the new one
                    f = form.fotografia.data
                    filename_extension = path.splitext(secure_filename(f.filename))[1]
                    file_static_path = 'profileImages/'+form.nombre.data + "-" + form.cedula.data + filename_extension
                    local_file_path = Path('SanchoApp', "static", file_static_path)
                    f.save(local_file_path)
                    public_file_url = url_for("static", filename=file_static_path)
                    client_to_edit.fotografia = public_file_url

                # update the db data
                client_to_edit.nombre = form.nombre.data
                client_to_edit.cedula = form.cedula.data
                client_to_edit.direccion = form.direccion.data
                client_to_edit.telefono = form.telefono.data
                
                db.session.commit()
                return redirect(url_for('clientes'))

            else:
                return render_template('Clients/clientes_registrar.html', title='Editar cliente', form=form)

    @app.route("/clientes/eliminar/<string:id>",  methods=['GET', 'POST'])
    @login_required
    def delete_client(id):

        # get the user info to initialize the form
        client_to_delete = Cliente.query.get(id)

        if client_to_delete is None:
            return "404"
        else:
            
            # delete the picture file if the user used a diferent image
            default_user_image_url = url_for('static', filename=DEFAULT_USER_PICTURE_STATIC_PATH )
            if not (client_to_delete.fotografia == default_user_image_url or client_to_delete.fotografia == None):
                local_file_path = Path(
                    'SanchoApp', 
                    client_to_delete.fotografia
                    ).absolute()
                remove(local_file_path)

            db.session.delete(client_to_delete)
            db.session.commit()

            flash(f'Client {client_to_delete} deleted!', 'warning')
            return redirect(url_for('clientes'))


    