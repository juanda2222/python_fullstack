from SanchoApp import create_app, db
from SanchoApp.Products.model import Producto
from unittest import TestCase, main

class TestEncription(TestCase):

    def test_insert_and_read_dumb_products(self):

        app = create_app()

        # use the context to create a dev version of the db and insert an admin user
        with app.app_context():

            
            
            print(query)

            self.assertTrue(5 < len(query))

if __name__ == '__main__':
    main()