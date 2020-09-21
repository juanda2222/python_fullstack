from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    DecimalField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo,  ValidationError
from flask_wtf.file import FileField, FileRequired
from SanchoApp.DatabaseModel import User, Producto, Cliente, Factura

from wtforms.fields.html5 import DateField

class CreateFacturaForm(FlaskForm):

    codigo = StringField('Codigo', validators=[DataRequired()])
    fecha = DateField('Fecha de compra')
    valor_total = DecimalField('Valor total', validators=[DataRequired()])
    cedula_cliente = StringField('Cedula de cliente', validators=[DataRequired()])
    metodo_pago = StringField('Metodo de pago', default="efectivo")

    productos = SelectMultipleField('Productos', default=[])

    submit = SubmitField('Crear Factura')


    def validate_cedula_cliente(self, cedula):
        client = Cliente.query.filter_by(cedula=cedula.data).first()
        if client is None:
            raise ValidationError('This client does not Exist.')

    def validate_codigo(self, codigo):
        factura = Factura.query.filter_by(codigo=codigo.data).first()
        if factura is not None:
            raise ValidationError('This code already exist.')



class UpdateFacturaForm(FlaskForm):

    codigo = StringField('Codigo', validators=[DataRequired()])
    fecha = DateField('Fecha de compra')
    valor_total = DecimalField('Valor total', validators=[DataRequired()])
    cedula_cliente = StringField('Cedula de cliente', validators=[DataRequired()])
    metodo_pago = StringField('Metodo de pago', default="efectivo")

    productos = SelectMultipleField('Productos', default=[])

    submit = SubmitField('Actualizar factura')
