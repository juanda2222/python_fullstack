
from datetime import datetime
from flask_login import UserMixin  # used to manage the login state inside the db
from sqlalchemy.orm import relationship
from SanchoApp import db


# helper for the many to many relation between Facturas and Productos
relacion_productos_facturas = db.Table(
    'relacion_productos_facturas', 
    db.metadata,
    db.Column('factura_id', db.Integer, db.ForeignKey('facturas.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column("cantidad_producto", db.Integer, nullable=True, default=1)
)


class Factura(db.Model):

    __tablename__="facturas"

    # many to one relation describer
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    relacion_cliente = relationship("Cliente", back_populates="relacion_facturas")

    # many to many relationship
    relacion_productos = relationship("Producto",
                             secondary=relacion_productos_facturas,
                             back_populates="relacion_facturas")

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False, unique=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor_total = db.Column(db.String(10), nullable=False)
    metodo_pago = db.Column(db.String(100), nullable=False, default="efectivo")

    def __repr__(self):
        return f"Factura('{self.codigo}', fecha: '{self.fecha}') \
            Productos: {self.relacion_productos}"

