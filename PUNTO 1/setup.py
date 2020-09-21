
from SanchoApp import create_app, db
from SanchoApp.DatabaseModel import User

DEV_ADMIN_EMAIL = "admin@sancho.com"
DEV_USERNAME = "admin"
DEV_ADMIN_PASSWORD = "password"

if __name__ == "__main__":

    app = create_app()

    # use the context to create a dev version of the db and insert an admin user
    with app.app_context():

        db.create_all()
        print(">>> database created! ")

        admin_user_record = User(
            email=DEV_ADMIN_EMAIL,
            username=DEV_USERNAME,
            password=DEV_ADMIN_PASSWORD
        )
        db.session.add(admin_user_record)
        db.session.commit()
        print(">>> admin user created! ")
        print("Users table: ")
        print(User.query.all())