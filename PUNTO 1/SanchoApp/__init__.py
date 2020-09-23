from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
login_required

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# init the login_manager to use it later
login_manager = LoginManager()

from SanchoApp.Auth import configure_auth
from SanchoApp.Clients import configure_clients
from SanchoApp.Facturas import configure_facturas
from SanchoApp.Products import configure_products



def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    # load helpper middleware 
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = u"Log in to view this content."
    login_manager.login_message_category = "info"

    # custom configuration
    configure_auth(app)
    configure_clients(app)
    configure_facturas(app)
    configure_products(app)

    """
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    """

    return app

