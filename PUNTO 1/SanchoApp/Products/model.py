
from datetime import datetime
from flask_login import UserMixin  # used to manage the login state inside the db
from sqlalchemy.orm import relationship
from SanchoApp import db

from SanchoApp.Facturas.model import relacion_productos_facturas

class Producto(db.Model):

    __tablename__="productos"

    # many to many relationship
    relacion_facturas = relationship("Factura",
                            secondary=relacion_productos_facturas,
                            back_populates="relacion_productos")

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.String(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    categoria = db.Column(db.String(100), nullable=True)
    bodega = db.Column(db.String(100), nullable=True)
    estado_activo = db.Column(db.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return f"Produto('{self.id}', '{self.nombre}', '{self.codigo}', '{self.precio}')"
