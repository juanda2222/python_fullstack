
from datetime import datetime
from flask_login import UserMixin  # used to manage the login state inside the db
from sqlalchemy.orm import relationship
from SanchoApp import db


class User(UserMixin, db.Model):

    __tablename__="usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Cliente(db.Model):

    __tablename__="clientes"

    # one to many relation describer
    relacion_facturas = relationship("Factura", back_populates="relacion_cliente")

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.Integer, nullable=True)
    fotografia = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"Client('{self.nombre}', cedula: '{self.cedula}') \
            Facturas: '{self.facturas}'"


# helper for the many to many relation between Facturas and Productos
relacion_productos_facturas = db.Table(
    'relacion_productos_facturas', 
    db.metadata,
    db.Column('factura_id', db.Integer, db.ForeignKey('facturas.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column("cantidad_producto", db.Integer, nullable=False, default=1)
)


class Factura(db.Model):

    __tablename__="facturas"

    # many to one relation describer
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
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
        return f"Produto('{self.id}', '{self.nombre}', '{self.codigo}', '{self.precio}') \
            Facturas: {self.relacion_facturas}"
