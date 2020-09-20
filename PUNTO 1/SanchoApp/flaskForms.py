from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    DecimalField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo,  ValidationError
from flask_wtf.file import FileField, FileRequired
from SanchoApp.databaseModel import User, Producto, Cliente, Factura

from wtforms.fields.html5 import DateField

"""
    START Authentication wise forms:
"""


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


"""
    END  Authentication wise forms:
"""


"""
    START Database manager wise forms
"""

# product wise forms:


class RegisterProductForm(FlaskForm):

    nombre = StringField('Nombre del producto', validators=[DataRequired()])
    categoria = StringField('Categoria')
    precio = StringField('Precio en COP', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()], default=1)
    bodega = StringField('Almacenado en Bodega', default="")
    estado_activo = BooleanField('Estado activo', default=True)

    submit = SubmitField('Crear')


class UpdateProductForm(FlaskForm):

    nombre = StringField('Nombre del producto', validators=[DataRequired()])
    codigo = StringField('Codigo del producto', validators=[DataRequired()])
    precio = StringField('Precio en COP', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', default=1)
    categoria = StringField('Categoria', default="")
    bodega = StringField('Almacenado en Bodega', default="")
    estado_activo = BooleanField('Estado activo', default=True)

    submit = SubmitField('Modificar')


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


"""
   END Database manager wise forms
"""
