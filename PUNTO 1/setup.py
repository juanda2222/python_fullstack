
from SanchoApp import create_app, db
from SanchoApp.Auth.model import User
from SanchoApp.Products.model import Producto
from SanchoApp.Clients.model import Cliente
from SanchoApp.Facturas.model import Factura
from SanchoApp.Clients.controller import DEFAULT_USER_PICTURE_STATIC_PATH

DEV_ADMIN_EMAIL = "admin@sancho.com"
DEV_USERNAME = "admin"
DEV_ADMIN_PASSWORD = "password"


def create_dummy_user(db):
    admin_user_record = User(
        email=DEV_ADMIN_EMAIL,
        username=DEV_USERNAME,
        password=DEV_ADMIN_PASSWORD
    )
    gest_user_record = User(
        email=DEV_ADMIN_EMAIL,
        username=DEV_USERNAME,
        password=DEV_ADMIN_PASSWORD
    )
    db.session.add(admin_user_record)
    db.session.add(admin_user_record)
    db.session.commit()
    print(">>> admin user created! ")
    print(">>> gest user created! ")
    users = User.query.all()
    print("Users table: ", users)


def create_dummy_clients(db):
    lista_de_clientes = [
        {
            'nombre': 'Juanda',
            'cedula': "1111",
            'direccion': 'Av cape may 123',
            'telefono': '+2123344',
            'fotografia': "static/profileImages/Juanda-1111.png"
        }, {
            'nombre': 'Robert',
            'cedula': "2222",
            'fotografia': "static/profileImages/Robert-2222.png"
        }, {
            'nombre': 'Daniela',
            'cedula': "3333",
            'direccion': 'Av landmark may 321',
            'telefono': '+332212',
            'fotografia': "static/profileImages/Daniela-3333.png"
        }, {
            'nombre': 'Pepe',
            'cedula': "4455"
        }
    ]

    for nuevo_cliente in lista_de_clientes:
        nuevo_database_client = Cliente(
            nombre=nuevo_cliente["nombre"],
            cedula=nuevo_cliente["cedula"],
            direccion=nuevo_cliente["direccion"] if "direccion" in nuevo_cliente else None,
            telefono=nuevo_cliente["telefono"] if "telefono" in nuevo_cliente else None,
            fotografia=nuevo_cliente["fotografia"] if "fotografia" in nuevo_cliente else "static/profileImages/default.png"
        )
        db.session.add(nuevo_database_client)

    db.session.commit()
    print(">>> Dummy clients inserted! ")
    query = Cliente.query.all()
    print("Clients table: ", query)


def create_dummy_products(db):
    lista_de_productos = [
        {
            'nombre': 'Camisa el corral',
            'codigo': 'f343rwekroq2oe',
            'categoria': 'verano',
            'precio': '12000',
            'cantidad': 12,
            'bodega': "Bodega Cali",
            "estado_activo": False
        },
        {
            'nombre': 'Pantalon don pedro',
            'codigo': 'sdgndfg4t4tw',
            'categoria': 'verano',
            'precio': '32000',
            'cantidad': 5,
            'bodega': "Bodega Cali",
            "estado_activo": False
        },
        {
            'nombre': 'Zapatos gava',
            'codigo': '34km3kefmwd',
            'categoria': 'invierno',
            'precio': '43000',
            'cantidad': 50,
            "estado_activo": True
        }, {
            'nombre': 'Correa don pedro',
            'codigo': 'fg3rg3r23rg',
            'categoria': 'verano',
            'precio': '42000',
            'cantidad': 125,
        },
        {
            'nombre': 'Zapatos rendi',
            'codigo': 'dsfb4t2t234tr4',
            'categoria': 'invierno',
            'precio': '48000',
            'cantidad': 10,
            'bodega': "Bodega Medellin"
        }
    ]

    for producto in lista_de_productos:
        nuevo_producto = Producto(
            nombre=producto["nombre"],
            codigo=producto["codigo"],
            precio=producto["precio"],
            categoria=producto["categoria"] if "categoria" in producto else None,
            cantidad=producto["cantidad"] if "cantidad" in producto else None,
            bodega=producto["bodega"] if "bodega" in producto else None,
            estado_activo=producto["estado_activo"] if "estado_activo" in producto else None
        )
        db.session.add(nuevo_producto)

    db.session.commit()
    print(">>> dummy products inserted! ")
    query = Producto.query.all()
    print("Products table: ", query)
    

if __name__ == "__main__":

    app = create_app()

    # use the context to create a dev version of the db and insert an admin user
    with app.app_context():

        db.create_all()
        print(">>> database created! ")

        create_dummy_user(db)
        create_dummy_clients(db)
        create_dummy_products(db)
