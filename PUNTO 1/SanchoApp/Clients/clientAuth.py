from SanchoApp import create_app, db
from SanchoApp.Auth.model import create_new_user, User
from unittest import TestCase, main

class TestAuth(TestCase):

    def _test_create_user(self):
        
        # use all the required fields
        test_user = create_new_user(
            username="test_username", 
            email="test_email@test.com", 
            password="test_password"
        )
        print("Created user: ", test_user)
        test_database_user = User.query.filter_by( username="test_username" ).first()
        print("User readed from DB: ", test_user)
        self.assertEqual( test_database_user, test_user )
        

    def _test_delete_user(self):
        
        test_user = User.query.filter_by(
            username="test_username"
        ).first()
        print("Test user to delete: ", test_user)
        db.session.delete(test_user)
        db.session.commit()
        print("User deleted!")
        test_user_after_deletion = User.query.filter_by(
            username="test_username"
        ).first()
        print("Test user created query result: ", test_user_after_deletion)
        self.assertEqual(test_user_after_deletion, None)

    def test_create_and_delete_user(self):
        
        app = create_app()

        with app.app_context():
            self._test_create_user()
            self._test_delete_user()
            self.assertTrue(True)


if __name__ == '__main__':
    main()