from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from .loginview import bp as loginview_bp
    app.register_blueprint(loginview_bp)

    from .addcart import bp as addcart_bp
    app.register_blueprint(addcart_bp)

    return app
