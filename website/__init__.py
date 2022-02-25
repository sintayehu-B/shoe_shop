from flask import Flask


from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
from os import path



from flask_login import LoginManager, login_manager

db = SQLAlchemy()
DB_NAME = "shopping.db"
# admin = Admin()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'sintayehu'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # initialize our app
    db.init_app(app)
    # admin.init_app(app)
   
    

    from .views import views
    from .auth import auth
    from .api import api_blue
    # from .admin import admin_blue

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api_blue, url_prefix = '/' )
    # app.register_blueprint(admin_blue, url_prefix = '/' ) 

    from .models import User, Product, Order
    create_database(app)

    login_manager = LoginManager()
    # this will redirect us to login page if we are not already logged in  
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    # tell the login_manager which app we are using
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created Database')