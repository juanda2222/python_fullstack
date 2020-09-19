from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,  ValidationError
from SanchoApp.databaseModel import User, Producto

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

#product wise forms:
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
    cantidad = IntegerField('Cantidad', validators=[DataRequired()], default=1)
    categoria = StringField('Categoria', default="")
    bodega = StringField('Almacenado en Bodega', default="")
    estado_activo = BooleanField('Estado activo', default=True)

    submit = SubmitField('Modificar')