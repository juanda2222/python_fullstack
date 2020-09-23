  
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove
from flask import jsonify


from SanchoApp.Facturas.view import CreateFacturaForm, UpdateFacturaForm
from SanchoApp import login_manager, db
from SanchoApp.Facturas.model import Factura
from SanchoApp.Products.model import Producto
from SanchoApp.Clients.model import Cliente
from sqlalchemy import asc, desc

def configure_facturas(app):

    @app.route("/facturas")
    @login_required
    def facturas():

        facturas_records = Factura.query.order_by(
            Factura.valor_total).limit(10).all()

        return render_template('Facturas/facturas.html', title='Facturas', lista_de_facturas=facturas_records)

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

            return redirect(url_for('Facturas/facturas'))

        else:

            return render_template('Facturas/facturas_registrar.html', title='Facturas', form=form)

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

                flash(f'Order: {factura_to_edit} modified!', 'success')

                return redirect(url_for('facturas'))

            else:
                return render_template('Facturas/facturas_registrar.html', title='Clientes', form=form)


    @app.route("/facturas/api/<string:codigo>", methods=['GET'])
    def facturas_api(codigo):
        factura_record = Factura.query.filter_by(codigo=codigo).first().__dict__
        factura_record.pop('_sa_instance_state', None)
        print(factura_record)
        return factura_record