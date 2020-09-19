from SanchoApp import create_app, db
from SanchoApp.databaseModel import Producto

if __name__ == "__main__":

    app = create_app()

    # use the context to create a dev version of the db and insert an admin user
    with app.app_context():

        
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
                'bodega': "Bodega Cali"
                "estado_activo": False
            },
            {
                'nombre': 'Zapatos gava',
                'codigo': '34km3kefmwd',
                'categoria': 'invierno',
                'precio': '43000',
                'cantidad': 50,
                "estado_activo": True
            },{
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
            nuevo_producto = Productos(
                nombre=producto["nombre"],
                codigo=producto["codigo"],
                categoria=producto["categoria"],
                precio=producto["precio"],
                cantidad=producto["cantidad"],
                bodega=producto["bodega"],
                estado_activo=producto["estado_activo"]
            )
            db.session.add(nuevo_producto)

        db.session.commit()
        print(">>> admin user created! ")
        print("Users table: ")
        print(User.query.all())