
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    DecimalField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo,  ValidationError
from flask_wtf.file import FileField, FileRequired
from SanchoApp.DatabaseModel import User, Producto, Cliente, Factura

from wtforms.fields.html5 import DateField

class RegisterProductForm(FlaskForm):

    nombre = StringField('Nombre del producto', validators=[DataRequired()])
    categoria = StringField('Categoria')
    codigo = StringField('Codigo del producto', validators=[DataRequired()])
    precio = DecimalField('Precio en COP', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()], default=1)
    bodega = StringField('Almacenado en Bodega', default="")
    estado_activo = BooleanField('Estado activo', default=True)

    submit = SubmitField('Crear')

    def validate_codigo(self, codigo):
        client = Producto.query.filter_by(codigo=codigo.data).first()
        if client is not None:
            raise ValidationError('This code already exists.')

class UpdateProductForm(FlaskForm):

    nombre = StringField('Nombre del producto', validators=[DataRequired()])
    codigo = StringField('Codigo del producto', validators=[DataRequired()])
    precio = DecimalField('Precio en COP', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', default=1)
    categoria = StringField('Categoria', default="")
    bodega = StringField('Almacenado en Bodega', default="")
    estado_activo = BooleanField('Estado activo', default=True)

    submit = SubmitField('Modificar')
