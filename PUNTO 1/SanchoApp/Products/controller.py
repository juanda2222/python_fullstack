  
from flask import Flask, session, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
from os import path, remove
from flask import jsonify


from SanchoApp.Products.model import RegisterProductForm, UpdateProductForm
from SanchoApp import login_manager, db
from SanchoApp.DatabaseModel import User, Producto, Cliente, Factura
from sqlalchemy import asc, desc

def configure_products(app):
  
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

        form = RegisterProductForm(codigo=str(uuid4()))

        if form.validate_on_submit():
            new_product = Producto(
                nombre=form.nombre.data,
                codigo=form.codigo.data,
                precio=str(form.precio.data),
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

            return render_template('productos_registrar.html', title='Registrar producto', form=form)

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
                precio=float(product_to_edit.precio),
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
                return render_template('productos_registrar.html', title='Editar Producto', form=form)
