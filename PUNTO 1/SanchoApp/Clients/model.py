

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    DecimalField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo,  ValidationError
from flask_wtf.file import FileField, FileRequired
from SanchoApp.DatabaseModel import User, Producto, Cliente, Factura

from wtforms.fields.html5 import DateField


class CreateClientForm(FlaskForm):

    nombre = StringField('Nombre del cliente', validators=[DataRequired()])
    cedula = StringField('Cedula', validators=[DataRequired()])
    direccion = StringField('Dirección')
    telefono = StringField('Telefono')
    fotografia = FileField("Subir foto", validators=[FileRequired()])

    submit = SubmitField('Crear usuario')

    def validate_cedula(self, cedula):
        client = Cliente.query.filter_by(cedula=cedula.data).first()
        if client is not None:
            raise ValidationError('This client already exists.')

class UpdateClientForm(FlaskForm):

    nombre = StringField('Nombre del cliente', validators=[DataRequired()])
    cedula = StringField('Cedula', validators=[DataRequired()])
    direccion = StringField('Dirección')
    telefono = StringField('Telefono')
    fotografia = FileField("Subir foto", validators=[FileRequired()])

    submit = SubmitField('Actulizar usuario')
