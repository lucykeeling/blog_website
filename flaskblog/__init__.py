from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt  # added so routes.py can import bcrypt via `from . import bcrypt`
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Initialize extensions without binding them to an app yet.
# They get bound in create_app() via .init_app(app).
mysql = MySQL()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap5()
load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = '6139bba5591f08c4ebfaba0bf2edee0b'
    
    # MySQL configuration settings
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = 'blog'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # Bind extensions to the app instance
    mysql.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html')

    # 3. Import and register blueprints HERE to avoid circular loops
    from flaskblog.routes import bp
    app.register_blueprint(bp)

    return app