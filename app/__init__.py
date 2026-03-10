from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main as main_blueprint
    from app.routes.admin import admin as admin_blueprint
    from app.routes.employer import employer as employer_blueprint
    from app.routes.fresher import fresher as fresher_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(employer_blueprint)
    app.register_blueprint(fresher_blueprint)

    return app
