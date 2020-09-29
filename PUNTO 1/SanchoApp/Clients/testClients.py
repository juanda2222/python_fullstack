from SanchoApp import create_app, db
from SanchoApp.Auth.model import create_new_user, User
from unittest import TestCase, main

class TestAuth(TestCase):

    def _test_create_client(self):
    """
    TODO:   create function
    """    
        # use all the required fields
        pass
        

    def _test_delete_clients(self):
    """
    TODO:   create function
    """ 
        pass

    def test_create_and_delete_user(self):
        
        app = create_app()

        with app.app_context():
            self._test_create_user()
            self._test_delete_user()
            self.assertTrue(True)


if __name__ == '__main__':
    main()