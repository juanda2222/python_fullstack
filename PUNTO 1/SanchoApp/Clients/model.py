

from datetime import datetime
from flask_login import UserMixin  # used to manage the login state inside the db
from sqlalchemy.orm import relationship
from SanchoApp import db


class Cliente(db.Model):

    __tablename__="clientes"

    # one to many relation describer
    relacion_facturas = relationship("Factura", back_populates="relacion_cliente")

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(12), nullable=True)
    fotografia = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"Client('{self.nombre}', cedula: '{self.cedula}' fotografia_url: {self.fotografia} )"
        

def create_new_client(**kargs):
    pass